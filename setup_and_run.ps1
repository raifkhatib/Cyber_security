Write-Host "SecureVault setup starting..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing dependencies..."
python -m pip install -r requirements.txt

Write-Host "Running tests..."
python -m pytest

Write-Host "Starting SecureVault at http://127.0.0.1:5000"
python run.py