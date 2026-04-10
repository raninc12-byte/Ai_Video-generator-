@echo off
REM AI Video Generator - Launches the Stable Diffusion-powered GUI

echo.
echo ====================================
echo   AI Video Generator
echo   Creating videos from text...
echo ====================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Run the AI video generator
python ai_video_gui.py

pause
