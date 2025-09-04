# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import List, Optional
import uuid
from app.api.models import QueryRequest, QueryResponse, ConversationMessage
from app.services.rag_service import query_rag
from app.services.document_service import process_uploaded_files
from app.core.database import save_message, get_conversation, get_all_conversation_ids

router = APIRouter()


@router.post("/rag-query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def rag_query_endpoint(
    question: str = Form(...),
    files: List[UploadFile] = File([]),
    urls: Optional[List[str]] = Form(None),
):
    """Endpoint para cargar documentos y hacer consultas RAG."""

    # Procesar archivos si se proporcionan
    if files or urls:
        await process_uploaded_files(files, urls)

    # Generar ID de conversación
    conversation_id = str(uuid.uuid4())

    # Guardar pregunta del usuario
    save_message(conversation_id, "user", question)

    # Obtener respuesta del RAG
    answer_text = query_rag(question)

    # Guardar respuesta del asistente
    save_message(conversation_id, "assistant", answer_text)

    return QueryResponse(
        answer=answer_text, sender="assistant", conversation_id=conversation_id
    )


@router.get("/conversation/{conversation_id}", response_model=List[ConversationMessage])
def get_conversation_endpoint(conversation_id: str):
    messages = get_conversation(conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return messages


@router.get("/conversations")
def list_conversations_endpoint():
    conversation_ids = get_all_conversation_ids()
    return {"conversation_ids": conversation_ids}


@router.get("/health")
def health_check():
    return {"status": "healthy", "collection": "documentos", "database": "connected"}
