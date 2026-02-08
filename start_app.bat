@echo off
echo ===================================================
echo   VideoInsight AI - Launcher
echo ===================================================

echo [1/2] Starting Backend Server (Port 8000)...
start "VideoInsight Backend" cmd /k "cd /d "%~dp0" && python backend\main.py"

echo [2/2] Starting Frontend Server (Port 5173)...
cd /d "%~dp0frontend"
start "VideoInsight Frontend" cmd /k "npm run dev -- --host"

echo.
echo ===================================================
echo   Startup initiated!
echo   Please wait a few seconds for servers to load.
echo.
echo   Frontend : http://localhost:5173/
echo   Backend  : http://localhost:8000/docs
echo ===================================================
pause
