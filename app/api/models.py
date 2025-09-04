# app/api/models.py
from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sender: str
    conversation_id: str

class ConversationMessage(BaseModel):
    id: int
    conversation_id: str
    sender: str
    message: str
    timestamp: Optional[str] = None