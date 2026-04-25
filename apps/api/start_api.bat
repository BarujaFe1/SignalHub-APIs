@echo off
cd C:\dev\signalhub-apis\apps\api
call venv\Scripts\activate.bat
set PYTHONPATH=C:\dev\signalhub-apis\apps\api;C:\dev\signalhub-apis
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
