@echo off
REM Start the FastAPI backend and Streamlit frontend from the project root.
cd /d %~dp0
if not exist .venv\Scripts\activate.bat (
  echo .venv is missing or not set up. Run python -m venv .venv and install requirements first.
  exit /b 1
)

call .venv\Scripts\activate.bat
echo Starting Streamlit frontend on port 8501...

echo Setting PYTHONPATH to %%CD%%\src
set PYTHONPATH=%CD%\src
set PATH=%CD%\tesseract_bin;%PATH%
set TESSDATA_PREFIX=%CD%\tessdata

echo Starting FastAPI backend on port 8000...
start "Backend" "" ".venv\Scripts\uvicorn.exe" main:app --host 0.0.0.0 --port 8000 --reload

timeout /t 3 /nobreak >nul

echo Starting Streamlit frontend on port 8501...
start "Streamlit" "" ".venv\Scripts\streamlit.exe" run "src\streamlit_app.py"

echo Started backend and frontend. Open http://localhost:8501 in your browser.
