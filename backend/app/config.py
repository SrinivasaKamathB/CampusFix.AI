import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEMO_ASSETS_DIR = BASE_DIR.parent / "demo_assets"
DB_PATH = BASE_DIR / "campusfix.db"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0")

# Departments configuration
DEPARTMENTS = [
    "Electrical Maintenance",
    "Plumbing & Sanitation",
    "Carpentry & Furniture",
    "IT & Audio-Visual Support",
    "Housekeeping & Facilities"
]

# Standard Priority Levels
PRIORITIES = ["P1 - Critical Hazard", "P2 - High", "P3 - Normal", "P4 - Low"]

# Status Lifecycle
STATUS_LIFECYCLE = [
    "Reported",
    "Reviewed",
    "Assigned",
    "In Progress",
    "Awaiting Verification",
    "Verified Resolved"
]
