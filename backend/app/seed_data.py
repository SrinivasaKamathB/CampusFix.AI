import os
import base64
from datetime import datetime, timedelta
from app.database import get_db, init_db, log_audit
from app.config import DEMO_ASSETS_DIR

def get_demo_asset_data(filename):
    path = os.path.join(DEMO_ASSETS_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            svg_text = f.read()
            b64 = base64.b64encode(svg_text.encode('utf-8')).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"
    return ""

def seed_database():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM incidents")
    if cursor.fetchone()[0] > 0:
        conn.close()
        print("Database already contains records. Skipping seed.")
        return

    now = datetime.utcnow()
    fan_broken_img = get_demo_asset_data("classroom_fan_broken.svg")
    fan_fixed_img = get_demo_asset_data("classroom_fan_fixed.svg")
    leak_img = get_demo_asset_data("washroom_leak.svg")

    seed_items = [
        {
            "id": "CF-101",
            "title": "Ceiling Fan - Bent Blade & Motor Wobble",
            "description": "Ceiling fan blade warped at 35 degrees. Non-functional and creates safety hazard.",
            "location": "Block B / Room 204",
            "category": "Electrical",
            "department": "Electrical Maintenance",
            "priority": "P2 - High",
            "status": "In Progress",
            "reporter_role": "Student (Computer Science)",
            "before_image": fan_broken_img,
            "after_image": None,
            "confidence": 0.96,
            "upvotes": 4,
            "is_room_scan": 0,
            "created_at": (now - timedelta(hours=4)).isoformat(),
            "updated_at": (now - timedelta(hours=1)).isoformat()
        },
        {
            "id": "CF-102",
            "title": "Water Pipe Joint - High-Pressure Leak",
            "description": "Corroded elbow joint leaking actively. Standing water accumulating near washroom door.",
            "location": "Block C / 2nd Fl Washroom",
            "category": "Plumbing",
            "department": "Plumbing & Sanitation",
            "priority": "P1 - Critical Hazard",
            "status": "Reported",
            "reporter_role": "Faculty (Mechanical Dept)",
            "before_image": leak_img,
            "after_image": None,
            "confidence": 0.95,
            "upvotes": 8,
            "is_room_scan": 0,
            "created_at": (now - timedelta(hours=2)).isoformat(),
            "updated_at": (now - timedelta(hours=2)).isoformat()
        },
        {
            "id": "CF-103",
            "title": "Fluorescent Tube Fitting - Loose Ballast & Flickering",
            "description": "Rapid strobe flickering causing visual distraction in lab.",
            "location": "Science Block / Lab 3",
            "category": "Electrical",
            "department": "Electrical Maintenance",
            "priority": "P3 - Normal",
            "status": "Awaiting Verification",
            "reporter_role": "Student (Physics)",
            "before_image": fan_broken_img,
            "after_image": fan_fixed_img,
            "confidence": 0.92,
            "upvotes": 1,
            "is_room_scan": 0,
            "verification_status": "CONSISTENT_VERIFIED",
            "verification_confidence": 0.95,
            "verification_notes": "Electronic ballast replaced; tube securely anchored and illumination normalized.",
            "created_at": (now - timedelta(hours=6)).isoformat(),
            "updated_at": (now - timedelta(minutes=25)).isoformat()
        },
        {
            "id": "CF-104",
            "title": "Lecture Hall 1 - Cracked Wooden Bench Leg",
            "description": "Fractured support bracket on dual bench.",
            "location": "Main Block / Lecture Hall 1",
            "category": "Carpentry",
            "department": "Carpentry & Furniture",
            "priority": "P3 - Normal",
            "status": "Verified Resolved",
            "reporter_role": "Staff",
            "before_image": fan_broken_img,
            "after_image": fan_fixed_img,
            "confidence": 0.89,
            "upvotes": 2,
            "is_room_scan": 0,
            "verification_status": "CONSISTENT_VERIFIED",
            "verification_confidence": 0.97,
            "verification_notes": "Structural bracket replaced and bolt tightened. Verified by Chief Facilities Officer.",
            "created_at": (now - timedelta(days=1, hours=2)).isoformat(),
            "updated_at": (now - timedelta(hours=5)).isoformat(),
            "resolved_at": (now - timedelta(hours=5)).isoformat()
        }
    ]

    for item in seed_items:
        cursor.execute('''
            INSERT INTO incidents (
                id, title, description, location, category, department, priority,
                status, reporter_role, before_image, after_image, confidence, upvotes,
                is_room_scan, verification_status, verification_confidence, verification_notes,
                created_at, updated_at, resolved_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item["id"], item["title"], item["description"], item["location"],
            item["category"], item["department"], item["priority"], item["status"],
            item["reporter_role"], item["before_image"], item.get("after_image"),
            item["confidence"], item["upvotes"], item["is_room_scan"],
            item.get("verification_status", "Unverified"),
            item.get("verification_confidence", 0.0),
            item.get("verification_notes"), item["created_at"], item["updated_at"],
            item.get("resolved_at")
        ))
        
        cursor.execute('''
            INSERT INTO audit_logs (incident_id, action, actor, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (item["id"], "Incident Logged", item["reporter_role"], f"Initial report received for {item['location']}", item["created_at"]))
        
        if item["status"] in ["Awaiting Verification", "Verified Resolved"]:
            cursor.execute('''
                INSERT INTO audit_logs (incident_id, action, actor, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (item["id"], "Repair Completed", "Maintenance Staff", "Uploaded post-repair photo evidence", item["updated_at"]))
            
        if item["status"] == "Verified Resolved":
            cursor.execute('''
                INSERT INTO audit_logs (incident_id, action, actor, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (item["id"], "Resolution Verified & Signed-Off", "Chief Facilities Officer", "Proof-of-work accepted", item["resolved_at"] or item["updated_at"]))

    conn.commit()
    conn.close()
    print("Database seeded with sample campus incidents successfully.")

if __name__ == "__main__":
    seed_database()
