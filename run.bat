@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ============================================
echo  Placement Portal - Multiple Services
echo ============================================
echo.
echo This script will help you start all services.
echo.
echo Select what to run:
echo 1. Backend Server Only
echo 2. Frontend Server Only
echo 3. Celery Worker Only
echo 4. Redis Check
echo 5. Full Setup Instructions
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    cd backend
    call venv\Scripts\activate.bat
    echo Starting Backend Server on http://localhost:5000
    python app.py
) else if "%choice%"=="2" (
    cd frontend
    echo Starting Frontend Server on http://localhost:8080
    npm run dev
) else if "%choice%"=="3" (
    cd backend
    call venv\Scripts\activate.bat
    echo Starting Celery Worker
    celery -A tasks.celery_tasks worker --loglevel=info
) else if "%choice%"=="4" (
    echo Checking Redis connection...
    redis-cli ping
    if errorlevel 1 (
        echo Error: Redis is not running
        echo Start Redis with: redis-server
    )
) else if "%choice%"=="5" (
    echo.
    echo ============================================
    echo  Full Setup Instructions
    echo ============================================
    echo.
    echo 1. Start Redis Server (in a new terminal):
    echo    redis-server
    echo.
    echo 2. Start Backend Server (in a new terminal):
    echo    cd backend
    echo    venv\Scripts\activate.bat
    echo    python app.py
    echo.
    echo 3. Start Celery Worker (in a new terminal):
    echo    cd backend
    echo    venv\Scripts\activate.bat
    echo    celery -A tasks.celery_tasks worker --loglevel=info
    echo.
    echo 4. Start Frontend Server (in a new terminal):
    echo    cd frontend
    echo    npm run dev
    echo.
    echo 5. Access application:
    echo    http://localhost:8080
    echo.
    echo 6. Admin Login:
    echo    Email: admin@placementportal.com
    echo    Password: admin123
    echo.
) else (
    echo Invalid choice!
)

pause
