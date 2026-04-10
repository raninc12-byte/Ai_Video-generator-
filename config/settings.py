"""
Configuration settings for AI Video Workflow
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
LOG_DIR = BASE_DIR / "logs"

# Save videos to Downloads folder
DOWNLOADS_DIR = Path.home() / "Downloads"
OUTPUT_DIR = DOWNLOADS_DIR / "AI Videos"

# Ensure output and log directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Video Generation Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # TikTok vertical video format
VIDEO_FPS = 30 # frames per second
VIDEO_DURATION = 30  # seconds (TikTok standard)

# AI Model Settings
# MODEL_TYPE options: "diffusers", "ollama", "local_llm"
MODEL_TYPE = os.getenv("MODEL_TYPE", "diffusers")

# Text-to-Image Model Configuration
TEXT_TO_IMAGE_MODEL = os.getenv("TEXT_TO_IMAGE_MODEL", "segmind/SSD-1B")

# Ollama Configuration (for local LLM/image generation)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")  # Can use llava for vision tasks
OLLAMA_TIMEOUT = 300  # seconds

# Available Text-to-Image Models
AVAILABLE_DIFFUSERS_MODELS = {
    "segmind/SSD-1B": "Fast & lightweight (~1GB)",  # recommended for quick generation
    "stable-diffusion-v1-5": "Standard quality (~4GB)", # popular and well-supported
    "stabilityai/stable-diffusion-2": "High quality (~5GB)", # newer model with improved details
    "runwayml/stable-diffusion-v1-5": "Alternative v1.5 (~4GB)",# different training data, may produce varied results
}

# Available Model Types
AVAILABLE_MODELS = {
    "diffusers": "Stable Diffusion (Hugging Face)", # popular open-source text-to-image models
    "ollama": "Ollama (Local LLM/Vision)", # local models for text and image generation
    "local_llm": "Local LLM for prompt enhancement",# use a local language model to enhance prompts before image generation
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Video Generation Prompts (can be customized or auto-generated)
DEFAULT_PROMPT = "A beautiful sunset over mountains" # default prompt for testing

# Performance
USE_GPU = True # Set to False to force CPU usage (for testing or compatibility)
BATCH_SIZE = 4 # Number of images to generate in parallel (if supported by model)
