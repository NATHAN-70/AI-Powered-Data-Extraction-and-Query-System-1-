# Start the FastAPI backend and Streamlit frontend from the project root.
# Run this from PowerShell in the project folder.

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectRoot

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Error ".venv is missing or not set up. Run `python -m venv .venv` and install requirements first."
    exit 1
}

Write-Host "Activating virtual environment..."
. .venv\Scripts\Activate.ps1

Write-Host "Setting PYTHONPATH to src and starting FastAPI backend on port 8000..."
$env:PYTHONPATH = "$projectRoot\\src"
$env:PATH = "$projectRoot\\tesseract_bin;$env:PATH"
$env:TESSDATA_PREFIX = "$projectRoot\\tessdata"

# Start Uvicorn and keep a process handle so we can wait for readiness
$uvArgs = "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
$uvProcess = Start-Process -NoNewWindow -PassThru -FilePath "$projectRoot\\.venv\\Scripts\\uvicorn.exe" -ArgumentList $uvArgs

# Wait up to $maxWait seconds for the backend to respond on /docs
$maxWait = 60
$elapsed = 0
$ready = $false
Write-Host "Waiting for backend to become available at http://localhost:8000/docs ..."
while (-not $ready -and $elapsed -lt $maxWait) {
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing -TimeoutSec 5
        if ($resp.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {
        # ignore and retry
    }
    Start-Sleep -Seconds 1
    $elapsed += 1
    Write-Host "Waiting... ${elapsed}s"
}
if (-not $ready) {
    Write-Warning "Backend did not become ready within $maxWait seconds. Starting Streamlit anyway."
} else {
    Write-Host "Backend ready after ${elapsed}s."
}

Write-Host "Starting Streamlit frontend on port 8501..."
Start-Process -NoNewWindow -FilePath "$projectRoot\\.venv\\Scripts\\streamlit.exe" -ArgumentList "run", "src\\streamlit_app.py"

Write-Host "Started backend and frontend. Open http://localhost:8501 in your browser."
