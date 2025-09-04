# tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir el directorio de la aplicación al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
import json

# Crear cliente de prueba
client = TestClient(app)


def test_health_check():
    """Prueba el endpoint de salud."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "collection" in data
    assert "database" in data


def test_root_endpoint():
    """Prueba el endpoint raíz."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_list_conversations_empty():
    """Prueba que la lista de conversaciones esté vacía inicialmente."""
    with patch("app.api.routes.get_all_conversation_ids") as mock_get_ids:
        mock_get_ids.return_value = []

        response = client.get("/api/v1/conversations")
        assert response.status_code == 200
        data = response.json()
        assert "conversation_ids" in data
        assert data["conversation_ids"] == []


def test_get_nonexistent_conversation():
    """Prueba obtener una conversación que no existe."""
    with patch("app.api.routes.get_conversation") as mock_get_conv:
        mock_get_conv.return_value = []

        response = client.get(
            "/api/v1/conversation/694e9653-ffbc-4b29-86dc-1a2094d097a2"
        )
        assert response.status_code == 404


def test_rag_query_no_files():
    """Prueba el endpoint RAG sin archivos."""
    with patch("app.api.routes.query_rag") as mock_query, patch(
        "app.api.routes.save_message"
    ) as mock_save:

        # Mock de la respuesta
        mock_query.return_value = "Esta es una respuesta de prueba"

        # Datos de la solicitud
        response = client.post(
            "/api/v1/rag-query", data={"question": "¿Cuál es el objetivo del desafío?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sender" in data
        assert "conversation_id" in data
        assert data["answer"] == "Esta es una respuesta de prueba"
        assert data["sender"] == "assistant"

        # Verificar que se llamaron las funciones de guardado
        assert mock_save.call_count == 2  # Una para user, una para assistant


@patch("app.api.routes.process_uploaded_files")
@patch("app.api.routes.query_rag")
@patch("app.api.routes.save_message")
def test_rag_query_with_files(mock_save, mock_query, mock_process):
    """Prueba el endpoint RAG con archivos."""
    # Mock de la respuesta
    mock_query.return_value = "Respuesta procesada"

    # Simular que no hay errores en el procesamiento
    mock_process.return_value = None

    # Datos de la solicitud con archivos (simulados) - corregida la URL
    response = client.post(
        "/api/v1/rag-query",
        data={
            "question": "How to make Thai curry?",
            "urls": [
                "https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
            ],  # Sin espacios al final
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Respuesta procesada"
    assert data["sender"] == "assistant"
