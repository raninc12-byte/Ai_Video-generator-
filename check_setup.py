"""
Setup validation script - Checks if all requirements are met
"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} found. Python 3.8+ required.")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✓ FFmpeg is installed")
        return True
    except:
        print("✗ FFmpeg not found. Install with: pip install ffmpeg")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    if env_path.exists():
        print("✓ .env file found")
        return True
    else:
        print("✗ .env file not found. Copy from .env.example: cp .env.example .env")
        return False

def check_cuda():
    """Check if CUDA/GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ GPU found: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("⚠ GPU not found. Will use CPU (slower)")
            return False
    except:
        print("⚠ Could not check GPU. Will use CPU if necessary")
        return False

def check_dependencies():
    """Check required packages"""
    required = [
        "torch",
        "torchvision",
        "diffusers",
        "transformers",
        "moviepy",
        "PIL",
        "numpy",
        "opencv",
        "requests",
        "python-dotenv"
    ]
    
    try:
        import pkg_resources
        installed = {pkg.key for pkg in pkg_resources.working_set}
        
        all_present = True
        for package in required:
            if package.lower() in installed or package.lower().replace("-", "_") in installed:
                print(f"✓ {package} installed")
            else:
                print(f"✗ {package} not installed")
                all_present = False
        
        return all_present
    except:
        print("⚠ Could not check dependencies")
        return False

def main():
    print("\n" + "=" * 60)
    print("AI Video Workflow - Setup Validation")
    print("=" * 60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("GPU/CUDA", check_cuda)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"Error checking {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All checks passed! Ready to generate videos.")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
