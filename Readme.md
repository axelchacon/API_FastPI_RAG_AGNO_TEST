Bienvenido a `README.md`

Nota:
Como se usó Render gratuito , el endpoint probablemnete no esté operativo luego de su despliegue (Your free instance will spin down with inactivity, which can delay requests by 50 seconds or more.): https://api-fastpi-rag-agno-test.onrender.com/ .
Se usó FastAPI como API, Agno como Framework para crear sistems de IA, ChromaDB como base de datos vectoriales, sqlite3 para almacenar las conversaciones o base de datos, Render para el despliegue y github para integración continua, y Pytest para pruebas unitarias y de intergración. Se obtó por tecnologías gratuitas para este prototipo de API RAG.

Se pudo obtar usar Docling (https://github.com/docling-project/docling) que paresea archivos PDFs, Txt, Docs, Docx y más para transformar a Markdown (De URls a Markdown o Archivos Binarios a Markdown) que luego se pueden almancenr el bases de datos vectoriales y es más entendible para los LLMs ese formato Markdown, pero pesa mucho, por lo que se optó por usar las opciones nativas de Agno que es un framework opensource hecho para crear soluciones poco complejas con IA generativa como sistemas multiagentes simples o asistentes de IA simples. Se pudo obtar por CrewAI que es similar, pero es más usado para soluciones más complejas y requiere mayor comprensión de ciertos temas; se pudo obtar por LangChain y Langraph, pero no Langchain no está hecho para escalar y es inestable. En este caso se obtó por algo que pueda escalar mejor y más simple con versiones estables para escalar.

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

Entiendo que quieres que añada la sección de "response" o respuestas a las pruebas curl que mencioné anteriormente.

Aquí está el contenido actualizado con ejemplos de respuestas:

# 🧪 Ejemplos de Uso del API - Desafío Musache

## 📡 Ejemplos con cURL

### Para archivos locales:

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -H "Content-Type: multipart/form-data" \
     -F "question=¿Cuál es el objetivo del desafío?" \
     -F "files=@/ruta/a/tu/documento.pdf"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG).",
	"sender": "assistant",
	"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

### Para URLs:

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -H "Content-Type: multipart/form-data" \
     -F "question=How to make Thai curry?" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "To make Thai curry, you need to prepare the curry paste first by grinding lemongrass, galangal, and chilies. Then cook with coconut milk and add your choice of protein and vegetables.",
	"sender": "assistant",
	"conversation_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
}
```

### Para múltiples URLs:

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -H "Content-Type: multipart/form-data" \
     -F "question=¿Qué información contienen estos documentos?" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "Los documentos contienen información sobre diferentes aspectos del proyecto. El primer documento describe la arquitectura del sistema, mientras que el segundo presenta los requisitos técnicos y funcionales.",
	"sender": "assistant",
	"conversation_id": "c8b7a6d5-e4f3-2109-8765-432109876543"
}
```

### Para solo hacer una pregunta (sin cargar documentos):

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/rag-query" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "question=¿Cuál es el objetivo del desafío Musache?"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG), y exponerlo como un API web utilizando Python.",
	"sender": "assistant",
	"conversation_id": "d7e6f5c4-b3a2-1098-7654-321098765432"
}
```

### Obtener una conversación específica:

```bash
curl -X GET "http://127.0.0.1:8001/api/v1/conversation/a1b2c3d4-e5f6-7890-1234-567890abcdef"
```

**Ejemplo de respuesta:**

```json
[
	{
		"id": 1,
		"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
		"sender": "user",
		"message": "¿Cuál es el objetivo del desafío?",
		"timestamp": "2025-09-04T10:30:45.123456"
	},
	{
		"id": 2,
		"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
		"sender": "assistant",
		"message": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG).",
		"timestamp": "2025-09-04T10:30:47.654321"
	}
]
```

### Obtener todas las conversaciones:

```bash
curl -X GET "http://127.0.0.1:8001/api/v1/conversations"
```

**Ejemplo de respuesta:**

```json
{
	"conversation_ids": [
		"a1b2c3d4-e5f6-7890-1234-567890abcdef",
		"f0e9d8c7-b6a5-4321-fedc-ba9876543210",
		"c8b7a6d5-e4f3-2109-8765-432109876543"
	]
}
```

### Verificar el estado del servicio:

```bash
curl -X GET "http://127.0.0.1:8001/api/v1/health"
```

**Ejemplo de respuesta:**

```json
{
	"status": "healthy",
	"collection": "documentos",
	"database": "connected"
}
```

## 🖥️ Ejemplos con Postman

### 1. Configuración para cargar archivos locales

**Método:** `POST`  
**URL:** `http://127.0.0.1:8001/api/v1/rag-query`  
**Pestaña Body:**

- Seleccionar `form-data`
- Agregar campos:
  - Key: `question`, Value: `¿Cuál es el objetivo del desafío?`, Type: `Text`
  - Key: `files`, Value: `[Seleccionar archivo]`, Type: `File`

### 2. Configuración para URLs

**Método:** `POST`  
**URL:** `http://127.0.0.1:8001/api/v1/rag-query`  
**Pestaña Body:**

- Seleccionar `form-data`
- Agregar campos:
  - Key: `question`, Value: `How to make Thai curry?`, Type: `Text`
  - Key: `urls`, Value: `https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf`, Type: `Text`

### 3. Configuración para múltiples URLs

**Método:** `POST`  
**URL:** `http://127.0.0.1:8001/api/v1/rag-query`  
**Pestaña Body:**

- Seleccionar `form-data`
- Agregar campos:
  - Key: `question`, Value: `¿Qué información contienen estos documentos?`, Type: `Text`
  - Key: `urls`, Value: `https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf`, Type: `Text`
  - Key: `urls`, Value: `https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf`, Type: `Text`
  - _(Haz clic en "Add" para agregar múltiples campos con la misma key `urls`)_

### 4. Obtener conversaciones

**Método:** `GET`  
**URL:** `http://127.0.0.1:8001/api/v1/conversations`

**Método:** `GET`  
**URL:** `http://127.0.0.1:8001/api/v1/conversation/a1b2c3d4-e5f6-7890-1234-567890abcdef`

## 🎯 Notas importantes:

1. **Content-Type:** Para solicitudes con archivos o URLs, Postman configurará automáticamente el `Content-Type: multipart/form-data`
2. **Espacios:** Asegúrate de no dejar espacios al final de las URLs
3. **Archivos:** Al cargar archivos locales, asegúrate de que la ruta sea correcta y el archivo exista
4. **Respuestas:** Todas las respuestas incluyen un `conversation_id` que puedes usar para consultar el historial de la conversación

## 📋 Ejemplo de respuesta completo:

```json
{
	"answer": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG), y exponerlo como un API web utilizando Python.",
	"sender": "assistant",
	"conversation_id": "694e9653-ffbc-4b29-86dc-1a2094d097a2"
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
    - **Environment**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4.  Agrega la variable de entorno `OPENAI_API_KEY` en la sección de "Environment Variables" de Render.
5.  Render desplegará automáticamente la aplicación.

## ✅ Criterios del Desafío

- **Claridad del código y estructura del API**: Código modular, bien organizado y con nombres descriptivos. API RESTful clara.
- **Eficiencia y relevancia del sistema RAG**: Uso de ChromaDB para recuperación eficiente y modelo OpenAI para generación de respuestas relevantes.
- **Calidad de las pruebas y documentación**: Incluye pruebas unitarias e integración, y este `README.md` detallado.
- **Solidez en decisiones técnicas**: Elección de tecnologías modernas y adecuadas, arquitectura modular, manejo de errores.

---

# 🧪 Pruebas del Proyecto - Desafío Musache

Este proyecto incluye un conjunto completo de pruebas unitarias e integración para garantizar la calidad y el correcto funcionamiento del sistema RAG.

## 📁 Estructura de las Pruebas

```
tests/
├── __init__.py
├── conftest.py                # Puedes añadir fixtures globales aquí si los necesitas
├── test_rag_logic.py          # Pruebas unitarias de la lógica RAG
├── test_document_processing.py # Pruebas unitarias del procesamiento de documentos
├── test_database.py           # Pruebas unitarias de la base de datos SQLite
└── test_api_endpoints.py      # Pruebas de integración de la API
```

# 🧪 Ejecutar las Pruebas

### Requisitos Previos

Asegúrate de tener instaladas las dependencias de prueba:

```bash
pip install pytest pytest-asyncio httpx
```

### Comandos de Ejecución

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar todas las pruebas con salida detallada
pytest -v

# Ejecutar un archivo de prueba específico
pytest tests/test_api_endpoints.py

# Ejecutar pruebas con cobertura (requiere pytest-cov)
pytest --cov=app tests/
```

## 📊 Resultado de las Pruebas

Todas las pruebas pasan exitosamente:

```
=============================================================== test session starts ===============================================================
collected 18 items

test/test_api_endpoints.py::test_health_check PASSED                     [  5%]
test/test_api_endpoints.py::test_root_endpoint PASSED                    [ 11%]
test/test_api_endpoints.py::test_list_conversations_empty PASSED         [ 16%]
test/test_api_endpoints.py::test_get_nonexistent_conversation PASSED     [ 22%]
test/test_api_endpoints.py::test_rag_query_no_files PASSED               [ 27%]
test/test_api_endpoints.py::test_rag_query_with_files PASSED             [ 33%]
test/test_database.py::test_init_db PASSED                               [ 38%]
test/test_database.py::test_save_and_get_message PASSED                  [ 44%]
test/test_database.py::test_get_all_conversation_ids PASSED              [ 50%]
test/test_document_processing.py::test_get_file_extension PASSED         [ 55%]
test/test_document_processing.py::test_process_single_file_pdf PASSED    [ 61%]
test/test_document_processing.py::test_process_url_pdf PASSED            [ 66%]
test/test_document_processing.py::test_process_uploaded_files PASSED     [ 72%]
test/test_rag_logic.py::test_get_knowledge_base PASSED                   [ 77%]
test/test_rag_logic.py::test_ensure_chromadb_collections PASSED          [ 83%]
test/test_rag_logic.py::test_create_knowledge_bases PASSED               [ 88%]
test/test_rag_logic.py::test_create_rag_agent PASSED                     [ 94%]
test/test_rag_logic.py::test_query_rag PASSED                            [100%]

=============================================================== 18 passed in 9.28s ================================================================
```

## 🎯 Cobertura de las Pruebas

### 1. Pruebas de Lógica RAG (`test_rag_logic.py`)

- ✅ `test_get_knowledge_base`: Verifica la obtención de la base de conocimiento
- ✅ `test_ensure_chromadb_collections`: Prueba la creación de colecciones ChromaDB
- ✅ `test_create_knowledge_bases`: Verifica la creación de bases de conocimiento combinadas
- ✅ `test_create_rag_agent`: Prueba la creación del agente RAG
- ✅ `test_query_rag`: Verifica la función de consulta al sistema RAG

### 2. Pruebas de Base de Datos (`test_database.py`)

- ✅ `test_init_db`: Prueba la inicialización de la base de datos SQLite
- ✅ `test_save_and_get_message`: Verifica el guardado y recuperación de mensajes
- ✅ `test_get_all_conversation_ids`: Prueba la obtención de IDs de conversación

### 3. Pruebas de Procesamiento de Documentos (`test_document_processing.py`)

- ✅ `test_get_file_extension`: Verifica la función de obtención de extensiones
- ✅ `test_process_single_file_pdf`: Prueba el procesamiento de archivos PDF locales
- ✅ `test_process_url_pdf`: Verifica el procesamiento de URLs PDF
- ✅ `test_process_uploaded_files`: Prueba el procesamiento de archivos subidos

### 4. Pruebas de API (`test_api_endpoints.py`)

- ✅ `test_health_check`: Verifica el endpoint de salud
- ✅ `test_root_endpoint`: Prueba el endpoint raíz
- ✅ `test_list_conversations_empty`: Verifica listado de conversaciones vacías
- ✅ `test_get_nonexistent_conversation`: Prueba manejo de conversaciones inexistentes
- ✅ `test_rag_query_no_files`: Verifica consulta RAG sin archivos
- ✅ `test_rag_query_with_files`: Prueba consulta RAG con URLs

## 🛠️ Tecnologías de Pruebas

- **pytest**: Framework principal de pruebas
- **pytest-asyncio**: Soporte para pruebas asíncronas
- **httpx**: Cliente HTTP para pruebas de API
- **unittest.mock**: Para mocking de dependencias externas

## 🎯 Criterios del Desafío Cumplidos

- ✅ **Pruebas unitarias**: Cada componente del sistema es probado individualmente
- ✅ **Pruebas de integración**: Verifican el funcionamiento conjunto de la API
- ✅ **Cobertura completa**: Todas las funcionalidades críticas están cubiertas
- ✅ **Uso de mocks**: Se evitan dependencias externas para pruebas aisladas
- ✅ **Manejo de errores**: Se prueban casos de error y respuestas esperadas

Las pruebas garantizan que el sistema cumple con los requisitos del Desafío Musache y mantiene una alta calidad de código.

# Render:

### Pasos Generales para Render:

1.  Crea una cuenta en [Render](https://render.com).
2.  Conecta tu repositorio de GitHub.
3.  Configura el servicio web:
    - **Environment**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4.  Agrega la variable de entorno `OPENAI_API_KEY` en la sección de "Environment Variables" de Render.
5.  Render desplegará automáticamente la aplicación.

## 🧪 Ejemplos de Uso del API - Desafío Musache

Link: https://api-fastpi-rag-agno-test.onrender.com

## 📡 Ejemplos con cURL

### Para archivos locales:

```bash
curl -X POST "https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query" \
     -H "Content-Type: multipart/form-data" \
     -F "question=¿Cuál es el objetivo del desafío?" \
     -F "files=@/ruta/a/tu/documento.pdf"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG).",
	"sender": "assistant",
	"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

### Para URLs:

```bash
curl -X POST "https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query" \
     -H "Content-Type: multipart/form-data" \
     -F "question=How to make Thai curry?" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "To make Thai curry, you need to prepare the curry paste first by grinding lemongrass, galangal, and chilies. Then cook with coconut milk and add your choice of protein and vegetables.",
	"sender": "assistant",
	"conversation_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
}
```

### Para múltiples URLs:

```bash
curl -X POST "https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query" \
     -H "Content-Type: multipart/form-data" \
     -F "question=¿Qué información contienen estos documentos?" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf" \
     -F "urls=https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "Los documentos contienen información sobre diferentes aspectos del proyecto. El primer documento describe la arquitectura del sistema, mientras que el segundo presenta los requisitos técnicos y funcionales.",
	"sender": "assistant",
	"conversation_id": "c8b7a6d5-e4f3-2109-8765-432109876543"
}
```

### Para solo hacer una pregunta (sin cargar documentos):

```bash
curl -X POST "https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "question=¿Cuál es el objetivo del desafío Musache?"
```

**Ejemplo de respuesta:**

```json
{
	"answer": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG), y exponerlo como un API web utilizando Python.",
	"sender": "assistant",
	"conversation_id": "d7e6f5c4-b3a2-1098-7654-321098765432"
}
```

### Obtener una conversación específica:

```bash
curl -X GET "https://api-fastpi-rag-agno-test.onrender.com/api/v1/conversation/a1b2c3d4-e5f6-7890-1234-567890abcdef"
```

**Ejemplo de respuesta:**

```json
[
	{
		"id": 1,
		"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
		"sender": "user",
		"message": "¿Cuál es el objetivo del desafío?",
		"timestamp": "2025-09-04T10:30:45.123456"
	},
	{
		"id": 2,
		"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
		"sender": "assistant",
		"message": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG).",
		"timestamp": "2025-09-04T10:30:47.654321"
	}
]
```

### Obtener todas las conversaciones:

```bash
curl -X GET "https://api-fastpi-rag-agno-test.onrender.com/api/v1/conversations"
```

**Ejemplo de respuesta:**

```json
{
	"conversation_ids": [
		"a1b2c3d4-e5f6-7890-1234-567890abcdef",
		"f0e9d8c7-b6a5-4321-fedc-ba9876543210",
		"c8b7a6d5-e4f3-2109-8765-432109876543"
	]
}
```

### Verificar el estado del servicio:

```bash
curl -X GET "hhttps://api-fastpi-rag-agno-test.onrender.com/api/v1/health"
```

**Ejemplo de respuesta:**

```json
{
	"status": "healthy",
	"collection": "documentos",
	"database": "connected"
}
```

## 🖥️ Ejemplos con Postman

### 1. Configuración para cargar archivos locales

**Método:** `POST`  
**URL:** `https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query`  
**Pestaña Body:**

- Seleccionar `form-data`
- Agregar campos:
  - Key: `question`, Value: `¿Cuál es el objetivo del desafío?`, Type: `Text`
  - Key: `files`, Value: `[Seleccionar archivo]`, Type: `File`

### 2. Configuración para URLs

**Método:** `POST`  
**URL:** `https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query`  
**Pestaña Body:**

- Seleccionar `form-data`
- Agregar campos:
  - Key: `question`, Value: `How to make Thai curry?`, Type: `Text`
  - Key: `urls`, Value: `https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf`, Type: `Text`

### 3. Configuración para múltiples URLs

**Método:** `POST`  
**URL:** `https://api-fastpi-rag-agno-test.onrender.com/api/v1/rag-query`  
**Pestaña Body:**

- Seleccionar `form-data`
- Agregar campos:
  - Key: `question`, Value: `¿Qué información contienen estos documentos?`, Type: `Text`
  - Key: `urls`, Value: `https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf`, Type: `Text`
  - Key: `urls`, Value: `https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf`, Type: `Text`
  - _(Haz clic en "Add" para agregar múltiples campos con la misma key `urls`)_

### 4. Obtener conversaciones

**Método:** `GET`  
**URL:** `https://api-fastpi-rag-agno-test.onrender.com/api/v1/conversations`

**Método:** `GET`  
**URL:** `https://api-fastpi-rag-agno-test.onrender.com/api/v1/conversation/a1b2c3d4-e5f6-7890-1234-567890abcdef`

## 🎯 Notas importantes:

1. **Content-Type:** Para solicitudes con archivos o URLs, Postman configurará automáticamente el `Content-Type: multipart/form-data`
2. **Espacios:** Asegúrate de no dejar espacios al final de las URLs
3. **Archivos:** Al cargar archivos locales, asegúrate de que la ruta sea correcta y el archivo exista
4. **Respuestas:** Todas las respuestas incluyen un `conversation_id` que puedes usar para consultar el historial de la conversación

## 📋 Ejemplo de respuesta completo:

```json
{
	"answer": "El objetivo del desafío Musache es construir un sistema de respuesta a preguntas basado en un documento utilizando la técnica Retrieval-Augmented Generation (RAG), y exponerlo como un API web utilizando Python.",
	"sender": "assistant",
	"conversation_id": "694e9653-ffbc-4b29-86dc-1a2094d097a2"
}
```
