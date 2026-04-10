#!/usr/bin/env python
"""
Helper script to run workflow commands using the virtual environment
Usage: python run.py generate "Your prompt"
"""
import subprocess
import sys
import os
from pathlib import Path

def get_venv_python():
    """Get the path to Python in the virtual environment"""
    if sys.platform == "win32":
        venv_python = Path("venv") / "Scripts" / "python.exe"
    else:
        venv_python = Path("venv") / "bin" / "python"
    
    if not venv_python.exists():
        print(f"Error: Virtual environment not found at {venv_python}")
        print("Run setup.bat (Windows) or create venv manually first")
        return None
    
    return str(venv_python.absolute())

def main():
    """Run the workflow command"""
    venv_python = get_venv_python()
    if not venv_python:
        sys.exit(1)
    
    # Build the command: python venv_path src/workflow.py [args]
    cmd = [venv_python, "src/workflow.py"] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
