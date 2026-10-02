<<<<<<< HEAD
# CampusFix AI

## AI-Powered Visual Campus Maintenance and Repair Verification

CampusFix AI is a software-based campus maintenance system that uses AI-powered image analysis to transform maintenance photographs into structured incidents, identify potential duplicate reports, route incidents to the appropriate maintenance department, and verify completed repairs using before-and-after evidence.

The system follows a complete maintenance workflow:

```text
Capture → Understand → Classify → Route → Repair → Verify → Close
```

CampusFix AI is designed as a software-only prototype and does not require dedicated campus hardware or IoT devices.

---

## Features

### Visual Issue Analysis

CampusFix AI analyzes uploaded maintenance photographs and extracts structured information about the reported issue.

The analysis can include:

* Issue category
* Description
* Location and room information
* Detected objects
* Maintenance department
* Confidence information

The system uses multimodal AI analysis when the configured AI service is available.

### Room Scan

A single classroom or room photograph can contain multiple maintenance problems.

The Room Scan functionality analyzes the complete scene and can identify multiple issues from one image instead of requiring separate reports for every visible problem.

Detected issues can include normalized bounding-box information for the identified objects.

### Duplicate Detection

CampusFix AI checks new incidents against existing reports to identify potential duplicate maintenance requests.

The specified similarity approach combines:

* Location similarity
* Room similarity
* Category similarity
* Object similarity

The technical specification defines the following similarity calculation:

```text
Similarity =
0.45 × Location
+ 0.15 × Room
+ 0.20 × Category
+ 0.30 × Object Jaccard
```

A similarity score of `0.65` or higher is used by the specified workflow for duplicate handling.

### Maintenance Department Routing

After an incident has been analyzed, it can be assigned to the appropriate maintenance department.

```text
Incident
   |
   v
Category and Context
   |
   v
Maintenance Department
   |
   v
Assigned Technician
```

### Before and After Repair Verification

CampusFix AI introduces an evidence-based verification stage after a maintenance task has been completed.

Instead of relying only on a technician marking an incident as completed, the system can use an after-repair photograph together with the original incident evidence.

```text
Before Image
     |
     v
Maintenance Work
     |
     v
After Image
     |
     v
AI Verification
     |
     v
Verified / Requires Review
```

The verification process produces information such as verification status, confidence, and notes.

### Maintenance Dashboard

The dashboard provides an overview of maintenance activity, including information related to:

* Total incidents
* Open incidents
* Assigned incidents
* In-progress work
* Verification status
* Resolved incidents
* Maintenance activity

### Audit Trail

Important incident actions can be recorded as part of the maintenance audit history.

This provides visibility into how an incident progresses through the system.

### Offline and Fallback Processing

The system includes a fallback path for situations where the external AI service is unavailable, times out, or is not configured.

This allows the prototype to continue demonstrating the maintenance workflow without depending entirely on external AI availability.

---

## System Workflow

CampusFix AI is organized around seven major stages.

```text
+----------+
| Capture  |
+----+-----+
     |
     v
+------------+
| Understand |
+-----+------+
      |
      v
+----------+
| Classify |
+----+-----+
     |
     v
+--------+
| Route  |
+---+----+
    |
    v
+---------+
| Repair  |
+----+----+
     |
     v
+---------+
| Verify  |
+----+----+
     |
     v
+---------+
|  Close  |
+---------+
```

This workflow connects the initial maintenance report with department assignment, physical repair, evidence collection, and final verification.

---

## AI Architecture

CampusFix AI separates its main AI responsibilities into three agents.

```text
                    CampusFix AI
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
   Vision Agent   Duplicate Agent   Verification Agent
          |              |              |
          v              v              v
   Image Analysis   Duplicate Check   Repair Verification
```

### Vision Agent

File:

```text
backend/app/ai/vision_agent.py
```

Responsibilities include:

* Image understanding
* Maintenance issue extraction
* Category identification
* Context and location extraction
* Room Scan analysis
* Structured AI responses

The technical specification describes multimodal Gemini analysis with structured JSON output and fallback processing.

### Duplicate Agent

File:

```text
backend/app/ai/duplicate_agent.py
```

The Duplicate Agent evaluates whether a newly submitted incident may correspond to an existing incident.

It combines multiple signals rather than depending on a single similarity measure.

```text
Location
   +
Room
   +
Category
   +
Objects
   |
   v
Similarity Analysis
   |
   v
Duplicate Assessment
```

### Verification Agent

File:

```text
backend/app/ai/verification_agent.py
```

The Verification Agent evaluates before-and-after repair evidence.

It checks whether the reported issue appears to have been addressed and produces verification information such as confidence and notes.

---

## Incident State Machine

Each incident follows a defined lifecycle.

```text
Reported
   |
   v
Reviewed
   |
   v
Assigned
   |
   v
In Progress
   |
   v
Awaiting Verification
   |
   v
Verified Resolved
```

This separates the maintenance process into clearly defined stages rather than treating an incident as immediately resolved after assignment or repair.

---

## Database

CampusFix AI uses SQLite for the prototype database.

The incident data model includes information such as:

| Field                 | Purpose                                    |
| --------------------- | ------------------------------------------ |
| `id`                  | Unique incident identifier                 |
| `category`            | Maintenance issue category                 |
| `department`          | Responsible maintenance department         |
| `before_image`        | Original issue evidence                    |
| `after_image`         | Repair evidence                            |
| `duplicate_of`        | Reference to a possible duplicate incident |
| `verification_status` | Current repair verification state          |

The database supports incident management, duplicate handling, repair verification, and the incident lifecycle.

---

## Project Architecture

The current shipped frontend uses a Vanilla JavaScript single-page application served through FastAPI.

```text
CampusFix.AI/
|
+-- backend/
|   |
|   +-- app/
|   |   |
|   |   +-- ai/
|   |   |   +-- vision_agent.py
|   |   |   +-- duplicate_agent.py
|   |   |   +-- verification_agent.py
|   |   |
|   |   +-- routers/
|   |   |   +-- incidents.py
|   |   |   +-- maintenance.py
|   |   |   +-- verification.py
|   |   |   +-- analytics.py
|   |   |
|   |   +-- static/
|   |   |   +-- index.html
|   |   |
|   |   +-- config.py
|   |   +-- database.py
|   |   +-- main.py
|   |
|   +-- seed_data.py
|   +-- requirements.txt
|
+-- demo_assets/
|
+-- docs/
|
+-- Dockerfile
+-- Procfile
+-- start.sh
+-- test_api.py
+-- README.md
```

### Frontend Implementation Note

The earlier technical specification describes React 18 and Vite 5 as the frontend architecture.

The current shipped implementation documented here uses Vanilla JavaScript served through FastAPI. This README describes the implementation currently present in the project rather than presenting the earlier frontend specification as an implemented technology.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* SQLite

### AI

* Gemini multimodal vision
* Structured AI responses
* Visual issue analysis
* Duplicate analysis
* Before-and-after repair verification
* Fallback processing

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Lucide Icons

### Development and Deployment

* REST APIs
* Docker
* Procfile-based deployment support
* API testing

---

## API Endpoints

The main API operations include:

| Method | Endpoint                           | Purpose                                 |
| ------ | ---------------------------------- | --------------------------------------- |
| `POST` | `/api/incidents/analyze-single`    | Analyze a single maintenance image      |
| `POST` | `/api/incidents/analyze-room-scan` | Analyze multiple issues in a room image |
| `POST` | `/api/maintenance/assign`          | Assign a maintenance incident           |
| `POST` | `/api/verification/verify-repair`  | Verify repair evidence                  |
| `GET`  | `/api/analytics/dashboard`         | Retrieve dashboard analytics            |

---

## Engineering Challenges and Solutions

### Poor Image Quality

Campus maintenance photographs may have poor lighting, blur, or unclear visual information.

The system can use confidence information and human review for uncertain cases.

```text
Image
  |
  v
AI Analysis
  |
  v
Confidence Evaluation
  |
  +---- High Confidence ----> Continue
  |
  +---- Low Confidence -----> Review
```

### Duplicate Reports

The same maintenance problem can be reported multiple times.

CampusFix AI combines several incident attributes to perform duplicate assessment.

```text
Location
Room
Category
Objects
   |
   v
Similarity Analysis
```

### Repair Verification

A maintenance ticket being marked as completed does not itself provide visual evidence.

CampusFix AI adds an after-repair evidence stage.

```text
Before Evidence
      |
      v
Repair
      |
      v
After Evidence
      |
      v
Verification
```

### Multiple Problems in One Room

A classroom may contain several maintenance issues at the same time.

Room Scan allows the system to analyze multiple visible issues from a single image.

### Zero-Hardware Prototype

The core prototype is software-based and does not require dedicated IoT hardware.

```text
Smartphone / Image
        |
        v
   CampusFix AI
        |
        v
Maintenance Workflow
=======
# 🏛️ CampusFix AI
### Visual Campus Maintenance & Resolution Intelligence System
*"Don't fill a complaint form. Show the problem."*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📌 Executive Summary

Educational institutions manage extensive physical infrastructure—lecture halls, labs, libraries, washrooms, and hostels. Physical maintenance issues (broken ceiling fans, flickering tube lights, water leaks, shattered windows, and damaged desks) occur on a daily basis.

Current complaint portals fail because they rely on manual text descriptions, guess-work categorization, and simple checkboxes for resolution with zero proof.

**CampusFix AI** introduces an **evidence-based visual lifecycle**:
1. **Show the problem**: Students snap a single photo instead of filling out a tedious 10-field form.
2. **AI Vision & Auto-Triage**: Multimodal Vision extracts the affected object, visible damage, safety score, and routes the ticket to the correct department (Electrical, Plumbing, IT, Carpentry, Housekeeping).
3. **Room Scan Mode**: Audits multiple defects in a classroom simultaneously from a single wide photograph.
4. **Duplicate Ticket Fusion**: Automatically detects redundant complaints for the same issue and prompts upvoting instead of queue clutter.
5. **Before/After AI Verification**: Technicians upload an "After" photo of the completed repair. The Vision AI performs comparative visual diffing to verify resolution consistency before the admin signs off.
6. **Campus Digital Twin**: Interactive 2D floor blueprint of Academic Blocks with live pulsing status beacons for rapid dispatch.

---

## 🌟 Hero Features

* 🔍 **Zero-Friction Vision Reporting**: Snap an image or record a voice note; AI automatically determines category, priority, and problem description.
* ⚡ **Room Scan Mode**: One wide photo parses and logs multiple maintenance defects in a single pass.
* ⟷ **Interactive Before/After Slider**: Draggable split-slider and side-by-side view with Defect Delta bounding box overlays to inspect repair quality.
* 🗺️ **Campus Digital Twin**: Real-time floorplan visualization (Block B & Block C) mapping active incidents with color-coded severity beacons.
* 🏷️ **QR Plaque Scanner**: Rapid location binding by scanning classroom doorway plaques or NFC tags.
* 🛡️ **No Phantom Closures**: Eliminates fake closures with automated AI consistency verification between initial defect and final repair photos.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                   STUDENT / STAFF WEB APP              │
│       (Responsive Mobile Web / Desktop Dashboard)       │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    API GATEWAY (FastAPI)               │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
┌─────────────▼───────────────┐ ┌──────────▼───────────────┐
│  ENGINE A: VISUAL PERCEPTION│ │ ENGINE B: WORKFLOW &     │
│  & SCENE INTELLIGENCE       │ │ RESOLUTION VERIFICATION  │
├─────────────────────────────┤ ├──────────────────────────┤
│ • Zero-Shot Defect Parsing  │ │ • Category Auto-Routing  │
│ • Room Scan (Multi-Defect)  │ │ • Similarity Deduplication│
│ • Safety & Hazard Scoring   │ │ • Before/After AI Diff   │
│ • QR Plaque Location Binder │ │ • Digital Twin Telemetry │
└─────────────┬───────────────┘ └──────────┬───────────────┘
              │                            │
┌─────────────▼────────────────────────────▼─────────────┐
│           INCIDENT & RESOLUTION EVIDENCE DATABASE      │
│                     (SQLite / SQLAlchemy)              │
└────────────────────────────────────────────────────────┘
>>>>>>> 415013a (Update logo design, README documentation, and asset packages)
```

---

<<<<<<< HEAD
## Getting Started

### Prerequisites

Install the following:

* Python
* Git

A Gemini API key can be configured when external Gemini-powered analysis is required.

### 1. Clone the Repository

```bash
### Clone the Repository

=======
## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the Repository
>>>>>>> 415013a (Update logo design, README documentation, and asset packages)
```bash
git clone https://github.com/SrinivasaKamathB/CampusFix.AI.git
cd CampusFix.AI
```

<<<<<<< HEAD
### 2. Create a Virtual Environment

#### Windows PowerShell

```powershell
cd backend

python -m venv venv

.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
cd backend

python3 -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create the required environment configuration according to the variables used by the application's configuration module.

If Gemini-powered analysis is enabled, configure the required Gemini API key.

Do not commit API keys, passwords, or other secrets to the repository.

### 5. Start the Application

From the `backend` directory:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Open the Application

Open:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

---

## Demo Workflow

A typical demonstration follows this process:

### Step 1: Report an Issue

Upload a photograph of a campus maintenance problem.

```text
Maintenance Image
       |
       v
   AI Analysis
```

### Step 2: Analyze the Issue

The system extracts structured information from the image.

```text
Image
  |
  +-- Issue
  +-- Category
  +-- Location / Context
  +-- Detected Objects
```

### Step 3: Check for Duplicates

The system evaluates the new incident against existing reports.

```text
New Incident
     |
     v
Duplicate Analysis
     |
     +---- New Incident
     |
     +---- Possible Duplicate
```

### Step 4: Assign Maintenance

The incident is routed to the appropriate department.

```text
Incident
   |
   v
Department
   |
   v
Assignment
```

### Step 5: Repair the Issue

The maintenance team performs the required repair.

### Step 6: Submit After-Repair Evidence

An after-repair photograph is submitted.

```text
Before Image + After Image
            |
            v
       Verification
```

### Step 7: Resolve the Incident

After successful verification, the incident can progress to the verified resolved state.

---

## Example Scenario

Consider a classroom with a broken ceiling fan.

```text
User
 |
 | Uploads Image
 v
Vision Agent
 |
 +-- Category: Maintenance
 +-- Object: Fan
 +-- Location: Classroom
 |
 v
Duplicate Agent
 |
 | Checks Existing Reports
 v
Maintenance Assignment
 |
 v
Repair
 |
 v
After-Repair Image
 |
 v
Verification Agent
 |
 v
Verified Resolved
```

This demonstrates the complete reporting, assignment, repair, evidence, and verification workflow.

---

## Configuration

Application configuration is handled through the backend configuration module.

Configuration areas include:

```text
AI provider settings
Database settings
Application settings
Environment variables
```

Sensitive values should be stored in environment variables and should not be committed to Git.

---

## Testing

API tests are included in:

```text
test_api.py
```

If the repository is configured for Pytest, tests can be executed with:

```bash
pytest
```

Use the project's actual test configuration if it specifies a different test command.

---

## Limitations

CampusFix AI is a prototype and should not be considered a fully autonomous campus maintenance platform.

Current limitations include:

* AI image analysis can produce incorrect interpretations.
* Poor lighting and image quality can affect analysis.
* Duplicate detection is an assessment and cannot guarantee that every duplicate is identified.
* Repair verification should support human review rather than completely replacing responsible personnel.
* Online AI functionality depends on external AI service availability when the external provider is used.
* The current frontend implementation is Vanilla JavaScript rather than React/Vite.
* Production deployment would require additional authentication, authorization, security, monitoring, scalability, and data-management measures.

---

## Future Improvements

Potential future improvements include:

* Mobile-first maintenance reporting
* Role-based authentication
* Technician-specific dashboards
* Maintenance notifications
* Improved image similarity
* Advanced maintenance analytics
* Campus map integration
* Historical maintenance analysis
* Improved offline AI capabilities
* Cloud image storage
* Production-grade authentication and authorization

---

## Project Objectives

CampusFix AI aims to:

1. Simplify the reporting of campus maintenance problems.
2. Convert maintenance photographs into structured incident information.
3. Reduce duplicate maintenance reports.
4. Route incidents to appropriate maintenance departments.
5. Introduce visual evidence into repair verification.
6. Provide a transparent maintenance incident lifecycle.
7. Demonstrate an AI-powered campus maintenance workflow without dedicated hardware.

---

## Technical Foundation

The project architecture is based on a modular FastAPI backend, AI processing agents, a structured incident database, a visual maintenance workflow, and before-and-after repair verification.

The technical specification defines the major concepts around visual analysis, duplicate detection, room scanning, repair verification, incident states, and auditability.

---

## Project Status

CampusFix AI is an academic and portfolio prototype demonstrating an AI-assisted visual campus maintenance workflow.

The system focuses on the complete maintenance lifecycle:

```text
Report
  |
  v
Analyze
  |
  v
Classify
  |
  v
Route
  |
  v
Repair
  |
  v
Verify
  |
  v
Resolve
=======
### 2. Set Up Virtual Environment & Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)
```bash
# If you have a Gemini API key for live multimodal processing:
export GEMINI_API_KEY="your_api_key_here"

# (If no key is provided, CampusFix AI automatically runs with high-fidelity simulated vision models for offline demos)
```

### 4. Run the Application
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser and navigate to:
👉 **`http://localhost:8000`**

---

## 👥 Collaborator Workflow (For Team Members)

To make edits and contribute to the web app:

1. **Clone the repo** onto your machine:
   ```bash
   git clone https://github.com/SrinivasaKamathB/CampusFix.AI.git
   ```
2. **Open in VS Code**:
   ```bash
   code CampusFix.AI
   ```
3. **Run locally** following the Quick Start steps above.
4. **Make changes** to the frontend (`backend/app/static/index.html`) or backend (`backend/app/`).
5. **Commit and push** back to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
   *(Note: Ensure your GitHub account is invited as a Collaborator in repo **Settings → Collaborators**)*.

---

## 📁 Project Directory Structure

```
CampusFix.AI/
├── README.md                      # Project documentation and quickstart
├── start.sh                       # One-click start script
├── backend/
│   ├── Dockerfile                 # Containerized deployment spec
│   ├── Procfile                   # Cloud platform process file
│   ├── requirements.txt           # Python backend dependencies
│   ├── run.sh                     # Launch runner
│   ├── test_api.py                # Automated backend test suite
│   └── app/
│       ├── main.py                # FastAPI endpoints & static routing
│       ├── models.py              # SQLite ORM models
│       ├── schemas.py             # Pydantic validation schemas
│       ├── seed.py                # Campus asset and sample ticket seeder
│       ├── services/
│       │   ├── vision_service.py  # Multimodal defect & verification engine
│       │   └── routing_service.py # Department assignment logic
│       └── static/
│           └── index.html         # Single-page web dashboard & mobile UI
├── demo_assets/                   # Sample defect images and asset SVGs
└── docs/                          # Presentation slides, overview & pitch deck
    ├── CampusFix_AI_Presentation.html
    ├── CampusFix_AI_Project_Overview.md
    └── CampusFix_AI_Judge_Pitch.md
>>>>>>> 415013a (Update logo design, README documentation, and asset packages)
```

---

<<<<<<< HEAD
## License

This project is developed as an academic and portfolio prototype.

A specific open-source license should only be added if the repository is intentionally being released under that license.
=======
## 🌐 Deployment Options

### Render (Recommended Free Cloud Host)
1. Sign up on [Render.com](https://render.com) and create a **New Web Service**.
2. Connect your GitHub repository: `CampusFix.AI`.
3. Configure the service:
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy! Your app will be live at `https://<your-service>.onrender.com`.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
>>>>>>> 415013a (Update logo design, README documentation, and asset packages)
