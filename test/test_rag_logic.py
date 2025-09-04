# tests/test_rag_logic.py
import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Añadir el directorio de la aplicación al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.rag_service import (
    ensure_chromadb_collections,
    create_knowledge_bases,
    create_rag_agent,
    query_rag,
    get_knowledge_base,
)
from app.core.config import settings

# Importar las clases reales para los mocks
try:
    from agno.vectordb.base import VectorDb
    from agno.knowledge.pdf import PDFKnowledgeBase
    from agno.knowledge.text import TextKnowledgeBase
    from agno.knowledge.docx import DocxKnowledgeBase
    from agno.knowledge.combined import CombinedKnowledgeBase
except ImportError as e:
    print(f"Warning: No se pudieron importar clases de agno: {e}")

    # Crear clases dummy para los mocks
    class VectorDb:
        pass

    class PDFKnowledgeBase:
        pass

    class TextKnowledgeBase:
        pass

    class DocxKnowledgeBase:
        pass

    class CombinedKnowledgeBase:
        pass


def test_get_knowledge_base():
    """Prueba que se pueda obtener la base de conocimiento."""
    # Reiniciar el estado global
    import app.services.rag_service as rag_service_module

    # Guardar el valor original
    original_kb = rag_service_module.knowledge_base

    # Forzar reinicio para la prueba
    rag_service_module.knowledge_base = None

    kb = get_knowledge_base()
    assert kb is not None
    assert hasattr(kb, "sources")

    # Restaurar el valor original
    rag_service_module.knowledge_base = original_kb


@patch("app.services.rag_service.ChromaDb")
def test_ensure_chromadb_collections(mock_chromadb):
    """Prueba que se creen las colecciones de ChromaDB."""
    # Mock para evitar errores reales
    mock_db_instance = MagicMock()
    # Hacer que el mock se comporte como una instancia de VectorDb
    mock_db_instance.__class__ = VectorDb
    mock_chromadb.return_value = mock_db_instance
    mock_db_instance.search.return_value = None

    # Mock os.makedirs para evitar crear directorios reales
    with patch("app.services.rag_service.os.makedirs"):
        # Ejecutar la función
        ensure_chromadb_collections()

    # Verificar que se llamó con los parámetros correctos
    mock_chromadb.assert_called_with(
        collection=settings.CHROMA_COLLECTION,
        path=settings.CHROMA_PATH,
        persistent_client=True,
    )


@patch("app.services.rag_service.ChromaDb")
@patch("app.services.rag_service.PDFKnowledgeBase")
@patch("app.services.rag_service.TextKnowledgeBase")
@patch("app.services.rag_service.DocxKnowledgeBase")
@patch("app.services.rag_service.CombinedKnowledgeBase")
def test_create_knowledge_bases(
    mock_combined_kb, mock_docx_kb, mock_txt_kb, mock_pdf_kb, mock_chromadb
):
    """Prueba que se cree la base de conocimiento combinada."""
    # Reiniciar el estado global
    import app.services.rag_service as rag_service_module

    original_kb = rag_service_module.knowledge_base
    rag_service_module.knowledge_base = None

    # Crear mocks que se comporten como instancias reales
    mock_vector_db = MagicMock()
    mock_vector_db.__class__ = VectorDb
    mock_chromadb.return_value = mock_vector_db

    mock_pdf_instance = MagicMock()
    mock_pdf_instance.__class__ = PDFKnowledgeBase
    mock_pdf_kb.return_value = mock_pdf_instance

    mock_txt_instance = MagicMock()
    mock_txt_instance.__class__ = TextKnowledgeBase
    mock_txt_kb.return_value = mock_txt_instance

    mock_docx_instance = MagicMock()
    mock_docx_instance.__class__ = DocxKnowledgeBase
    mock_docx_kb.return_value = mock_docx_instance

    mock_combined_instance = MagicMock()
    mock_combined_instance.__class__ = CombinedKnowledgeBase
    mock_combined_kb.return_value = mock_combined_instance

    # Mock os.makedirs
    with patch("app.services.rag_service.os.makedirs"):
        kb = create_knowledge_bases()

        # Verificar que se llamaron las funciones correctamente
        assert kb is not None
        mock_chromadb.assert_called()
        mock_pdf_kb.assert_called()
        mock_txt_kb.assert_called()
        mock_docx_kb.assert_called()
        mock_combined_kb.assert_called()

    # Restaurar el valor original
    rag_service_module.knowledge_base = original_kb


@patch("app.services.rag_service.OpenAIChat")
@patch("app.services.rag_service.Agent")
@patch("app.services.rag_service.ChromaDb")
@patch("app.services.rag_service.PDFKnowledgeBase")
@patch("app.services.rag_service.TextKnowledgeBase")
@patch("app.services.rag_service.DocxKnowledgeBase")
@patch("app.services.rag_service.CombinedKnowledgeBase")
def test_create_rag_agent(
    mock_combined_kb,
    mock_docx_kb,
    mock_txt_kb,
    mock_pdf_kb,
    mock_chromadb,
    mock_agent,
    mock_openai,
):
    """Prueba que se cree el agente RAG."""
    # Reiniciar el estado global
    import app.services.rag_service as rag_service_module

    original_agent = rag_service_module.rag_agent
    original_kb = rag_service_module.knowledge_base
    rag_service_module.rag_agent = None
    rag_service_module.knowledge_base = None

    # Mocks
    mock_model = MagicMock()
    mock_openai.return_value = mock_model

    mock_agent_instance = MagicMock()
    mock_agent.return_value = mock_agent_instance

    # Crear mocks para la base de conocimiento
    mock_vector_db = MagicMock()
    mock_vector_db.__class__ = VectorDb
    mock_chromadb.return_value = mock_vector_db

    mock_pdf_instance = MagicMock()
    mock_pdf_instance.__class__ = PDFKnowledgeBase
    mock_pdf_kb.return_value = mock_pdf_instance

    mock_txt_instance = MagicMock()
    mock_txt_instance.__class__ = TextKnowledgeBase
    mock_txt_kb.return_value = mock_txt_instance

    mock_docx_instance = MagicMock()
    mock_docx_instance.__class__ = DocxKnowledgeBase
    mock_docx_kb.return_value = mock_docx_instance

    mock_combined_instance = MagicMock()
    mock_combined_instance.__class__ = CombinedKnowledgeBase
    mock_combined_kb.return_value = mock_combined_instance

    # Mock os.makedirs
    with patch("app.services.rag_service.os.makedirs"):
        # Ejecutar la función
        agent = create_rag_agent()

        # Verificar llamadas
        mock_openai.assert_called_with(
            id="gpt-4o-mini", api_key=settings.OPENAI_API_KEY
        )
        mock_agent.assert_called()  # Verifica que se llamó al constructor

    # Restaurar los valores originales
    rag_service_module.rag_agent = original_agent
    rag_service_module.knowledge_base = original_kb


def test_query_rag():
    """Prueba la función de consulta al RAG."""
    with patch("app.services.rag_service.rag_agent") as mock_agent:
        # Mock de la respuesta
        mock_response = MagicMock()
        mock_response.content = "Respuesta de prueba"
        mock_agent.run.return_value = mock_response

        result = query_rag("Pregunta de prueba")
        assert result == "Respuesta de prueba"
        mock_agent.run.assert_called_once_with("Pregunta de prueba")
