@echo off
REM SignalHub APIs - Quick Start Script
REM This script helps you start the backend and frontend quickly

echo ========================================
echo SignalHub APIs - Quick Start
echo ========================================
echo.

echo [1/3] Starting Backend API...
echo.
cd C:\dev\signalhub-apis\apps\api
start cmd /k "call venv\Scripts\activate.bat && set PYTHONPATH=C:\dev\signalhub-apis\apps\api;C:\dev\signalhub-apis && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend...
echo.
cd C:\dev\signalhub-apis\apps\web
start cmd /k "npm run dev"

timeout /t 2 /nobreak >nul

echo [3/3] Done!
echo.
echo ========================================
echo Services Started:
echo ========================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3001
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
