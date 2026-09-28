import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import init_db
from app.seed_data import seed_database
from app.ai.vision_agent import analyze_single_issue, analyze_room_scan
from app.ai.duplicate_agent import detect_duplicates
from app.ai.verification_agent import verify_repair_evidence
from app.routers.incidents import list_incidents

def test_backend_components():
    print("1. Testing DB Init & Seeding...")
    init_db()
    seed_database()

    print("2. Testing Incidents List...")
    incidents = list_incidents()
    assert len(incidents) >= 4, f"Expected at least 4 seeded incidents, got {len(incidents)}"
    print(f"   Found {len(incidents)} incidents. First: {incidents[0]['id']} - {incidents[0]['title']}")

    print("3. Testing Vision Agent Single Issue...")
    res = analyze_single_issue("test image data with broken fan", "Room 204")
    assert res["is_maintenance_issue"] is True
    print(f"   Detected: {res['object']} ({res['department']}, {res['priority']})")

    print("4. Testing Room Scan Mode...")
    scan = analyze_room_scan("test wide classroom image", "Room 204")
    assert scan["total_issues_detected"] >= 2
    print(f"   Room Scan found {scan['total_issues_detected']} issues in {scan['room_name']}")

    print("5. Testing Duplicate Detection...")
    dup = detect_duplicates("Block B / Room 204", "Electrical", "Ceiling Fan", incidents)
    assert dup["is_duplicate"] is True
    print(f"   Duplicate Detection: Match={dup['is_duplicate']}, Conf={dup['confidence']}, Target={dup['matched_incident']['id']}")

    print("6. Testing Before/After AI Verification Agent...")
    ver = verify_repair_evidence("before_img", "after_img", {"title": "Ceiling Fan", "location": "Room 204"})
    assert ver["verification_status"] == "CONSISTENT_VERIFIED"
    print(f"   AI Verification: Status={ver['verification_status']}, Conf={ver['resolution_confidence']}")

    print("\nALL BACKEND CORE TESTS PASSED SUCCESSFULLY! ✅")

if __name__ == "__main__":
    test_backend_components()
