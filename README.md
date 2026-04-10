# AI Video Generator - One-Click Video Creation

Generate beautiful AI videos from simple text descriptions. No coding needed. No cloud costs. No TikTok complications.

Just type what you want to see → Press button → Get video!

## Features

✨ **One-Click Video Generation**
- Simple GUI app with button to generate videos
- No command line needed
- Real-time progress updates

🎨 **Multiple AI Models**
- **Stable Diffusion** (Hugging Face Diffusers) - Fast, local, GPU-accelerated
- **Ollama** - Local LLM models, run anything offline
- **Extensible** - Easy to add new model backends

💾 **Auto-Save to Downloads**
- Videos automatically saved to `Downloads/AI Videos`
- Easy access from Windows Explorer
- No setup required

⚡ **Fast & Free**
- Local models (no cloud costs)
- GPU acceleration available
- Works offline once model is downloaded

📝 **Full Control**
- Adjust frames for quality/speed tradeoff
- See detailed generation logs
- Works on Windows, Mac, and Linux

## Model Options

### Stable Diffusion (Default)
**Command:** `python video_gen.py` or set `MODEL_TYPE=diffusers`

Fast text-to-image generation using Hugging Face models:
- `segmind/SSD-1B` (default) - Fast & lightweight (~1GB)
- `stable-diffusion-v1-5` - Standard quality (~4GB)
- `stabilityai/stable-diffusion-2` - High quality (~5GB)

**Requirements:** No additional setup, downloads on first run

### Ollama (Local LLMs)
**Command:** Set `MODEL_TYPE=ollama` or `ollama` as first argument

Run any Ollama model locally without GPU (or with GPU for speed):

**Setup:**
1. Install Ollama: https://ollama.ai
2. Start Ollama: `ollama serve`
3. Pull a model: `ollama pull llava` (for vision tasks) or `ollama pull llama2`
4. Set environment: `set MODEL_TYPE=ollama`
5. Run: `python video_gen.py`

**Available Models:**
- `llava` - Vision model, can analyze images
- `llama2` - General LLM for prompt enhancement
- Any model from https://ollama.ai/library

## Setup Instructions

### Windows
```bash
# First time setup (downloads model ~4GB)
setup.bat

# Run the app
start.bat

# Or use Python directly with Ollama:
set MODEL_TYPE=ollama
python video_gen.py
```

### Linux / Mac
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Diffusers (default)
python video_gen.py

# Or with Ollama
export MODEL_TYPE=ollama
python video_gen.py
```

## Project Structure

```
ai-video-generator/
├── src/
│   ├── video_generator.py      # Core AI video generation
│   │   ├── DiffusersBackend    # Stable Diffusion implementation
│   │   ├── OllamaBackend       # Ollama implementation
│   │   └── ModelFactory        # Model loader
│   ├── gui_app.py              # GUI application
│   └── __init__.py
├── config/
│   └── settings.py             # Configuration & model settings
├── logs/                       # Log files
├── setup.bat                   # Windows setup (run once)
├── start.bat                   # Launch the app (Windows)
├── requirements.txt            # Python packages
└── README.md                   # This file
```

## Configuration

Edit `config/settings.py` to customize:

```python
# Model type: "diffusers" or "ollama"
MODEL_TYPE = "diffusers"

# Diffusers-specific
TEXT_TO_IMAGE_MODEL = "segmind/SSD-1B"

# Ollama-specific
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama2"

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # TikTok format
VIDEO_FPS = 30
```

## Environment Variables

Control settings via environment variables:

```bash
# Switch to Ollama
set MODEL_TYPE=ollama
set OLLAMA_HOST=http://localhost:11434
set OLLAMA_MODEL=llava

# Use different Diffusers model
set TEXT_TO_IMAGE_MODEL=stable-diffusion-v1-5

# Run the app
python video_gen.py
```

## Troubleshooting

**"Failed to download model"**
- Check internet connection
- Ensure 10GB+ free disk space
- Try again - downloads can take 2-5 minutes

**"Failed to connect to Ollama"**
- Make sure Ollama is installed: https://ollama.ai
- Start Ollama: `ollama serve`
- Pull a model: `ollama pull llama2`
- Check connection at http://localhost:11434/api/tags

**GPU not detected**
- Install NVIDIA CUDA Toolkit
- Install cuDNN
- Ensure torch was installed with GPU support
- Check: `python -c "import torch; print(torch.cuda.is_available())"`

## Adding Custom Models

To add a new model backend, create a class in `src/video_generator.py`:

```python
class CustomBackend:
    def __init__(self, model_name, host):
        self.model_name = model_name
        self.load_model()
    
    def load_model(self):
        # Initialize your model here
        pass
    
    def generate_image(self, prompt):
        # Generate image from prompt
        # Return PIL Image
        return image
```

Then update `ModelFactory`:

```python
elif model_type == "custom":
    return CustomBackend(MODEL_NAME, HOST)
```

## License

MIT License - Free for personal and commercial use

## Prerequisites

- **Python 3.8+**
- **NVIDIA GPU** (recommended for faster generation, CPU fallback available)
- **FFmpeg** (for video processing)
- **TikTok Developer Account** (for API credentials)

### System Requirements

- **Storage**: 10GB+ free space (for models and videos)
- **RAM**: 8GB minimum (16GB+ recommended)
- **GPU**: RTX 3060+ recommended (or comparable)

## Installation

### For Windows Users (Easiest):

1. **Download or extract this folder**

2. **Run setup (one-time, ~4 minutes):**
   ```cmd
   setup.bat
   ```
   This downloads the AI model and installs Python packages.

3. **Launch the app:**
   ```cmd
   start.bat
   ```

That's it! Wait for the GUI window to appear.

### For Mac/Linux Users:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/gui_app.py
```

## Usage

### Option 1: GUI Application (Easiest) ⭐

1. Click `start.bat` (Windows) or run `python src/gui_app.py` (Mac/Linux)
2. Type your video description in the text box
3. Adjust the frame slider if you want (default is fine)
4. Click the big **"🎥 GENERATE VIDEO"** button
5. Wait for generation (show progress in real-time)
6. Videos appear automatically in `Downloads/AI Videos`

### Example Prompts

Here are some ideas to get started:

- "A futuristic city with neon lights and flying cars at night"
- "Serene forest waterfall with mist and golden sunlight"
- "Ocean beach at sunset with palm trees and crashing waves"
- "Cyberpunk street market with holograms and crowds"
- "Magical forest with glowing mushrooms and flying creatures"
- "Northern lights (aurora) dancing over snowy mountains"
- "Underwater coral reef with colorful tropical fish"
- "Cozy cabin in the snow during a winter storm"

## Configuration

Customize behavior by editing `config/settings.py`:

```python
VIDEO_WIDTH = 1080        # Video width (portrait)
VIDEO_HEIGHT = 1920       # Video height
VIDEO_FPS = 30            # Frames per second
VIDEO_DURATION = 15       # Total seconds
USE_GPU = True            # Enable GPU (NVIDIA CUDA)
```

## Where Are My Videos?

Videos are automatically saved to:

**Windows:**
```
C:\Users\[YourUsername]\Downloads\AI Videos\
```

Just open Windows Explorer and navigate to Downloads!

**Mac/Linux:**
```
~/Downloads/AI Videos/
```

## Troubleshooting

### "Out of memory" error

→ Reduce the number of frames using the slider (try 3-5 instead of 10)

### Model takes forever to download

→ This is normal on first run (~4GB download, 2-3 minutes). It only happens once.
→ Make sure you have stable internet connection.

### Generation is very slow

→ Reduce the number of frames
→ Use a simpler, shorter prompt
→ Try with fewer words

### GUI doesn't open

→ Make sure you ran `setup.bat` successfully
→ Try opening a terminal and running: `.\venv\Scripts\python.exe src/gui_app.py`

### Still having issues?

→ Check the log files in the `logs/` folder for detailed error messages
→ Try running `python check_setup.py` to validate your installation

## File Locations

- **Generated Videos**: `C:\Users\[YOU]\Downloads\AI Videos\` (Windows)
- **Log Files**: `logs/` folder in the project
- **Configuration**: `config/settings.py`

## Performance Tips

1. **Faster generation**: Reduce frame count (3-5 frames)
2. **Better quality**: Increase frame count (12-15 frames)
3. **Better prompts**: Be descriptive and specific
   - Good: "A serene Japanese temple in autumn with falling leaves and mist"
   - Okay: "A temple"

## Requirements

- **Python 3.8+** (recommended: Python 3.10 or 3.11)
- **Windows, Mac, or Linux**
- **Storage**: 10GB free (for model files)
- **RAM**: 8GB minimum (16GB+ recommended)
- **CPU**: Any processor (GPU optional but faster)

## Specifications

- **Video Format**: MP4 (H.264 codec)
- **Resolution**: 1920x1080 (portrait, mobile-friendly)
- **Default Duration**: 15 seconds
- **Frame Rate**: 30 FPS

## Limitations

- Videos generated without audio (can add later in video editor)
- First run downloads ~4GB model file
- Requires internet for model download (then works offline)
- Generation time: 5-15 minutes depending on frame count

## Future Enhancements

- [ ] Add background music/sound effects
- [ ] Web-based interface (no installation needed)
- [ ] More model options for different styles
- [ ] Video editing (cuts, transitions, effects)
- [ ] Export to multiple formats
- [ ] Scheduled generation
- [ ] Cloud model options (fast generation)

## License

MIT License - Free to use for personal or commercial projects.

## Safety Notes

⚠️ **Important**:

1. **First-time setup downloads 4GB** - Be patient
2. **Videos are generated locally** - No data sent to cloud
3. **Free to use** - No API costs or subscriptions
4. **Use responsibly** - Generated videos should be used ethically

## Support

If something isn't working:

1. Check the `logs/` folder for error messages
2. Try reducing the number of frames
3. Make sure you have enough disk space
4. Try a different, simpler prompt

For more help, see QUICKSTART.md or README.md details above.
#   A i _ V i d e o - g e n e r a t o r -  
 