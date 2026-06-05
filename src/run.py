import subprocess
import sys
import time
import os

def run():
    # Determine binary paths inside the virtual environment
    venv_dir = os.path.join(os.path.dirname(__file__), ".venv")
    if os.name == "nt":
        uvicorn_exe = os.path.join(venv_dir, "Scripts", "uvicorn.exe")
        streamlit_exe = os.path.join(venv_dir, "Scripts", "streamlit.exe")
    else:
        uvicorn_exe = os.path.join(venv_dir, "bin", "uvicorn")
        streamlit_exe = os.path.join(venv_dir, "bin", "streamlit")

    # Check if virtual environment binaries exist
    if not os.path.exists(uvicorn_exe) or not os.path.exists(streamlit_exe):
        print("Error: Virtual environment binaries not found. Please ensure the .venv folder is correctly setup.")
        sys.exit(1)

    print("Starting FastAPI backend on port 8000 (with --reload)...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "src")
    backend = subprocess.Popen([uvicorn_exe, "main:app", "--port", "8000", "--reload"], env=env)

    # Wait for the backend to initialize
    time.sleep(2)

    print("Starting Streamlit frontend on port 8501...")
    frontend = subprocess.Popen([streamlit_exe, "run", "src\\streamlit_app.py"], env=env)

    try:
        # Keep the runner script alive to monitor the sub-processes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down both servers...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Servers successfully stopped.")

if __name__ == "__main__":
    run()
