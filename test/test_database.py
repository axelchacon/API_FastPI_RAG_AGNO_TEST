# tests/test_database.py
import pytest
import os
import sqlite3
import sys

# Añadir el directorio de la aplicación al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import (
    init_db,
    save_message,
    get_conversation,
    get_all_conversation_ids,
)
import uuid
from datetime import datetime


@pytest.fixture
def test_db():
    """Fixture para crear una base de datos de prueba."""
    test_db_path = "test_conversations.db"

    # Parchear la configuración para usar la DB de prueba
    from app.core.config import settings

    original_url = settings.DATABASE_URL
    settings.DATABASE_URL = f"sqlite:///{os.path.basename(test_db_path)}"

    # Forzar la creación de la tabla
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS conversations")
    conn.commit()
    conn.close()

    yield test_db_path

    # Limpiar después de la prueba
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    # Restaurar configuración original
    settings.DATABASE_URL = original_url


def test_init_db(test_db):
    """Prueba que se inicialice correctamente la base de datos."""
    from app.core.config import settings

    # Forzar reinicio de la base de datos
    init_db()

    # Verificar que la tabla existe
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='conversations'
    """
    )
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "La tabla 'conversations' debería existir"


def test_save_and_get_message(test_db):
    """Prueba guardar y recuperar un mensaje."""
    from app.core.config import settings

    # Inicializar DB
    init_db()

    # Datos de prueba
    conversation_id = str(uuid.uuid4())
    sender = "user"
    message = "Hola, ¿cómo estás?"

    # Guardar mensaje
    save_message(conversation_id, sender, message)

    # Recuperar conversación
    messages = get_conversation(conversation_id)

    assert len(messages) == 1
    assert messages[0]["conversation_id"] == conversation_id
    assert messages[0]["sender"] == sender
    assert messages[0]["message"] == message
    assert "timestamp" in messages[0]


def test_get_all_conversation_ids(test_db):
    """Prueba obtener todos los IDs de conversación."""
    from app.core.config import settings

    # Inicializar DB
    init_db()

    # Guardar algunos mensajes
    conv_id1 = str(uuid.uuid4())
    conv_id2 = str(uuid.uuid4())

    save_message(conv_id1, "user", "Mensaje 1")
    save_message(conv_id2, "user", "Mensaje 2")

    # Obtener IDs
    ids = get_all_conversation_ids()

    assert len(ids) == 2
    assert conv_id1 in ids
    assert conv_id2 in ids
