# Multi Source RAG Assistant

This repository contains a Streamlit frontend and a FastAPI backend for a retrieval-augmented generation (RAG) assistant.

## Project structure

- `src/`: application source code
  - `src/main.py` - FastAPI backend
  - `src/streamlit_app.py` - Streamlit frontend
  - `src/extractor.py` - URL/PDF/Image extraction helpers
  - `src/vector_db.py` - Milvus/local vector storage helper
  - `src/rag.py` - NVIDIA LLM API integration
- `docker-compose.yml` - local multi-service deployment including Milvus, backend, and frontend
- `Dockerfile` - backend container build
- `Dockerfile.streamlit` - frontend container build
- `.streamlit/config.toml` - Streamlit configuration
- `.gitignore` - ignored files for GitHub

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (for container deployment)
- Git (for repository management and GitHub push)

## Local development

1. Create and activate the virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Start the app:
   ```powershell
   .\start_app.ps1
   ```
4. Open Streamlit in the browser:
   ```text
   http://localhost:8501
   ```

