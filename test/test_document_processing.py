# tests/test_document_processing.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Añadir el directorio de la aplicación al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.document_service import (
    _get_file_extension,
    _process_single_file,
    _process_url,
    process_uploaded_files,
)


def test_get_file_extension():
    """Prueba la función que obtiene extensiones de archivo."""
    assert _get_file_extension("documento.pdf") == ".pdf"
    assert _get_file_extension("archivo.TXT") == ".txt"
    assert _get_file_extension("sin_extension") == ""
    assert _get_file_extension("") == ""
    assert _get_file_extension("multiple.dots.pdf") == ".pdf"


@pytest.mark.asyncio
async def test_process_single_file_pdf():
    """Prueba el procesamiento de un archivo PDF."""
    with patch(
        "app.services.document_service.get_knowledge_base"
    ) as mock_get_kb, patch(
        "app.services.document_service.PDFKnowledgeBase"
    ) as mock_pdf_kb, patch(
        "app.services.document_service.ChromaDb"
    ) as mock_chromadb, patch(
        "app.services.document_service.tempfile.NamedTemporaryFile"
    ) as mock_tempfile, patch(
        "app.services.document_service.os.unlink"
    ) as mock_unlink, patch(
        "app.services.document_service.os.makedirs"
    ):

        # Mocks
        mock_kb = MagicMock()
        mock_get_kb.return_value = mock_kb

        mock_pdf_instance = MagicMock()
        mock_pdf_kb.return_value = mock_pdf_instance

        # Mock del archivo temporal
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test.pdf"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        mock_tempfile.return_value.__exit__.return_value = None

        # Ejecutar la función
        await _process_single_file("test.pdf", b"contenido pdf")

        # Verificar llamadas
        mock_pdf_kb.assert_called_once()
        mock_kb.sources.append.assert_called_once()
        mock_pdf_instance.load.assert_called_once_with(recreate=False)


@pytest.mark.asyncio
async def test_process_url_pdf():
    """Prueba el procesamiento de una URL PDF."""
    with patch(
        "app.services.document_service.get_knowledge_base"
    ) as mock_get_kb, patch(
        "app.services.document_service.PDFUrlKnowledgeBase"
    ) as mock_pdf_url_kb, patch(
        "app.services.document_service.ChromaDb"
    ) as mock_chromadb, patch(
        "app.services.document_service.PDFUrlReader"
    ) as mock_pdf_reader, patch(
        "app.services.document_service.os.makedirs"
    ):

        # Mocks
        mock_kb = MagicMock()
        mock_get_kb.return_value = mock_kb

        mock_pdf_url_instance = MagicMock()
        mock_pdf_url_kb.return_value = mock_pdf_url_instance

        mock_reader_instance = MagicMock()
        mock_pdf_reader.return_value = mock_reader_instance

        # Ejecutar la función (corregida la URL, eliminando espacios)
        await _process_url(
            "https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
        )

        # Verificar llamadas
        mock_pdf_url_kb.assert_called_once()
        mock_kb.sources.append.assert_called_once()
        mock_pdf_url_instance.load.assert_called_once_with(recreate=False)


@pytest.mark.asyncio
async def test_process_uploaded_files():
    """Prueba el procesamiento de archivos subidos."""
    with patch(
        "app.services.document_service._process_single_file"
    ) as mock_process_file, patch(
        "app.services.document_service._process_url"
    ) as mock_process_url:

        # Crear un mock de UploadFile
        mock_file = MagicMock()
        mock_file.filename = "test.pdf"
        mock_file.read = AsyncMock(return_value=b"contenido")

        # Ejecutar con archivos
        await process_uploaded_files([mock_file], [])

        # Verificar llamadas
        mock_process_file.assert_called_once_with("test.pdf", b"contenido")

        # Ejecutar con URLs (corregida la URL, eliminando espacios)
        await process_uploaded_files(
            [], ["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"]
        )

        # Verificar llamadas
        mock_process_url.assert_called_once_with(
            "https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
        )
