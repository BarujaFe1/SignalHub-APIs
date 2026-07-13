@echo off
setlocal
REM SignalHub APIs - Quick Start (Windows)
REM Run from the repository root.

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"

echo ========================================
echo SignalHub APIs - Quick Start
echo ========================================
echo.
echo Repo: %ROOT%
echo.

if not exist "%ROOT%\apps\api\.venv\Scripts\activate.bat" (
  echo [setup] Creating Python venv...
  python -m venv "%ROOT%\apps\api\.venv"
  call "%ROOT%\apps\api\.venv\Scripts\activate.bat"
  pip install -r "%ROOT%\apps\api\requirements.txt"
) else (
  call "%ROOT%\apps\api\.venv\Scripts\activate.bat"
)

set "PYTHONPATH=%ROOT%\apps\api;%ROOT%"

echo [1/4] Ensuring database schema (Alembic)...
pushd "%ROOT%\apps\api"
alembic upgrade head 2>nul
if errorlevel 1 (
  echo Alembic migrate skipped or failed — seed will create tables if needed.
)
echo [2/4] Seeding sources (idempotent)...
python "%ROOT%\scripts\seed.py"
popd

echo [3/4] Starting Backend API on :8000...
start "SignalHub API" cmd /k "cd /d "%ROOT%\apps\api" && call .venv\Scripts\activate.bat && set PYTHONPATH=%ROOT%\apps\api;%ROOT% && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [4/4] Starting Frontend on :3000...
if not exist "%ROOT%\apps\web\node_modules" (
  pushd "%ROOT%\apps\web"
  call npm install
  popd
)
start "SignalHub Web" cmd /k "cd /d "%ROOT%\apps\web" && npm run dev"

echo.
echo ========================================
echo Services:
echo   API:      http://localhost:8000
echo   Swagger:  http://localhost:8000/docs
echo   Frontend: http://localhost:3000
echo ========================================
echo.
echo Tip: open the Sources page and click "Run now" to ingest live data.
pause
