@echo off
echo ================================================
echo Starting Studdy Buddy AI Application
echo ================================================
echo.
echo This will open 2 terminal windows:
echo   1. Backend Server (Port 8000)
echo   2. Frontend Server (Port 8080)
echo.
echo After both servers start, open your browser to:
echo   http://localhost:8080
echo.
echo Press any key to start...
pause >nul

echo.
echo Starting Backend Server...
start "Studdy Buddy - Backend" cmd /k "cd /d "%~dp0" && uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Studdy Buddy - Frontend" cmd /k "cd /d "%~dp0frontend" && echo Frontend URL: http://localhost:8080 && echo. && python -m http.server 8080"

echo.
echo ================================================
echo Both servers are starting!
echo ================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Open http://localhost:8080 in your browser
echo.
pause
