@echo off
REM Start Wildlife Detection System

echo ==================================
echo 🦁 Wildlife Detection System
echo ==================================
echo.
echo Starting backend and frontend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.
    pause
    exit /b 1
)

echo 🚀 Starting Flask backend (port 8000)...
start /B python app.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo 🌐 Starting Streamlit frontend (port 8501)...
start /B streamlit run streamlit_app.py

echo.
echo ==================================
echo ✅ System Started!
echo ==================================
echo.
echo 🌐 Streamlit UI:  http://localhost:8501
echo 🔌 Flask API:     http://localhost:8000
echo.
echo Press Ctrl+C to stop both services
echo ==================================
echo.

pause

