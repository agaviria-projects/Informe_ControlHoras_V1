import sqlite3
from pathlib import Path
from datetime import datetime


def get_db_path():
    base_dir = Path(__file__).resolve().parents[2]
    storage_dir = base_dir / "storage"
    storage_dir.mkdir(exist_ok=True)
    return storage_dir / "control_horas_v1.sqlite"


def get_connection():
    return sqlite3.connect(get_db_path())


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            nombre TEXT NOT NULL,
            placa TEXT NOT NULL,
            fecha TEXT NOT NULL,
            kilometro REAL,
            horas_trabajadas REAL,
            valor_hora_extra REAL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            deleted INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
