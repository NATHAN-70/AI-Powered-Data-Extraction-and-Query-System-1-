# Deployment Guide

## Local Development

### Option 1: Using run.py (Recommended for local dev)
```bash
python src/run.py
```
This starts both the FastAPI backend (port 8000) and Streamlit frontend (port 8501).

### Option 2: Manual start
**Terminal 1 - Start Backend:**
```bash
cd src
python -m uvicorn main:app --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run src/streamlit_app.py
```

## Docker Deployment (Production)

### Prerequisites
- Docker and Docker Compose installed

### Build and Run
```bash
docker-compose up --build
```

This will start:
- **Milvus** (Vector DB) on port 19530
- **Backend API** on port 8000
- **Streamlit** on port 8501

### Access the Application
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Streamlit Cloud Deployment

If deploying to Streamlit Cloud, you need to:

1. Deploy the FastAPI backend separately (e.g., on Railway, Render, Heroku, or your own server)
2. Set the API_URL environment variable in Streamlit Cloud:
   - Go to your Streamlit app settings
   - Add secret: `API_URL=https://your-backend-domain.com`

3. Or modify `src/streamlit_app.py` API configuration:
```python
API = os.getenv("API_URL", "https://your-backend-domain.com")
```

## Environment Variables

- `API_URL`: Backend API URL (default: `http://localhost:8000`)
- `PYTHONPATH`: Should include the src directory

## Troubleshooting

### "Failed to reach API" Error
This means Streamlit cannot connect to the backend. Check:
1. Is the backend running? Check with: `curl http://localhost:8000/docs`
2. Is the API_URL environment variable set correctly?
3. In Docker, make sure all services are running: `docker-compose ps`
4. Check logs: `docker-compose logs backend`

### Milvus Connection Issues
Ensure Milvus is healthy:
```bash
docker-compose logs milvus
```

And wait for it to be ready (check health check status).
