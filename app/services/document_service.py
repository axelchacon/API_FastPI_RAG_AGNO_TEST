# app/services/document_service.py
import tempfile
import os
import requests
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.docx import DocxKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase, PDFUrlReader  # ✅ Correcto
from app.services.rag_service import get_knowledge_base
from app.core.config import settings


async def process_uploaded_files(files: List[UploadFile], urls: Optional[List[str]]):
    """Procesa archivos subidos y URLs."""
    # Procesar archivos locales
    for file in files:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Archivo sin nombre.")
        file_bytes = await file.read()
        await _process_single_file(file.filename, file_bytes)

    # Procesar URLs
    if urls:
        for url in urls:
            try:
                await _process_url(url)
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error al procesar URL {url}: {str(e)}"
                )


async def _process_single_file(filename: str, file_bytes: bytes):
    """Procesa un solo archivo local."""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=_get_file_extension(filename)
    ) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    try:
        # Obtener la base de conocimiento correctamente
        knowledge_base = get_knowledge_base()

        shared_vector_db = ChromaDb(
            collection=settings.CHROMA_COLLECTION,
            path=settings.CHROMA_PATH,
            persistent_client=True,
        )

        if filename.lower().endswith(".pdf"):
            pdf_kb = PDFKnowledgeBase(path=tmp_path, vector_db=shared_vector_db)
            knowledge_base.sources.append(pdf_kb)
            pdf_kb.load(recreate=False)
        elif filename.lower().endswith((".txt", ".md")):
            txt_kb = TextKnowledgeBase(path=tmp_path, vector_db=shared_vector_db)
            knowledge_base.sources.append(txt_kb)
            txt_kb.load(recreate=False)
        elif filename.lower().endswith((".docx", ".doc")):
            doc_kb = DocxKnowledgeBase(path=tmp_path, vector_db=shared_vector_db)
            knowledge_base.sources.append(doc_kb)
            doc_kb.load(recreate=False)
    finally:
        os.unlink(tmp_path)


async def _process_url(url: str):
    """Procesa una URL de documento."""
    # Obtener la base de conocimiento correctamente
    knowledge_base = get_knowledge_base()

    shared_vector_db = ChromaDb(
        collection=settings.CHROMA_COLLECTION,
        path=settings.CHROMA_PATH,
        persistent_client=True,
    )
    # Determinar el tipo de archivo por la extensión de la URL
    url_lower = url.lower().strip()

    if url_lower.endswith(".pdf"):
        # Usar PDFUrlKnowledgeBase para URLs PDF
        pdf_url_kb = PDFUrlKnowledgeBase(
            urls=[url], vector_db=shared_vector_db, reader=PDFUrlReader(chunk=True)
        )
        knowledge_base.sources.append(pdf_url_kb)
        pdf_url_kb.load(recreate=False)
    elif url_lower.endswith((".txt", ".md")):
        # Para URLs de texto, podrías implementar TextUrlKnowledgeBase si está disponible
        # O descargar y procesar como archivo local
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            content = response.text

            # Crear archivo temporal con el contenido
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".txt"
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name

            # Procesar como archivo local
            txt_kb = TextKnowledgeBase(path=tmp_path, vector_db=shared_vector_db)
            knowledge_base.sources.append(txt_kb)
            txt_kb.load(recreate=False)

            # Limpiar archivo temporal
            os.unlink(tmp_path)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al procesar URL de texto {url}: {str(e)}",
            )
    elif url_lower.endswith((".docx", ".doc")):
        # Para URLs de DOCX, descargar y procesar como archivo local
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Crear archivo temporal con el contenido
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name

            # Procesar como archivo local
            doc_kb = DocxKnowledgeBase(path=tmp_path, vector_db=shared_vector_db)
            knowledge_base.sources.append(doc_kb)
            doc_kb.load(recreate=False)

            # Limpiar archivo temporal
            os.unlink(tmp_path)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al procesar URL de documento {url}: {str(e)}",
            )
    else:
        raise HTTPException(
            status_code=400, detail=f"Formato de URL no soportado: {url}"
        )


def _get_file_extension(filename: str) -> str:
    """Obtiene la extensión de un archivo."""
    if "." in filename:
        return "." + filename.split(".")[-1].lower()
    return ""
