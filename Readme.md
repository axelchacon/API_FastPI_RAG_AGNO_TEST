Okay, here is a comprehensive `README.md` for your scalable RAG API project, tailored to the "Desafío Musache" requirements.

---

# RAG API - Desafío Musache

Este proyecto implementa un sistema de **Retrieval-Augmented Generation (RAG)** para responder preguntas basadas en documentos. Expone una API RESTful usando FastAPI.

## 🎯 Objetivo

Construir un sistema que procese documentos (PDF, TXT, DOCX) y responda preguntas sobre su contenido mediante una API web, siguiendo buenas prácticas de desarrollo modular, escalable y testeable.

## 📁 Estructura del Proyecto

La aplicación está organizada de forma modular para facilitar el mantenimiento y la escalabilidad:

```
rag_musache_project/
├── app/                     # Código fuente principal de la aplicación
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── api/                 # Definición de endpoints y modelos Pydantic
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── core/                # Configuración y lógica central (DB, settings)
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── services/            # Lógica de negocio (RAG, procesamiento de archivos)
│   │   ├── __init__.py
│   │   ├── rag_service.py
│   │   └── document_service.py
│   └── utils/               # Funciones auxiliares
│       ├── __init__.py
│       └── helpers.py
├── tests/                   # Pruebas unitarias e integración
│   ├── __init__.py
│   ├── test_rag_logic.py
│   └── test_api_endpoints.py
├── tmp/                     # Directorio temporal para ChromaDB y archivos dummy
├── conversations.db         # Base de datos SQLite para almacenar conversaciones (Opcional 1)
├── requirements.txt         # Dependencias del proyecto
├── .env.example             # Ejemplo de archivo de variables de entorno
├── .gitignore               # Archivos y directorios ignorados por Git
└── README.md                # Este archivo
```

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone <TU_URL_DE_GITHUB>
cd rag_musache_project
```

### 2. Crear un Entorno Virtual (Recomendado)

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Copia el archivo de ejemplo y configura tu clave de API:

```bash
cp .env.example .env
```

Edita `.env` y agrega tu clave de OpenAI:

```env
CEREBRAS_API_KEY=
GROQ_API_KEY=
OPENAI_API_KEY=tu_clave_api_aqui
```

### 5. Ejecutar la Aplicación

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

La API estará disponible en `http://localhost:8001`. La documentación interactiva de la API se puede encontrar en `http://localhost:8001/docs`.

## 🧪 Pruebas

El proyecto incluye pruebas unitarias y de integración.

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con más detalles
pytest -v

# Ejecutar un archivo específico
pytest tests/test_api_endpoints.py
```

## 📦 Endpoints de la API

### Link : `http://127.0.0.1:8001/api/v1`

### `POST /api/v1/rag-query`

Realiza una consulta basada en documentos cargados.

- **Form Data:**
  - `question` (string, requerido): La pregunta a responder.
  - `files` (array of UploadFile, opcional): Archivos PDF, TXT o DOCX para procesar.
  - `urls` (array of strings, opcional): URLs de documentos PDF, TXT o DOCX para descargar y procesar.
- **Respuesta:**
  ```json
  {
  	"answer": "Respuesta generada por el modelo.",
  	"sender": "assistant",
  	"conversation_id": "uuid-único-para-esta-interacción"
  }
  ```

### Para archivos locales:

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -F "question=¿Cuál es el objetivo del desafío?" \
     -F "files=@/ruta/a/tu/documento.pdf"
```

### Para URLs:

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -F "question="How to make Thai curry?" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
```

### Para múltiples URLs:

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -F "question=¿Cuál es el objetivo del desafío?" \
     -F "urls=https://example.com/documento1.pdf" \
     -F "urls=https://example.com/documento2.txt"
```

### `GET /api/v1/conversation/{conversation_id}`

Obtiene el historial de mensajes de una conversación específica.

- **Respuesta:**
  ```json
  [
  	{
  		"id": 1,
  		"conversation_id": "uuid-único-para-esta-interacción",
  		"sender": "user",
  		"message": "¿Cuál es el objetivo del desafío?",
  		"timestamp": "2023-10-27T10:00:00.123456"
  	},
  	{
  		"id": 2,
  		"conversation_id": "uuid-único-para-esta-interacción",
  		"sender": "assistant",
  		"message": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas...",
  		"timestamp": "2023-10-27T10:00:02.654321"
  	}
  ]
  ```

### `GET /api/v1/conversations`

Lista todos los IDs de conversación almacenados.

- **Respuesta:**
  ```json
  {
  	"conversation_ids": ["uuid-único-1", "uuid-único-2"]
  }
  ```

### `GET /api/v1/health`

Verifica el estado de salud del servicio.

- **Respuesta:**
  ```json
  {
  	"status": "healthy",
  	"collection": "documentos",
  	"database": "connected"
  }
  ```

### `GET /`

Endpoint raíz con información básica.

- **Respuesta:**
  ```json
  {
  	"message": "RAG API - Desafío Musache",
  	"docs": "/docs"
  }
  ```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **FastAPI**: Framework web para construir APIs.
- **OpenAI API (gpt-4o-mini)**: Modelo de lenguaje para generación.
- **ChromaDB**: Base de datos vectorial para recuperación de información.
- **SQLite**: Base de datos relacional para almacenar conversaciones (Opcional 1).
- **Pydantic**: Validación de datos y manejo de configuraciones.
- **Pytest**: Framework para pruebas.
- **python-dotenv**: Carga variables de entorno desde `.env`.

## 📝 Decisiones Técnicas

- **Elección de Framework**: Se seleccionó **FastAPI** por su alta performance, fácil generación de documentación automática (Swagger/OpenAPI) y tipado estático con Pydantic, lo que mejora la mantenibilidad.
- **Elección de Modelo**: Se utilizó **gpt-4o-mini** por su balance entre costo, velocidad y calidad para tareas de comprensión y generación de lenguaje.
- **Formatos de Documento**: El sistema soporta **PDF, TXT y DOCX**. Esta flexibilidad permite procesar una amplia gama de documentos comunes.
- **Arquitectura Modular**: Se implementó una estructura de paquetes para separar claramente la lógica de negocio (servicios), la API (rutas y modelos) y la configuración (core), facilitando el mantenimiento y la escalabilidad futura.
- **Almacenamiento de Conversaciones (Opcional 1)**: Se implementó el almacenamiento en **SQLite** para registrar preguntas y respuestas. Esto permite auditoría, análisis futuro o incluso implementar contexto en conversaciones más complejas.

## 🌐 Despliegue (Opcional 2)

Este proyecto está listo para ser desplegado en plataformas como Render.

### Pasos Generales para Render:

1.  Crea una cuenta en [Render](https://render.com).
2.  Conecta tu repositorio de GitHub.
3.  Configura el servicio web:
    - **Environment**: Python
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4.  Agrega la variable de entorno `OPENAI_API_KEY` en la sección de "Environment Variables" de Render.
5.  Render desplegará automáticamente la aplicación.

_(Nota: Asegúrate de tener un archivo `render.yaml` o configurar correctamente los comandos de construcción e inicio en la interfaz de Render)._

## ✅ Criterios del Desafío

- **Claridad del código y estructura del API**: Código modular, bien organizado y con nombres descriptivos. API RESTful clara.
- **Eficiencia y relevancia del sistema RAG**: Uso de ChromaDB para recuperación eficiente y modelo OpenAI para generación de respuestas relevantes.
- **Calidad de las pruebas y documentación**: Incluye pruebas unitarias e integración, y este `README.md` detallado.
- **Solidez en decisiones técnicas**: Elección de tecnologías modernas y adecuadas, arquitectura modular, manejo de errores.

---
