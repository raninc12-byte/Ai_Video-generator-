@echo off
REM AI Video Workflow - Setup Script for Windows

echo.
echo ====================================
echo AI Video Workflow - Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    exit /b 1
)

echo.
echo Installing dependencies - this may take several minutes...
echo.

REM Install dependencies using venv Python
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To use this project, run:
echo   .\venv\Scripts\python.exe src/workflow.py generate "Your prompt here"
echo.
echo Or use the helper script:
echo   python run.py generate "Your prompt here"
echo.
