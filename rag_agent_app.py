# rag_agent_app.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from io import BytesIO
import tempfile
import requests
from agno.agent import Agent
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.docx import DocxKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.models.openai import OpenAIChat
from pypdf import PdfReader

load_dotenv()


def ensure_chromadb_collections():
    """Asegura que las colecciones de ChromaDB estén creadas."""
    os.makedirs("tmp/chromadb", exist_ok=True)

    # Crear todas las colecciones requeridas si no existen
    collections = ["documentos", "pdfs", "textos", "docs"]
    for collection in collections:
        db = ChromaDb(
            collection=collection, path="tmp/chromadb", persistent_client=True
        )
        # Hacer un get() o search vacío simplemente para forzar la creación
        try:
            db.search(query="dummy", limit=1)  # Esto asegura que la colección se cree
        except Exception:
            pass  # Si falla, ya se creará al insertar datos
    print("✅ Todas las colecciones han sido inicializadas.")


ensure_chromadb_collections()

app = FastAPI(title="RAG API - Desafío Musache")


def create_knowledge_bases():
    # Usar una única vector_db compartida
    shared_vector_db = ChromaDb(
        collection="documentos", path="tmp/chromadb", persistent_client=True
    )

    pdf_kb = PDFKnowledgeBase(path="tmp/dummy.pdf", vector_db=shared_vector_db)
    txt_kb = TextKnowledgeBase(path="tmp/dummy.txt", vector_db=shared_vector_db)
    doc_kb = DocxKnowledgeBase(path="tmp/dummy.docx", vector_db=shared_vector_db)

    return CombinedKnowledgeBase(
        sources=[pdf_kb, txt_kb, doc_kb], vector_db=shared_vector_db
    )


def create_rag_agent():
    knowledge_base = create_knowledge_bases()
    return Agent(
        name="RAG Agent",
        model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
        knowledge=knowledge_base,
        instructions="Eres un asistente experto en responder preguntas basadas en documentos.",
        markdown=True,
        show_tool_calls=True,
    )


class QueryRequest(BaseModel):
    question: str


@app.post("/rag-query")
async def rag_query(
    question: str = Form(...),
    files: List[UploadFile] = File([]),
    urls: Optional[List[str]] = Form(None),
):
    """Endpoint para cargar documentos y hacer consultas RAG."""
    agent = create_rag_agent()

    for file in files:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Archivo sin nombre.")
        file_bytes = await file.read()
        await process_uploaded_file(file.filename, file_bytes, agent.knowledge)

    if urls:
        for url in urls:
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                filename = url.split("/")[-1].split("?")[0] or "unnamed_file"
                await process_uploaded_file(filename, response.content, agent.knowledge)
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error al descargar {url}: {str(e)}"
                )

    response = agent.run(question)
    return {"answer": response.content, "sender": "assistant"}


async def process_uploaded_file(filename: str, file_bytes: bytes, knowledge_base):
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=get_file_extension(filename)
    ) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    try:
        shared_vector_db = ChromaDb(
            collection="documentos", path="tmp/chromadb", persistent_client=True
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


def get_file_extension(filename: str) -> str:
    if "." in filename:
        return "." + filename.split(".")[-1].lower()
    return ""


@app.get("/")
async def root():
    return {"message": "RAG API - Desafío Musache", "available_agents": ["rag_agent"]}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "collection": "documentos"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("rag_agent_app:app", host="0.0.0.0", port=8001, reload=True)
