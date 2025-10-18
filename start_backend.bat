@echo off
echo Starting Studdy Buddy AI Backend...
echo =====================================
cd /d "%~dp0"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
