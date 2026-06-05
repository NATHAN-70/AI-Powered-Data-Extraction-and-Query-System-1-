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

## Docker deployment

Run the full stack with:
```bash
docker-compose up --build
```

Then access:
- Streamlit frontend: `http://localhost:8501`
- FastAPI backend docs: `http://localhost:8000/docs`

## Streamlit Cloud deployment

This project requires a backend service for `API_URL`. Streamlit Cloud can host the frontend, but the backend must be hosted separately.

### Recommended architecture

1. Deploy the FastAPI backend on a hosting provider such as Render, Railway, or Fly.io.
2. Deploy the Streamlit frontend using Streamlit Cloud.
3. In the Streamlit Cloud app settings, set the environment variable:
   - `API_URL=https://<your-backend-host>/`

### Notes
- Keep `.env` out of GitHub. This repository already ignores `.env`.
- The backend uses your NVIDIA API key and tesseract configuration from `.env`.

## GitHub setup

To add this project to a GitHub repository, run:
```bash
git init
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git add .
git commit -m "Initial project commit"
git push -u origin main
```

If you already have a GitHub repo, replace the URL with your repository URL.

## Important environment variables

- `API_URL` - full URL of the running backend API
- `NVIDIA_API_KEY` - NVIDIA LLM API key
- `NVIDIA_BASE_URL` - NVIDIA API base URL
- `MODEL` - model name (e.g. `meta/llama-3.1-70b-instruct`)
- `TESSERACT_CMD` - optional path to the Tesseract binary
- `TESSDATA_PREFIX` - path to the Tesseract traineddata directory
- `MILVUS_HOST` / `MILVUS_PORT` - Milvus connection settings

## Troubleshooting

If Streamlit reports:
```
Failed to reach API at http://localhost:8000
```
then the backend is not running or the deployed `API_URL` is incorrect.

For Streamlit Cloud, make sure the frontend uses the deployed backend URL rather than `localhost`.
