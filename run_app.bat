@echo off
REM AI Video Generator Executable Launcher
echo.
echo ===============================================
echo   AI Video Generator
echo   Starting application...
echo ===============================================
echo.

REM Check if .exe exists
if not exist "dist/AIVideoGenerator.exe" (
    echo Error: AIVideoGenerator.exe not found
    echo Please run build_executable.py first
    pause
    exit /b 1
)

REM Launch the executable
start "" "dist/AIVideoGenerator.exe"
