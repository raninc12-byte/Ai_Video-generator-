@echo off
REM AI Video Generator - Direct installation (no venv)

cd /d "%~dp0"

echo Installing dependencies directly...
python -m pip install --upgrade pip

REM Core dependencies
echo.
echo Installing core packages...
python -m pip install python-dotenv requests Pillow numpy opencv-python imageio imageio-ffmpeg

REM PyTorch 
echo.
echo Installing PyTorch (CPU version - smaller, faster)...
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

REM AI models
echo.
echo Installing diffusers and transformers...
python -m pip install diffusers transformers safetensors

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Launching AI Video Generator...
python src/gui_app.py
