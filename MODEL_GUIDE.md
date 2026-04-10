# Model Selection Guide

## Quick Start

### Option 1: Use Default (Fastest)
```bash
python video_gen.py
```
This uses Stable Diffusion with the SSD-1B model (~1GB, very fast).

### Option 2: Interactive Model Selector
```bash
python model_selector.py
```
Shows available models and instructions.

### Option 3: Batch Script (Windows)
```bash
choose_model.bat
```
Interactive menu to pick your model.

---

## Model Types Explained

### 🎨 Diffusers (Stable Diffusion) - **RECOMMENDED FOR VIDEOS**

**What it is:** Text-to-image AI that converts descriptions directly into images.

**Pros:**
- ✅ Generates actual images from text
- ✅ Very fast (5-10 seconds per frame)
- ✅ GPU acceleration available
- ✅ Multiple quality/speed options
- ✅ Best for video generation

**Cons:**
- Requires ~1-5GB download (one-time)
- Needs GPU for reasonable speed

**Setup:**
```bash
set MODEL_TYPE=diffusers
set TEXT_TO_IMAGE_MODEL=segmind/SSD-1B
python video_gen.py
```

**Available Models:**
- `segmind/SSD-1B` (default) - Fast (~1GB, ~5sec per frame)
- `stable-diffusion-v1-5` - Better quality (~4GB, ~15sec per frame)
- `stabilityai/stable-diffusion-2` - Best quality (~5GB, ~20sec per frame)

---

### 🦙 Ollama - **FLEXIBLE, OFFLINE, ANY MODEL**

**What it is:** Local LLM (large language model) server that can run models like:
- llava (vision understanding)
- llama2 (text generation & analysis)
- mistral (fast LLM)
- And hundreds more!

**Pros:**
- ✅ Runs completely offline (no internet after setup)
- ✅ Can use Ollama for many tasks (not just video)
- ✅ CPU-only option available
- ✅ Quick model switching
- ✅ Privacy-focused

**Cons:**
- CPU-only is slow (use with GPU)
- Currently used for prompt enhancement, not image generation
- Requires Ollama installation & setup

**Setup:**
1. Install Ollama: https://ollama.ai
2. Start Ollama in terminal:
   ```bash
   ollama serve
   ```
3. In another terminal, pull a model:
   ```bash
   ollama pull llama2    # For text/prompt enhancement
   ollama pull llava     # For vision understanding
   ```
4. Run AI Video Generator:
   ```bash
   set MODEL_TYPE=ollama
   python video_gen.py
   ```

---

## Which Should I Use?

| Use Case | Recommendation |
|----------|-----------------|
| **First time setup** | Diffusers (segmind/SSD-1B) |
| **Fastest generation** | Diffusers SSD-1B |
| **Best visual quality** | Diffusers SD v2 |
| **CPU only** | Ollama with llama2 |
| **Offline (no internet)** | Ollama (after initial setup) |
| **Prompt enhancement** | Ollama llama2 |
| **Image understanding** | Ollama llava |
| **Running anything locally** | Ollama (flexible) |

---

## Switching Models at Runtime

### Using Environment Variables

```bash
# Windows
set MODEL_TYPE=diffusers
set TEXT_TO_IMAGE_MODEL=segmind/SSD-1B
python video_gen.py

# Or Ollama
set MODEL_TYPE=ollama
set OLLAMA_MODEL=llama2
python video_gen.py
```

### Using .env File

Create `.env` in project root:
```
MODEL_TYPE=diffusers
TEXT_TO_IMAGE_MODEL=segmind/SSD-1B
```

Then run:
```bash
python video_gen.py
```

### Using Python Code

```python
from src.video_generator import VideoGenerator

# Use Diffusers
gen = VideoGenerator(model_type="diffusers")

# Or use Ollama
gen = VideoGenerator(model_type="ollama")
```

---

## Troubleshooting

### "Failed to download model"
- Check internet connection
- Ensure 10GB+ free disk space
- Try again (downloads can pause/resume)

### "Failed to connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check http://localhost:11434/api/tags is accessible
- Verify firewall isn't blocking port 11434

### "GPU not detected with Diffusers"
```bash
# Check GPU status
python -c "import torch; print(torch.cuda.is_available())"

# Install GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### "Ollama is slow"
- Ollama runs on CPU by default
- Install GPU support: https://ollama.ai
- Or use Diffusers for faster generation

---

## Adding Custom Models

Want to use a different model backend? Create a class in `src/video_generator.py`:

```python
class MyCustomBackend:
    def __init__(self, model_name, host):
        self.model_name = model_name
        self.load_model()
    
    def load_model(self):
        # Load your model
        pass
    
    def generate_image(self, prompt):
        # Generate image from prompt
        # Must return PIL Image
        return image
```

Update `ModelFactory.create_model()`:
```python
elif model_type == "custom":
    return MyCustomBackend("mymodel", host)
```

---

## Performance Tips

1. **Use segmind/SSD-1B for speed** - Fastest Diffusers model (~5sec frame)
2. **Enable GPU** - 10-20x faster than CPU
3. **Reduce frames** - 3-5 frames = fast preview, 10+ = better quality
4. **Batch processing** - Generate multiple videos in sequence
5. **Use Ollama for text** - Fast text enhancement without AI image gen

---

## Resources

- **Stable Diffusion Models:** https://huggingface.co/models?task=text-to-image
- **Ollama Library:** https://ollama.ai/library
- **CUDA Setup:** https://pytorch.org/get-started/locally/
- **Ollama GPU Support:** https://github.com/jmorganca/ollama/blob/main/docs/gpu.md
