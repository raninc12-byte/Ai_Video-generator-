# VS Code Copilot Instructions - AI Video Generator

This workspace contains a simple GUI application for generating AI videos from text descriptions.

## Project Overview

The AI Video Generator is a Python-based tool that:
1. **Generates AI videos** from text prompts using Stable Diffusion
2. **Provides a simple GUI** with button-click interface (no coding needed)
3. **Auto-saves to Downloads** (Downloads/AI Videos folder)
4. **Runs completely locally** with no cloud costs or API keys

## Key Files

- `ai_video_gui.py` - **Main GUI application** with Stable Diffusion image generation (USE THIS!)
- `ai_video.bat` - **Windows launcher** for AI Video Generator (USE THIS!)
- `src/video_generator.py` - Core Stable Diffusion text-to-video generation engine
- `config/settings.py` - Configuration and constants
- `setup.bat` - Windows setup (run once)
- `video_gen.py` - Simplified version (basic animations only, not AI-generated)

## Quick Start (Windows)

### 1. First Time Only - Run Setup
```bash
setup.bat
```
This creates a virtual environment and downloads the AI models (~4GB, takes 2-3 minutes).

### 2. Generate Continuous 30 FPS Videos
```bash
ai_video.bat
```
A GUI window opens. Type your prompt, click "🚀 GENERATE VIDEO" button.

The app generates **continuous 30 FPS videos directly from text** - not separate images!

Videos automatically appear in: `Downloads/AI Videos/`

## Usage

1. **Type a prompt** describing the video you want
   - Example: "Ocean waves crashing on a beach"
   - Example: "A peaceful forest with sunlight"
   - Example: "Clouds moving across the sky"
   
2. **Select video mode** (Continuous is default!)
   - **🎬 Continuous** - Direct text-to-video, 30 FPS (RECOMMENDED)
   - ✨ Smooth - Interpolated frames (smoother motion)
   - 📸 Regular - Individual AI frames (fastest preview)
   
3. **Click the "🚀 GENERATE VIDEO" button** to generate
   
4. **Wait 5-15 minutes** (Continuous mode generates full video)
   
5. **Open Downloads folder** to find your video!

## Video Generation Modes

### 🎬 Continuous Video (DEFAULT) - NEW!
- Direct text-to-video generation
- **True 30 FPS continuous video**
- No separate image artifacts
- Most realistic and movie-like
- **~1 second of video**
- 5-10 minutes to generate

### ✨ Smooth Flowing Video
- AI-generated keyframes with interpolation
- Smooth transitions between frames
- Natural flowing motion
- ~1.3 seconds of video
- 2-4 minutes to generate

### 📸 Regular Video
- Individual AI-generated frames
- Combined into video
- Slideshow effect
- ~0.3 seconds of video
- 1-3 minutes to generate

## Configuration

Edit `config/settings.py` to change:
- Video width/height
- Frames per second
- GPU settings
- Model choice

## What's the Difference?

**Use `ai_video.bat`** (all modes below available):

### 🎬 Continuous Video (DEFAULT - RECOMMENDED)
- ✅ **Direct text-to-video generation**
- ✅ True 30 FPS continuous video
- ✅ No separate image artifacts
- ✅ Movie-like quality
- ⏱️ Takes 5-10 minutes per video

### ✨ Smooth Flowing Video
- ✅ **Real AI-generated images** from Stable Diffusion
- ✅ Smooth animated transitions
- ✅ NOT just static images stitched together
- ✅ Natural flowing motion (like Sora AI)
- ⏱️ Takes 2-4 minutes per video

### 📸 Regular Video
- ✅ Individual AI-generated frames
- ✅ Fast generation for previews
- ✅ Good for quick testing
- ✗ Slideshow effect (not smooth)
- ⏱️ Takes 1-3 minutes per video

**Always use Continuous mode for best movie-like quality!**

## File Structure

```
AI Video Generator/
├── ai_video_gui.py          # Main GUI application
├── ai_video.bat             # Launcher (click to start)
├── src/
│   ├── video_generator.py   # AI video generation with Stable Diffusion
│   ├── video_generator_simple.py  # Simple animations (backup)
│   └── __init__.py
├── config/
│   └── settings.py          # Configuration
├── logs/                    # Log files
├── setup.bat               # Setup script (Windows)
├── ai_video.bat            # Launch AI video generator (Windows)
└── README.md               # Full documentation
```

## What Changed (April 9, 2026)

Previously, the system was generating simple gradient animations. Now it actually uses **Stable Diffusion AI** to generate real images from your text prompts!

**Before:** Colorful gradient animations (no AI images)  
**Now:** Real AI-generated images from text descriptions (Stable Diffusion)

## No More Needed

- ✗ No TikTok API setup
- ✗ No command line commands
- ✗ No environment variables
- ✗ No complicated workflows
- ✓ Just click and generate!

## Next Steps

1. Run `setup.bat` (one time only)
2. Run `ai_video.bat` to launch the AI video generator
3. Type your prompt (example: "A futuristic city with neon lights")
4. Click "🚀 GENERATE VIDEO"
5. Check Downloads/AI Videos for your AI-generated video!

See README.md for complete documentation and more details.

