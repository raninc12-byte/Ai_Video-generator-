#!/usr/bin/env python3
"""
Model selector - Interactive tool to switch between different AI models
"""
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import (
    AVAILABLE_MODELS, 
    AVAILABLE_DIFFUSERS_MODELS,
    MODEL_TYPE,
    TEXT_TO_IMAGE_MODEL,
    OLLAMA_HOST,
    OLLAMA_MODEL
)


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def show_current_config():
    """Show current model configuration"""
    print_header("Current Configuration")
    print(f"\nActive Model Type: {MODEL_TYPE}")
    print(f"  │")
    
    if MODEL_TYPE == "diffusers":
        print(f"  ├─ Text-to-Image: {TEXT_TO_IMAGE_MODEL}")
        print(f"  └─ Description: {AVAILABLE_DIFFUSERS_MODELS.get(TEXT_TO_IMAGE_MODEL, 'Unknown')}")
    elif MODEL_TYPE == "ollama":
        print(f"  ├─ Ollama Host: {OLLAMA_HOST}")
        print(f"  └─ Ollama Model: {OLLAMA_MODEL}")
    
    print()


def show_available_models():
    """Show available model types and models"""
    print_header("Available Models")
    
    print("\n1. DIFFUSERS (Stable Diffusion)")
    print("   " + "─" * 56)
    for model_name, description in AVAILABLE_DIFFUSERS_MODELS.items():
        print(f"   • {model_name}")
        print(f"     └─ {description}")
    
    print("\n2. OLLAMA (Local LLMs)")
    print("   " + "─" * 56)
    print("   • llava      - Vision model for image understanding")
    print("   • llama2     - General LLM for prompt enhancement")
    print("   • mistral    - Fast high-quality LLM")
    print("   • neural-chat - Optimized for conversations")
    print("   • Plus any model from https://ollama.ai/library")
    print()


def show_setup_instructions():
    """Show setup instructions for each model type"""
    print_header("Setup Instructions")
    
    print("\n📦 DIFFUSERS Setup (Default)")
    print("   " + "─" * 56)
    print("   1. No additional setup needed!")
    print("   2. Set environment: set MODEL_TYPE=diffusers")
    print("   3. Choose model: set TEXT_TO_IMAGE_MODEL=segmind/SSD-1B")
    print("   4. Run: python video_gen.py")
    print("   5. First run will download ~1-5GB (takes 2-5 minutes)")
    
    print("\n🦙 OLLAMA Setup")
    print("   " + "─" * 56)
    print("   1. Install Ollama: https://ollama.ai")
    print("   2. Start Ollama: ollama serve")
    print("   3. In another terminal, pull a model:")
    print("      ollama pull llama2        # For LLM")
    print("      ollama pull llava         # For vision")
    print("   4. Set environment: set MODEL_TYPE=ollama")
    print("   5. Set model: set OLLAMA_MODEL=llama2")
    print("   6. Run: python video_gen.py")
    print()


def generate_batch_script():
    """Generate Windows batch script to quickly switch models"""
    print_header("Quick Switch Scripts")
    
    script_diffusers = """@echo off
REM Quick launcher for Diffusers (Stable Diffusion)
set MODEL_TYPE=diffusers
set TEXT_TO_IMAGE_MODEL=segmind/SSD-1B
python video_gen.py
pause
"""
    
    script_ollama = """@echo off
REM Quick launcher for Ollama
set MODEL_TYPE=ollama
set OLLAMA_HOST=http://localhost:11434
set OLLAMA_MODEL=llama2
python video_gen.py
pause
"""
    
    # Save scripts
    with open('run_diffusers.bat', 'w') as f:
        f.write(script_diffusers)
    
    with open('run_ollama.bat', 'w') as f:
        f.write(script_ollama)
    
    print("\n✅ Generated quick launcher scripts:")
    print("   • run_diffusers.bat - Launch with Stable Diffusion")
    print("   • run_ollama.bat    - Launch with Ollama")
    print("\nYou can now double-click these to launch the app with specific models!")
    print()


def main():
    """Main menu"""
    print_header("AI Video Generator - Model Selector")
    
    while True:
        print("\nOptions:")
        print("  1. Show current configuration")
        print("  2. Show available models")
        print("  3. Show setup instructions")
        print("  4. Generate quick launcher scripts")
        print("  5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            show_current_config()
        elif choice == "2":
            show_available_models()
        elif choice == "3":
            show_setup_instructions()
        elif choice == "4":
            generate_batch_script()
        elif choice == "5":
            print("\nGoodbye! 👋\n")
            break
        else:
            print("❌ Invalid option, try again")


if __name__ == "__main__":
    main()
