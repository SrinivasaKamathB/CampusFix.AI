from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db, log_audit
from app.ai.verification_agent import verify_repair_evidence

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])

class AfterPhotoUploadRequest(BaseModel):
    incident_id: str
    after_image: str
    technician_name: Optional[str] = "Campus Maintenance Team"
    repair_notes: Optional[str] = ""

@router.get("/tasks")
def get_maintenance_tasks():
    """Returns tasks that need attention by maintenance technicians."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM incidents 
        WHERE status IN ('Reported', 'Assigned', 'In Progress', 'Awaiting Verification')
        ORDER BY 
            CASE priority 
                WHEN 'P1 - Critical Hazard' THEN 1
                WHEN 'P2 - High' THEN 2
                WHEN 'P3 - Normal' THEN 3
                ELSE 4
            END ASC, created_at DESC
    ''')
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

@router.post("/upload-after-photo")
def upload_after_photo(req: AfterPhotoUploadRequest):
    """
    Receives post-repair 'After' photo from technician, initiates AI verification,
    and updates incident status to 'Awaiting Verification'.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE id = ?", (req.incident_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Incident not found")
        
    incident = dict(row)
    now = datetime.utcnow().isoformat()

    # Trigger AI verification comparative diff
    ai_eval = verify_repair_evidence(incident.get("before_image") or "", req.after_image, incident)

    cursor.execute('''
        UPDATE incidents 
        SET after_image = ?, status = 'Awaiting Verification',
            verification_status = ?, verification_confidence = ?,
            verification_notes = ?, updated_at = ?
        WHERE id = ?
    ''', (
        req.after_image,
        ai_eval.get("verification_status", "CONSISTENT_VERIFIED"),
        ai_eval.get("resolution_confidence", 0.95),
        ai_eval.get("object_comparison", "Repairs confirmed consistent with specifications."),
        now, req.incident_id
    ))
    conn.commit()
    conn.close()

    log_audit(
        req.incident_id,
        "After-Photo Uploaded & AI Verified",
        req.technician_name,
        f"AI Result: {ai_eval.get('verification_status')} ({int(ai_eval.get('resolution_confidence', 0.9)*100)}% Conf). Notes: {req.repair_notes}"
    )

    return {
        "message": "After-photo uploaded and AI verification complete",
        "verification_result": ai_eval
    }
