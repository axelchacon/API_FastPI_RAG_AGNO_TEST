# app/services/rag_service.py
import os
from agno.agent import Agent
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.docx import DocxKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.models.openai import OpenAIChat
from app.core.config import settings

# Variables globales para el agente y la base de conocimiento
rag_agent = None
knowledge_base = None


def ensure_chromadb_collections():
    """Asegura que las colecciones de ChromaDB estén creadas."""
    os.makedirs(settings.CHROMA_PATH, exist_ok=True)

    collections = [settings.CHROMA_COLLECTION]
    for collection in collections:
        db = ChromaDb(
            collection=collection, path=settings.CHROMA_PATH, persistent_client=True
        )
        try:
            db.search(query="dummy", limit=1)
        except Exception:
            pass
    print("✅ Todas las colecciones han sido inicializadas.")


def create_knowledge_bases():
    """Crea las bases de conocimiento combinadas."""
    global knowledge_base

    shared_vector_db = ChromaDb(
        collection=settings.CHROMA_COLLECTION,
        path=settings.CHROMA_PATH,
        persistent_client=True,
    )

    # Crear bases de conocimiento vacías que se cargarán dinámicamente
    pdf_kb = PDFKnowledgeBase(path="tmp/dummy.pdf", vector_db=shared_vector_db)
    txt_kb = TextKnowledgeBase(path="tmp/dummy.txt", vector_db=shared_vector_db)
    doc_kb = DocxKnowledgeBase(path="tmp/dummy.docx", vector_db=shared_vector_db)

    knowledge_base = CombinedKnowledgeBase(
        sources=[pdf_kb, txt_kb, doc_kb], vector_db=shared_vector_db
    )
    return knowledge_base


def create_rag_agent():
    """Crea el agente RAG."""
    global rag_agent, knowledge_base

    if knowledge_base is None:
        knowledge_base = create_knowledge_bases()

    rag_agent = Agent(
        name="RAG Agent",
        model=OpenAIChat(id="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
        knowledge=knowledge_base,
        instructions="Eres un asistente experto en responder preguntas basadas en documentos.",
        markdown=True,
        show_tool_calls=True,
    )
    return rag_agent


def initialize_rag_components():
    """Inicializa todos los componentes RAG necesarios."""
    ensure_chromadb_collections()
    create_knowledge_bases()
    create_rag_agent()


def get_knowledge_base():
    """Obtiene la base de conocimiento, inicializándola si es necesario."""
    global knowledge_base
    if knowledge_base is None:
        knowledge_base = create_knowledge_bases()
    return knowledge_base


def query_rag(question: str) -> str:
    """Realiza una consulta al agente RAG."""
    global rag_agent

    if rag_agent is None:
        create_rag_agent()

    response = rag_agent.run(question)
    return response.content
