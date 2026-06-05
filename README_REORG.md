Project reorganization

This repository has been reorganized to make development easier.

New layout (non-destructive; original files remain at project root):

- src/
  - main.py           # FastAPI app (copy)
  - streamlit_app.py  # Streamlit frontend (clean name)
  - vector_db.py      # Milvus helper with numpy fallback
  - extractor.py      # extraction helpers

- tesseract_bin/      # moved Tesseract executables and runtime DLLs out of the root
- doc/tesseract_html/ # moved Tesseract manual HTML pages out of the root
- start_app.ps1       # updated to set PYTHONPATH to src and launch services
- start_app.bat       # updated batch script

How to run

1. Activate venv and install dependencies if needed:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the app (PowerShell):

```powershell
.\start_app.ps1
```

or (cmd.exe):

```cmd
start_app.bat
```

Notes

- The reorg is non-destructive: original files are still present. The `src/` folder is used by the updated start scripts via `PYTHONPATH` so the application loads the cleaned modules.
- If you prefer a full move (delete originals), I can perform that after you confirm.
