# app/core/database.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
from app.core.config import settings


def init_db():
    """Inicializa la base de datos y crea la tabla de conversaciones si no existe."""
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    print("✅ Base de datos SQLite inicializada")


def save_message(conversation_id: str, sender: str, message: str):
    """Guarda un mensaje en la base de datos."""
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO conversations (conversation_id, sender, message, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (conversation_id, sender, message, timestamp),
    )
    conn.commit()
    conn.close()


def get_conversation(conversation_id: str) -> List[Dict[str, Any]]:
    """Obtiene todos los mensajes de una conversación específica."""
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, conversation_id, sender, message, timestamp 
        FROM conversations 
        WHERE conversation_id = ? 
        ORDER BY id
        """,
        (conversation_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_conversation_ids() -> List[str]:
    """Obtiene todos los IDs de conversación únicos."""
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT conversation_id FROM conversations")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
