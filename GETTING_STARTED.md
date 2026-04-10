# Getting Started Checklist

## 🚀 First Time Setup (5 minutes)

### Step 1: Choose Your Model Type
Pick one:

**Option A: Diffusers (FASTEST - Recommended for Video)**
- [ ] No extra installation needed
- [ ] Downloads ~1GB on first run
- [ ] Takes 5-10 seconds per video frame

**Option B: Ollama (FLEXIBLE - Online LLM)**
- [ ] Download from https://ollama.ai
- [ ] Takes 10-15 minutes to install
- [ ] Can run other AI models too

### Step 2: Run Setup
```bash
setup.bat
```
This creates a Python environment and downloads dependencies.

### Step 3: Generate Your First Video

**Easy Way (Default Diffusers):**
```bash
start.bat
```
Then type a prompt and click the button.

**Choose Your Model First:**
```bash
choose_model.bat
```
Pick Diffusers or Ollama from the menu.

**Advanced (Command Line):**
```bash
python video_gen.py
```

---

## 📋 What You Get

```
Your Video Generator
├── GUI Application (click to generate)
├── Auto-saves videos to Downloads/AI Videos/
├── Sound effects (10 different types)
├── AI-selected background music
├── AI voiceover narration
├── Status bar showing progress
└── Supports multiple AI models
```

---

## 🎯 Quick Tasks

### Generate a Simple Video
1. Click `start.bat`
2. Type: "A beautiful sunset over mountains"
3. Keep default 8 frames
4. Click "GENERATE VIDEO"
5. Check Downloads/AI Videos folder

### Generate a Long Video (Better Quality)
1. Click `start.bat`
2. Type: "A futuristic city with neon lights"
3. Drag slider to 12-15 frames
4. Click "GENERATE VIDEO"
5. Wait 2-5 minutes for rendering

### Add Voiceover/Sound
1. In GUI, check "Generate Voiceover"
2. Select sound effect or "Auto-Select Best"
3. Click "GENERATE VIDEO"
4. Video will include narration + music

### Switch AI Models
1. Run `choose_model.bat`
2. Select Ollama or Diffusers
3. Confirm (auto-configures)
4. Click `start.bat`
5. Videos use your chosen model

### Check Current Settings
```bash
python model_selector.py
```
Shows:
- Current model type
- Available models
- Setup instructions
- Configuration details

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Module not found"** | Run `setup.bat` again |
| **"Slow on first run"** | Model is downloading (~1-5GB), be patient |
| **"Out of VRAM"** | Use smaller model (SSD-1B), reduce frames |
| **"Ollama: connection refused"** | Run `ollama serve` in another terminal |
| **"TTS not working"** | Wait for dialog to close even if silent |
| **"Video file not created"** | Check Downloads/AI Videos folder, check disk space |

---

## 📁 File Structure

```
Ai workflow/
├── start.bat                 ← Click to launch GUI
├── setup.bat                 ← Run once for setup
├── choose_model.bat          ← Select your AI model
├── video_gen.py              ← Standalone app (can run directly)
├── model_selector.py         ← Check/change settings
├── config/
│   └── settings.py           ← Configuration file
├── src/
│   ├── __init__.py
│   └── video_generator.py    ← Core generation engine
├── README.md                 ← Full documentation
├── MODEL_GUIDE.md            ← Model options explained
└── GETTING_STARTED.md        ← This file
```

---

## 💻 Environment Variables (Advanced)

Switch models without launcher:

```bash
# Diffusers (default)
set MODEL_TYPE=diffusers
set TEXT_TO_IMAGE_MODEL=segmind/SSD-1B

# Ollama
set MODEL_TYPE=ollama
set OLLAMA_HOST=http://localhost:11434
set OLLAMA_MODEL=llama2

# Then run
python video_gen.py
```

Or create `.env` file:
```
MODEL_TYPE=diffusers
TEXT_TO_IMAGE_MODEL=segmind/SSD-1B
```

---

## ✨ Features

✅ **GUI Interface** - Click-button video generation  
✅ **AI Image Generation** - Text-to-video via Stable Diffusion  
✅ **Sound Effects** - 10 different background tracks  
✅ **AI Sound Selection** - Engine picks best music for your video  
✅ **Voiceover** - AI reads text descriptions  
✅ **Auto-Save** - Videos go straight to Downloads  
✅ **Status Messages** - Real-time progress updates  
✅ **Multiple Models** - Switch between Diffusers & Ollama  
✅ **No Internet** - Works offline (after initial setup)  
✅ **No API Keys** - Completely local, free  

---

## 🎬 Example Prompts

**Nature:**
- "A peaceful forest with sunlight filtering through trees"
- "Ocean waves crashing on a sandy beach at sunset"
- "Mountains covered in snow with eagles flying"

**Sci-Fi:**
- "A futuristic city with holographic signs and flying cars"
- "A spaceship exploring an alien planet with strange creatures"
- "Robot walking through a neon-lit cyberpunk street"

**Abstract:**
- "Colorful paint swirling in water with geometric patterns"
- "Galaxy spiraling with stars and cosmic dust"
- "Liquid metal flowing and morphing into different shapes"

**Action:**
- "Dragon flying through clouds breathing fire"
- "Explosion with colorful sparks in slow motion"
- "Lightning striking in a dark stormy sky"

---

## 📞 Need Help?

1. **Videos not generating?** → Check `logs/` folder for errors
2. **Model issues?** → Run `python model_selector.py` to check setup
3. **Performance?** → Try smaller model or fewer frames
4. **Ollama won't connect?** → Make sure `ollama serve` is running
5. **Syntax error?** → Wait a minute for Python caches to clear, try again

---

## 🔄 Typical Workflow

```
1. Click start.bat
   ↓
2. Type prompt (e.g., "cats playing in a garden")
   ↓
3. Optionally:
   - Adjust frames (more = better quality, slower)
   - Enable voiceover
   - Select sound effect
   ↓
4. Click "GENERATE VIDEO"
   ↓
5. Wait for progress bar (usually 30 sec - 5 min)
   ↓
6. Open Downloads/AI Videos/
   ↓
7. Watch your video! 🎉
```

That's it! No coding, no complex setup, no API keys. Just click and create.

---

## 🚀 Next Level

Once comfortable, try:
- [ ] Different AI models via `choose_model.bat`
- [ ] Long videos (12+ frames) for cinema-quality
- [ ] Ollama for text generation too
- [ ] Voiceover + custom sound combinations
- [ ] Batch create videos with different prompts
- [ ] Add watermarks or titles via `config/settings.py`

**Happy video creating! 🎬**
