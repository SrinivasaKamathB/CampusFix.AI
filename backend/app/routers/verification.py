from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db, log_audit
from app.ai.verification_agent import verify_repair_evidence

router = APIRouter(prefix="/api/verification", tags=["verification"])

class ReVerifyRequest(BaseModel):
    incident_id: str

class SupervisorApprovalRequest(BaseModel):
    incident_id: str
    supervisor_name: Optional[str] = "Chief Facilities Officer"
    approval_notes: Optional[str] = "Physical resolution visually verified. Approved for closure."

@router.get("/pending")
def get_pending_verifications():
    """Returns incidents awaiting final supervisor sign-off after AI verification."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM incidents 
        WHERE status = 'Awaiting Verification'
        ORDER BY updated_at DESC
    ''')
    incidents = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return incidents

@router.post("/reverify")
def reverify_incident(req: ReVerifyRequest):
    """Re-runs the comparative visual diff between before and after images."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE id = ?", (req.incident_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Incident not found")
        
    incident = dict(row)
    if not incident.get("before_image") or not incident.get("after_image"):
        conn.close()
        raise HTTPException(status_code=400, detail="Both before and after images are required for verification")

    result = verify_repair_evidence(incident["before_image"], incident["after_image"], incident)
    
    cursor.execute('''
        UPDATE incidents 
        SET verification_status = ?, verification_confidence = ?, verification_notes = ?
        WHERE id = ?
    ''', (result["verification_status"], result["resolution_confidence"], result["object_comparison"], req.incident_id))
    conn.commit()
    conn.close()

    return {"message": "Re-verification completed", "result": result}

@router.post("/approve")
def approve_resolution(req: SupervisorApprovalRequest):
    """Supervisor conducts final sign-off, transitioning ticket to Verified Resolved."""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    cursor.execute('''
        UPDATE incidents 
        SET status = 'Verified Resolved', resolved_at = ?, updated_at = ?
        WHERE id = ?
    ''', (now, now, req.incident_id))
    conn.commit()
    conn.close()

    log_audit(
        req.incident_id,
        "Verified & Signed-Off",
        req.supervisor_name,
        req.approval_notes
    )

    return {"message": f"Incident {req.incident_id} successfully marked as Verified Resolved"}
