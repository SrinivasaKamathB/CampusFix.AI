import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import DEMO_ASSETS_DIR
from app.database import init_db
from app.seed_data import seed_database
from app.routers import incidents, maintenance, verification, analytics

app = FastAPI(
    title="CampusFix AI API",
    description="Visual Campus Maintenance & Resolution Intelligence System",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database & seed data on startup
@app.on_event("startup")
def on_startup():
    init_db()
    seed_database()

# Include Routers
app.include_router(incidents.router)
app.include_router(maintenance.router)
app.include_router(verification.router)
app.include_router(analytics.router)

# Mount static demo assets if directory exists
if os.path.exists(DEMO_ASSETS_DIR):
    app.mount("/demo_assets", StaticFiles(directory=str(DEMO_ASSETS_DIR)), name="demo_assets")

from fastapi.responses import FileResponse

STATIC_DIR = Path(__file__).resolve().parent / "static"
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def root_view():
    index_path = STATIC_DIR / "index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "system": "CampusFix AI",
        "tagline": "Don't fill a complaint form. Show the problem.",
        "status": "online"
    }

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs"

@app.get("/download/pdf")
def download_pdf():
    pdf_path = DOCS_DIR / "CampusFix_AI_Project_Overview.pdf"
    if pdf_path.exists():
        return FileResponse(
            path=str(pdf_path),
            filename="CampusFix_AI_Project_Overview.pdf",
            media_type="application/pdf"
        )
    return {"error": "File not found"}

@app.get("/download/presentation")
def download_presentation():
    html_path = DOCS_DIR / "CampusFix_AI_Presentation.html"
    if html_path.exists():
        return FileResponse(
            path=str(html_path),
            filename="CampusFix_AI_Presentation.html",
            media_type="text/html"
        )
    return {"error": "File not found"}

@app.get("/download/pitch-guide")
def download_pitch_guide():
    guide_path = DOCS_DIR / "CampusFix_AI_Judge_Pitch.md"
    if guide_path.exists():
        return FileResponse(
            path=str(guide_path),
            filename="CampusFix_AI_Judge_Pitch.md",
            media_type="text/markdown"
        )
    return {"error": "File not found"}

<<<<<<< HEAD
=======
@app.get("/download/code")
@app.get("/download/zip")
def download_complete_code():
    zip_path = Path(__file__).resolve().parent.parent.parent / "campusfix-ai-complete.zip"
    if zip_path.exists():
        return FileResponse(
            path=str(zip_path),
            filename="campusfix-ai-complete.zip",
            media_type="application/zip"
        )
    return {"error": "Archive not found"}

>>>>>>> 415013a (Update logo design, README documentation, and asset packages)
