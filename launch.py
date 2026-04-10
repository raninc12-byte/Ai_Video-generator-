#!/usr/bin/env python
"""
AI Video Generator - Simple Launcher
No heavy dependencies - uses Pillow for video generation
"""
import sys
from pathlib import Path

def launch_gui():
    """Launch the GUI application"""
    print("\n" + "="*50)
    print("🎬 AI Video Generator Launching...")
    print("="*50 + "\n")
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from src.gui_app_simple import AIVideoGeneratorApp
        import tkinter as tk
        
        root = tk.Tk()
        app = AIVideoGeneratorApp(root)
        app.run()
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        print("Initializing...")
        
        # Check for PIL/Pillow
        try:
            from PIL import Image
            print("✓ Pillow found")
        except ImportError:
            print("Installing Pillow...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', 'imageio', 'imageio-ffmpeg'])
        
        launch_gui()
    except KeyboardInterrupt:
        print("\n\nCancelled")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
