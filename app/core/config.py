# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "RAG API - Desafío Musache"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL: str = "sqlite:///./conversations.db"
    CHROMA_PATH: str = "tmp/chromadb"
    CHROMA_COLLECTION: str = "documentos"


settings = Settings()
