# Quick Start Guide - AI Video Generator

## 2-Step Setup

### Step 1: Run Setup (4 minutes)

**Windows:**
```cmd
setup.bat
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This creates a virtual environment and installs all dependencies. Your first run will download the AI model (~4GB).

### Step 2: Generate Videos with GUI Button (Click & Wait)

**Windows:**
```cmd
start.bat
```

This opens a simple application with:
- 📝 Text box to describe your video
- 🎚️ Slider to control number of frames
- 🎥 Big button to generate
- 📊 Status updates and logs

**macOS/Linux:**
```bash
source venv/bin/activate
python src/gui_app.py
```

Your videos will be automatically saved to: **`Downloads/AI Videos`**

---

## Tips & Tricks

**Faster Generation:**
- Use fewer frames (try 5-6 instead of 10)
- Shorter prompts sometimes work better

**Better Quality:**
- Use more frames (up to 15)
- Detailed, descriptive prompts
- Be specific about style (e.g., "cinematic", "realistic", "anime")

**Example Prompts:**
- "A futuristic city with neon lights and flying cars"
- "Serene forest waterfall with mist and sunlight"
- "Ocean beach sunset with palm trees and waves"
- "Cyberpunk street market with holographic signs"
- "Magical forest with glowing creatures and flora"

---

## Common Issues

**"Out of memory"?**
→ Use the slider to reduce frames (try 3-5)

**"Model is loading for a long time?"**
→ This is normal on first run (2-3 minutes). It downloads 4GB of model files.

**"Generation is slow"?**
→ Reduce frames or use a simpler prompt
→ The app uses CPU by default (faster setup). Check CUDA if you have an NVIDIA GPU.

**"Can't find start.bat"?**
→ Make sure you're in the right folder: `cd "AI workflow"`

---

## Where Are My Videos?

Videos are automatically saved to:
```
C:\Users\[YourUsername]\Downloads\AI Videos\
```

Just open Windows Explorer and go to Downloads folder!

---

**Happy video creating!** 🎬
