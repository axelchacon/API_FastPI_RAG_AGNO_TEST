# app/main.py
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.database import init_db
from app.services.rag_service import initialize_rag_components

# Inicializar componentes
init_db()
initialize_rag_components()

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Incluir rutas
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "RAG API - Desafío Musache", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
