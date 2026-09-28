import sqlite3
import json
from datetime import datetime
from app.config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Incidents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            department TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            reporter_role TEXT DEFAULT 'Student',
            before_image TEXT,
            after_image TEXT,
            confidence REAL DEFAULT 0.90,
            upvotes INTEGER DEFAULT 1,
            duplicate_of TEXT,
            is_room_scan INTEGER DEFAULT 0,
            verification_status TEXT DEFAULT 'Unverified',
            verification_confidence REAL DEFAULT 0.0,
            verification_notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            resolved_at TEXT
        )
    ''')

    # Audit Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT NOT NULL,
            action TEXT NOT NULL,
            actor TEXT NOT NULL,
            details TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (incident_id) REFERENCES incidents (id)
        )
    ''')

    conn.commit()
    conn.close()

def log_audit(incident_id, action, actor, details=""):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (incident_id, action, actor, details, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (incident_id, action, actor, details, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
