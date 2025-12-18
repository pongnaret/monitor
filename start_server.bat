@echo off
echo ========================================
echo   Starting PC Monitor Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create database if not exists
if not exist monitor.db (
    echo Creating database...
    python database.py
)

echo Starting server at http://localhost:8000
echo Press Ctrl+C to stop
echo.

python server.py

pause
