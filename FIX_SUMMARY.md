# Quick Fix Summary

## Why the Error Occurred

When you deployed to Streamlit, the backend wasn't running on the same server. The error:
```
Failed to reach API at http://localhost:8000
Connection refused
```

This happens because:
- **Locally**: Backend runs on your machine at `localhost:8000`
- **Deployed**: Streamlit runs on a server but looks for `localhost:8000` (which doesn't exist)

## What I Fixed

### 1. **Updated docker-compose.yml**
   - Added FastAPI backend service
   - Added Streamlit frontend service  
   - Configured networking so Streamlit can reach backend at `http://backend:8000`
   - Services are automatically started together with proper dependencies

### 2. **Created Dockerfile**
   - Builds the backend container with all dependencies
   - Installs Tesseract OCR and other system deps

### 3. **Created Dockerfile.streamlit**
   - Builds the Streamlit frontend container
   - Configures proper port and health checks

### 4. **Created .streamlit/config.toml**
   - Streamlit configuration for Docker deployment

## How to Use Now

### For Local Development:
```bash
python src/run.py
```

### For Docker Deployment (Recommended):
```bash
docker-compose up --build
```

Then access:
- Streamlit: http://localhost:8501
- Backend: http://localhost:8000/docs (API documentation)

## If Deploying to Streamlit Cloud

You'll need to deploy the backend separately. Update the `API_URL` environment variable in Streamlit Cloud settings to point to your backend server.

Or modify `src/streamlit_app.py`:
```python
API = os.getenv("API_URL", "https://your-deployed-backend.com")
```
