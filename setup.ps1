Write-Host ""
Write-Host "============================================"
Write-Host "  Placement Portal Application Setup"
Write-Host "============================================"
Write-Host ""

$scriptLocation = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptLocation

Write-Host "Checking Python installation..."
$pythonInstalled = $null -ne (python --version 2>&1)
if (-not $pythonInstalled) {
    Write-Host "Error: Python is not installed or not in PATH"
    Read-Host "Press any key to continue"
    exit
}

Write-Host "Checking Node.js installation..."
$nodeInstalled = $null -ne (node --version 2>&1)
if (-not $nodeInstalled) {
    Write-Host "Error: Node.js is not installed or not in PATH"
    Read-Host "Press any key to continue"
    exit
}

Write-Host "Checking Redis installation..."
$redisRunning = $null -ne (redis-cli ping 2>&1 | Select-String "PONG")
if (-not $redisRunning) {
    Write-Host "Warning: Redis is not running. Please start Redis server before running the application."
}

Write-Host ""
Write-Host "Setting up Backend..."
Write-Host ""
Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

& ".\venv\Scripts\Activate.ps1"

Write-Host "Installing backend dependencies..."
pip install -r requirements.txt

Write-Host "Initializing database..."
python init_db.py

Write-Host ""
Write-Host "Backend setup complete!"
Write-Host "Admin credentials - Email: admin@placementportal.com, Password: admin123"
Write-Host ""

Set-Location ..

Write-Host ""
Write-Host "Setting up Frontend..."
Write-Host ""
Set-Location frontend

Write-Host "Installing frontend dependencies..."
npm install

Write-Host "Frontend setup complete!"
Write-Host ""

Set-Location ..

Write-Host ""
Write-Host "============================================"
Write-Host "  Setup Complete!"
Write-Host "============================================"
Write-Host ""
Write-Host "To run the application:"
Write-Host ""
Write-Host "1. Backend Server:"
Write-Host "   - Open a terminal in the 'backend' folder"
Write-Host "   - Run: .\venv\Scripts\Activate.ps1"
Write-Host "   - Run: python app.py"
Write-Host ""
Write-Host "2. Frontend Development Server:"
Write-Host "   - Open a terminal in the 'frontend' folder"
Write-Host "   - Run: npm run dev"
Write-Host ""
Write-Host "3. Celery Worker (for background jobs):"
Write-Host "   - Open a terminal in the 'backend' folder (with venv activated)"
Write-Host "   - Run: celery -A tasks.celery_tasks worker --loglevel=info"
Write-Host ""
Write-Host "4. Redis Server:"
Write-Host "   - Ensure Redis is running on localhost:6379"
Write-Host ""
Write-Host "5. Make sure to start them in the following order:"
Write-Host "   - Start Redis"
Write-Host "   - Start Backend"
Write-Host "   - Start Celery Worker"
Write-Host "   - Start Frontend"
Write-Host ""
Write-Host "Access the application at: http://localhost:8080"
Write-Host ""
Read-Host "Press any key to continue"
