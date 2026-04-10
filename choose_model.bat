@echo off
REM AI Video Generator - Model Selector
REM Quick setup for different AI models
echo.
echo ====================================================
echo   AI Video Generator - Model Selector
echo ====================================================
echo.
echo Select your preferred model:
echo.
echo   1. Stable Diffusion (Recommended - Default)
echo   2. Ollama (Local LLM)
echo   3. Show Model Info
echo   4. Cancel
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting with Stable Diffusion...
    set MODEL_TYPE=diffusers
    python video_gen.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting with Ollama...
    echo Make sure Ollama is running: ollama serve
    echo.
    set MODEL_TYPE=ollama
    python video_gen.py
    pause
) else if "%choice%"=="3" (
    python model_selector.py
) else (
    echo Cancelled.
)
