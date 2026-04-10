# 🎬 AI Video Generator - Build .EXE Guide

## Quick Start

### Method 1: Using Pre-built Executable (Easiest)
If you have an `AIVideoGenerator.exe` file:
1. Double-click `AIVideoGenerator.exe`
2. GUI opens
3. Choose RED (Smooth) or GREEN (Quick)
4. Type your prompt
5. Click GENERATE
6. Your video appears in `Downloads/AI Videos/`

### Method 2: Build Your Own Executable

#### Step 1: Install Build Tools
```bash
install_build_tools.bat
```
This installs PyInstaller (needed to create .exe)

#### Step 2: Build the Executable
```bash
python build_executable.py
```
This creates: `dist/AIVideoGenerator.exe`

The build takes 2-5 minutes and downloads packages as needed.

#### Step 3: Run Your Executable
Option A - Direct run:
```bash
dist/AIVideoGenerator.exe
```

Option B - Use the launcher:
```bash
run_app.bat
```

---

## What Is Happening During Build?

PyInstaller packages your Python application with:
- All Python dependencies
- UI framework (tkinter)
- AI libraries (torch, diffusers)
- Required config files
- Log directories

Result: A standalone .exe that doesn't require Python to be installed on the user's computer!

---

## Troubleshooting Build

**"PyInstaller not found"**
- Run: `install_build_tools.bat`

**"Build takes too long"**
- This is normal! First build takes 3-5 minutes
- Subsequent builds are faster

**"dist/AIVideoGenerator.exe is very large"**
- Normal! (~1-2 GB due to AI models included)
- This includes all dependencies

**"Error during build"**
- Check you have Windows 7 or newer
- Ensure you have 5GB+ free disk space
- Run as administrator if needed

---

## After Building

You can:
1. **Distribute the .exe** - Share it with others who don't have Python installed
2. **Create shortcuts** - Right-click executable → Send To → Desktop
3. **Run it anywhere** - Works on any Windows computer

---

## Log Files

When you run the application (Python or .exe), logs are saved:
```
logs/ai_video_YYYYMMDD_HHMMSS.log
```

These contain:
- Generation start/end times
- Model load times
- Total generation duration
- Any errors encountered

---

## File Structure After Build

```
project/
├── ai_video_gui.py (main app)
├── build_executable.py (build script)
├── install_build_tools.bat
├── run_app.bat (launcher)
├── dist/
│   └── AIVideoGenerator.exe ← Use this!
├── build/ (temporary files)
└── src/, config/, logs/ (support files)
```

---

## Running as .EXE vs Python

| Feature | Python | .EXE |
|---------|--------|------|
| Requires Python | ✅ Yes | ❌ No |
| File size | Small | Large (~1-2GB) |
| Speed | Fast startup | Slightly slower startup |
| Features | All | All |
| Logs | Saved | Saved |
| Customization | Easy | Harder |

---

## First Time Running App

Whether Python or .EXE:
1. **Initialize (2-3 min):** App downloads AI models (~4GB)
2. **Load (1-2 min):** Models load into memory
3. **Generate (2-4 min):** Video is generated
4. **Play:** Video appears in Downloads/AI Videos/

**Total first time: 5-10 minutes**
Subsequent runs: 2-4 minutes per video

---

## Advanced: Customize the Build

Edit `build_executable.py` to:
- Change executable name: `--name "MyVideoApp"`
- Add your own icon: `--icon "myicon.ico"`
- Different output location: `--distpath "output_folder"`
- Single folder instead of file: Remove `--onefile`

---

## Questions?

Check the logs in `logs/` folder for detailed information about what's happening.

All generation details are logged with timestamps!
