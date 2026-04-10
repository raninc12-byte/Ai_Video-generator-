#!/usr/bin/env python
"""
Build AI Video Generator as a standalone .exe executable
Run this script to create the .exe file
"""

import subprocess
import sys
import shutil
from pathlib import Path

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("="*60)
    print("Building AI Video Generator .exe")
    print("="*60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Build command
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create single .exe file
        "--windowed",  # No console window
        "--name", "AIVideoGenerator",
        "--add-data", "src:src",  # Include src folder
        "--add-data", "config:config",  # Include config folder
        "--add-data", "logs:logs",  # Include logs folder
        "--collect-all", "tkinter",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=diffusers",
        "--hidden-import=transformers",
        "--hidden-import=torch",
        "--paths", ".",
        "ai_video_gui.py"
    ]
    
    # Add icon only if it exists
    if Path("icon.ico").exists():
        build_cmd.insert(5, "--icon")
        build_cmd.insert(6, "icon.ico")
    
    print("\nBuilding executable...")
    print(f"Command: {' '.join(build_cmd)}")
    print()
    
    try:
        result = subprocess.run(build_cmd, check=False)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✅ BUILD SUCCESSFUL!")
            print("="*60)
            print("\nExecutable created: dist/AIVideoGenerator.exe")
            print("\nNext steps:")
            print("1. Run: dist/AIVideoGenerator.exe")
            print("2. The application will launch")
            print("\nNote: First run may be slow as it loads AI models (~4GB)")
            return True
        else:
            print("\n" + "="*60)
            print("❌ BUILD FAILED")
            print("="*60)
            print("\nTroubleshooting:")
            print("1. Ensure all dependencies are installed")
            print("2. Check that all required files exist")
            print("3. Review the error messages above")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during build: {e}")
        return False

def create_batch_launcher():
    """Create a batch file launcher"""
    
    batch_content = """@echo off
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
"""
    
    with open("run_app.bat", "w") as f:
        f.write(batch_content)
    
    print("✅ Created run_app.bat launcher")

if __name__ == "__main__":
    success = build_exe()
    if success:
        create_batch_launcher()
        print("\n✅ All done! You can now use:")
        print("   - dist/AIVideoGenerator.exe (direct executable)")
        print("   - run_app.bat (batch launcher)")
    else:
        print("\n❌ Build failed. Please check errors above.")
        sys.exit(1)
