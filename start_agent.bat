@echo off
echo ========================================
echo   Starting PC Monitor Agent
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting monitoring agent...
echo Press Ctrl+C to stop
echo.

python agent.py

pause
