@echo off
REM Quick installer for dependencies needed to build .exe
REM Run this first before building the executable

echo.
echo ===============================================
echo   AI Video Generator - Build Dependencies
echo   Installing PyInstaller...
echo ===============================================
echo.

python -m pip install PyInstaller --upgrade

if %errorlevel% equ 0 (
    echo.
    echo ✅ Installation successful!
    echo.
    echo Next steps:
    echo 1. Run: build_executable.py
    echo 2. This will create dist/AIVideoGenerator.exe
    echo.
) else (
    echo.
    echo ❌ Installation failed
    echo Please ensure Python is installed and in PATH
    echo.
)

pause
