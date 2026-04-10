@echo off
cd /d "%~dp0"

echo Installing minimal dependencies...
python -m pip install Pillow imageio imageio-ffmpeg --quiet 2>nul

echo.
echo Launching AI Video Generator...
echo.

python video_gen.py
