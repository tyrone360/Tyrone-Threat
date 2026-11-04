import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent.parent / "threat.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                hostname TEXT,
                risk_score INTEGER,
                risk_level TEXT,
                findings TEXT,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_scan(result):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO scan_history (
                url, hostname, risk_score,
                risk_level, findings, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            result.get("url", ""),
            result.get("hostname", ""),
            result.get("risk_score", 0),
            result.get("risk_level", "Unknown"),
            json.dumps(result.get("findings", [])),
            datetime.now(timezone.utc).isoformat()
        ))


def get_recent_scans(limit=10):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, url, hostname, risk_score,
                   risk_level, findings, created_at
            FROM scan_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    scans = []

    for row in rows:
        scan = dict(row)
        scan["findings"] = json.loads(scan["findings"] or "[]")
        scans.append(scan)

    return scans


def get_monitoring_metrics():
    with get_connection() as connection:

        row = connection.execute("""
            SELECT
                COUNT(*) AS total_scans,

                SUM(
                    CASE WHEN LOWER(risk_level) = 'low'
                    THEN 1 ELSE 0 END
                ) AS low_risk,

                SUM(
                    CASE WHEN LOWER(risk_level) = 'medium'
                    THEN 1 ELSE 0 END
                ) AS medium_risk,

                SUM(
                    CASE WHEN LOWER(risk_level) = 'high'
                    THEN 1 ELSE 0 END
                ) AS high_risk

            FROM scan_history
        """).fetchone()

    return {
        "total_scans": row["total_scans"] or 0,
        "low_risk": row["low_risk"] or 0,
        "medium_risk": row["medium_risk"] or 0,
        "high_risk": row["high_risk"] or 0
    }


# ==========================================
# USER ACCOUNT MANAGEMENT
# ==========================================

def create_user(full_name, email, password_hash):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO users (
                full_name, email, password_hash, created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            full_name,
            email,
            password_hash,
            datetime.now(timezone.utc).isoformat()
        ))

        return cursor.lastrowid


def get_user_by_email(email):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT id, full_name, email, password_hash
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

    return dict(row) if row else None


def get_user_by_id(user_id):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT id, full_name, email, created_at
            FROM users
            WHERE id = ?
        """, (user_id,)).fetchone()

    return dict(row) if row else None
