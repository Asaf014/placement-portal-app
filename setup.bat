@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================
echo  Placement Portal Application Setup
echo ============================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo Checking Redis installation...
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo Warning: Redis is not running. Please start Redis server before running the application.
)

echo.
echo Setting up Backend...
echo.
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt

echo Initializing database...
python init_db.py

echo.
echo Backend setup complete!
echo Admin credentials - Email: admin@placementportal.com, Password: admin123
echo.

cd ..

echo.
echo Setting up Frontend...
echo.
cd frontend

echo Installing frontend dependencies...
call npm install

echo Frontend setup complete!
echo.

cd ..

echo.
echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo To run the application:
echo.
echo 1. Backend Server:
echo    - Open a terminal in the 'backend' folder
echo    - Run: venv\Scripts\activate.bat
echo    - Run: python app.py
echo.
echo 2. Frontend Development Server:
echo    - Open a terminal in the 'frontend' folder
echo    - Run: npm run dev
echo.
echo 3. Celery Worker (for background jobs):
echo    - Open a terminal in the 'backend' folder
echo    - Run: venv\Scripts\activate.bat
echo    - Run: celery -A tasks.celery_tasks worker --loglevel=info
echo.
echo 4. Redis Server:
echo    - Ensure Redis is running on localhost:6379
echo.
echo 5. Make sure to start them in the following order:
echo    - Start Redis
echo    - Start Backend
echo    - Start Celery Worker
echo    - Start Frontend
echo.
echo Access the application at: http://localhost:8080
echo.
pause
