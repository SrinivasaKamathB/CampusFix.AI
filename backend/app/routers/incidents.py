from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

from app.database import get_db, log_audit
from app.ai.vision_agent import analyze_single_issue, analyze_room_scan
from app.ai.duplicate_agent import detect_duplicates

router = APIRouter(prefix="/api", tags=["incidents"])

class AnalyzeRequest(BaseModel):
    image_data: str
    location_hint: Optional[str] = ""
    is_room_scan: Optional[bool] = False

class DuplicateCheckRequest(BaseModel):
    location: str
    category: str
    object_name: str

class IncidentCreateRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    location: str
    category: str
    department: str
    priority: str
    before_image: Optional[str] = ""
    confidence: Optional[float] = 0.92
    reporter_role: Optional[str] = "Student"
    is_room_scan: Optional[bool] = False

class BatchIncidentCreateRequest(BaseModel):
    location: str
    before_image: Optional[str] = ""
    issues: List[dict]

class StatusUpdateRequest(BaseModel):
    status: str
    actor: Optional[str] = "Maintenance Supervisor"
    notes: Optional[str] = ""


@router.post("/analyze-image")
def analyze_image(req: AnalyzeRequest):
    """Analyzes an image using either single defect mode or room scan mode."""
    if not req.image_data:
        raise HTTPException(status_code=400, detail="Image data is required")
        
    if req.is_room_scan:
        result = analyze_room_scan(req.image_data, req.location_hint)
        return {"mode": "room_scan", "data": result}
    else:
        result = analyze_single_issue(req.image_data, req.location_hint)
        return {"mode": "single_issue", "data": result}


@router.post("/check-duplicates")
def check_duplicates_endpoint(req: DuplicateCheckRequest):
    """Checks if a similar incident is already open for this location/category."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE status != 'Verified Resolved'")
    open_incidents = [dict(row) for row in cursor.fetchall()]
    conn.close()

    result = detect_duplicates(req.location, req.category, req.object_name, open_incidents)
    return result


@router.post("/incidents")
def create_incident(req: IncidentCreateRequest):
    """Creates a new incident record and initializes the workflow lifecycle."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Generate sequential friendly ID: CF-101, CF-102, etc.
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]
    incident_id = f"CF-{101 + count}"
    
    now = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO incidents (
            id, title, description, location, category, department, priority,
            status, reporter_role, before_image, confidence, is_room_scan,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        incident_id, req.title, req.description, req.location, req.category,
        req.department, req.priority, "Reported", req.reporter_role,
        req.before_image, req.confidence, 1 if req.is_room_scan else 0,
        now, now
    ))
    conn.commit()
    conn.close()

    log_audit(incident_id, "Incident Created", req.reporter_role, f"Routed to {req.department} with priority {req.priority}")
    return {"message": "Incident created successfully", "incident_id": incident_id}


@router.post("/incidents/batch")
def create_batch_incidents(req: BatchIncidentCreateRequest):
    """Creates multiple incidents simultaneously from a Room Scan pass."""
    conn = get_db()
    cursor = conn.cursor()
    created_ids = []
    
    cursor.execute("SELECT COUNT(*) FROM incidents")
    base_count = cursor.fetchone()[0]

    now = datetime.utcnow().isoformat()
    for idx, item in enumerate(req.issues):
        inc_id = f"CF-{101 + base_count + idx}"
        title = f"{item.get('object', 'Asset')} - {item.get('defect', 'Defect')}"
        cursor.execute('''
            INSERT INTO incidents (
                id, title, description, location, category, department, priority,
                status, reporter_role, before_image, confidence, is_room_scan,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            inc_id, title, f"Detected via Room Scan: {item.get('bounding_area', 'Room Area')}",
            req.location, item.get("category", "General"), item.get("department", "Facilities"),
            item.get("priority", "P3 - Normal"), "Reported", "Student / Room Scan",
            req.before_image, item.get("confidence", 0.90), 1, now, now
        ))
        created_ids.append(inc_id)
        log_audit(inc_id, "Room Scan Auto-Dispatch", "Room Scan AI", f"Batch item created for {req.location}")

    conn.commit()
    conn.close()
    return {"message": f"Created {len(created_ids)} incidents from Room Scan", "incident_ids": created_ids}


@router.get("/incidents")
def list_incidents(status: Optional[str] = None, department: Optional[str] = None, search: Optional[str] = None):
    """Returns all incidents filtered by status, department, or search query."""
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM incidents WHERE 1=1"
    params = []
    
    if status and status != "All":
        query += " AND status = ?"
        params.append(status)
        
    if department and department != "All":
        query += " AND department = ?"
        params.append(department)
        
    if search:
        query += " AND (title LIKE ? OR location LIKE ? OR id LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
        
    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    incidents = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return incidents


@router.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    """Retrieves detailed information and audit history for a single incident."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Incident not found")
        
    incident = dict(row)
    
    # Fetch audit logs
    cursor.execute("SELECT * FROM audit_logs WHERE incident_id = ? ORDER BY timestamp ASC", (incident_id,))
    incident["audit_logs"] = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return incident


@router.post("/incidents/{incident_id}/upvote")
def upvote_incident(incident_id: str):
    """Increments the upvote counter when duplicate incidents are merged."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET upvotes = upvotes + 1 WHERE id = ?", (incident_id,))
    conn.commit()
    cursor.execute("SELECT upvotes FROM incidents WHERE id = ?", (incident_id,))
    new_count = cursor.fetchone()[0]
    conn.close()
    
    log_audit(incident_id, "Report Merged / Upvoted", "Student Reporter", f"Duplicate avoided. Upvotes now: {new_count}")
    return {"message": "Incident upvoted successfully", "upvotes": new_count}


@router.patch("/incidents/{incident_id}/status")
def update_incident_status(incident_id: str, req: StatusUpdateRequest):
    """Transitions an incident to a new workflow status."""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    resolved_time = now if req.status == "Verified Resolved" else None
    
    cursor.execute('''
        UPDATE incidents 
        SET status = ?, updated_at = ?, resolved_at = COALESCE(?, resolved_at)
        WHERE id = ?
    ''', (req.status, now, resolved_time, incident_id))
    conn.commit()
    conn.close()
    
    log_audit(incident_id, f"Status Changed to '{req.status}'", req.actor, req.notes)
    return {"message": f"Status updated to {req.status}"}
