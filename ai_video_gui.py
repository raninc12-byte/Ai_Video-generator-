#!/usr/bin/env python
"""
AI Video Generator GUI - SIMPLIFIED with Two Big Buttons
Uses Stable Diffusion for real AI-generated images
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from pathlib import Path
import subprocess
import sys
import os
import torch
import logging
from datetime import datetime
import time

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"ai_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("="*60)
logger.info("AI Video Generator Started")
logger.info("="*60)

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from src.video_generator import VideoGenerator
from src.smooth_video_generator import SmoothVideoGenerator
from config.settings import OUTPUT_DIR


class AIVideoGeneratorGUI:
    """GUI for AI Video Generator - SIMPLIFIED with 2 BIG BUTTONS"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Video Generator - Choose Your Style")
        self.root.geometry("900x700")
        self.generator = None
        self.is_generating = False
        self.selected_mode = "smooth"  # Default to smooth (RED)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="🎬 AI VIDEO GENERATOR", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Subtitle
        subtitle = ttk.Label(
            main_frame, 
            text="Step 1: Choose your video style below\nStep 2: Enter your prompt\nStep 3: Click GENERATE!",
            wraplength=800,
            justify=tk.CENTER,
            font=("Arial", 11)
        )
        subtitle.grid(row=1, column=0, columnspan=2, pady=15)
        
        # ===== BUTTON SELECTOR SECTION =====
        button_label = ttk.Label(main_frame, text="CHOOSE VIDEO STYLE:", font=("Arial", 12, "bold"))
        button_label.grid(row=2, column=0, columnspan=2, pady=15)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # RED BUTTON - SMOOTH (Default)
        self.smooth_btn = tk.Button(
            button_frame,
            text="🎬 SMOOTH FLOWING\n30 FPS Movie-Like Video\n(Recommended - Best Quality)\nWait: 2-4 minutes\n✓ SELECTED",
            font=("Arial", 12, "bold"),
            bg="#CC0000",
            fg="white",
            activebackground="#FF0000",
            activeforeground="white",
            width=45,
            height=5,
            command=lambda: self.select_mode("smooth"),
            relief=tk.RAISED,
            bd=3
        )
        self.smooth_btn.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # GREEN BUTTON - QUICK (Alternative)
        self.quick_btn = tk.Button(
            button_frame,
            text="📸 QUICK PREVIEW\nFast Standard Video\n(For Quick Testing)\nWait: 1-3 minutes\n",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#66BB6A",
            activeforeground="white",
            width=45,
            height=5,
            command=lambda: self.select_mode("quick"),
            relief=tk.RAISED,
            bd=2
        )
        self.quick_btn.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # ===== PROMPT SECTION =====
        prompt_label = ttk.Label(main_frame, text="ENTER YOUR VIDEO PROMPT:", font=("Arial", 12, "bold"))
        prompt_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        prompt_instructions = ttk.Label(
            main_frame,
            text="Example: 'Ocean waves crashing on a beach' or 'A peaceful forest with sunlight'",
            font=("Arial", 10),
            foreground="gray"
        )
        prompt_instructions.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.prompt_text = scrolledtext.ScrolledText(
            main_frame,
            height=5,
            width=80,
            wrap=tk.WORD,
            font=("Arial", 11)
        )
        self.prompt_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.prompt_text.insert("1.0", "A beautiful sunset over mountains")
        
        # ===== FRAMES SECTION (only for Quick) =====
        frames_label = ttk.Label(main_frame, text="Number of Frames (Quick mode only):", font=("Arial", 10))
        frames_label.grid(row=7, column=0, sticky=tk.W, pady=(15, 5))
        
        frame_frame = ttk.Frame(main_frame)
        frame_frame.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.frames_var = tk.IntVar(value=8)
        self.frames_slider = ttk.Scale(
            frame_frame,
            from_=3,
            to=15,
            orient=tk.HORIZONTAL,
            variable=self.frames_var,
            command=self.update_frame_label
        )
        self.frames_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipadx=100)
        
        self.frames_label = ttk.Label(frame_frame, text="8 frames", width=12, font=("Arial", 10))
        self.frames_label.pack(side=tk.LEFT, padx=5)
        
        # ===== GENERATE BUTTON =====
        self.generate_btn = tk.Button(
            main_frame,
            text="🚀 GENERATE VIDEO",
            font=("Arial", 16, "bold"),
            bg="#CC0000",
            fg="white",
            activebackground="#FF0000",
            padx=30,
            pady=20,
            command=self.generate_video
        )
        self.generate_btn.grid(row=9, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to generate. Choose RED (best) or GREEN (fast), enter your prompt, then click GENERATE!")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 10)
        )
        status_bar.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=800
        )
        self.progress.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Open folder button
        self.open_btn = tk.Button(
            main_frame,
            text="📁 Open Videos Folder",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.open_output_folder
        )
        self.open_btn.grid(row=12, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
    
    
    def select_mode(self, mode):
        """Select video generation mode (smooth or quick)"""
        self.selected_mode = mode
        logger.info(f"Mode selected: {mode}")
        
        # Update button appearances
        if mode == "smooth":
            # RED button selected
            logger.info("Selected: SMOOTH FLOWING (optical flow interpolation, 2-4 minutes)")
            self.smooth_btn.config(
                text="🎬 SMOOTH FLOWING\n30 FPS Movie-Like Video\n(Recommended - Best Quality)\nWait: 2-4 minutes\n✓ SELECTED",
                bg="#CC0000",
                relief=tk.SUNKEN,
                bd=4
            )
            self.quick_btn.config(
                text="📸 QUICK PREVIEW\nFast Standard Video\n(For Quick Testing)\nWait: 1-3 minutes\n",
                bg="#4CAF50",
                relief=tk.RAISED,
                bd=2
            )
            self.status_var.set("✓ Selected: SMOOTH FLOWING (best quality, takes 2-4 minutes)")
        else:
            # GREEN button selected
            logger.info("Selected: QUICK PREVIEW (direct frames, 1-3 minutes)")
            self.quick_btn.config(
                text="📸 QUICK PREVIEW\nFast Standard Video\n(For Quick Testing)\nWait: 1-3 minutes\n✓ SELECTED",
                bg="#2E7D32",
                relief=tk.SUNKEN,
                bd=4
            )
            self.smooth_btn.config(
                text="🎬 SMOOTH FLOWING\n30 FPS Movie-Like Video\n(Recommended - Best Quality)\nWait: 2-4 minutes\n",
                bg="#CC0000",
                relief=tk.RAISED,
                bd=2
            )
            self.status_var.set("✓ Selected: QUICK PREVIEW (fast testing, takes 1-3 minutes)")
    
    def update_frame_label(self, value):
        """Update frame count label"""
        frames = int(float(value))
        self.frames_label.config(text=f"{frames} frames")
    
    def generate_video(self):
        """Generate video in background thread"""
        if self.is_generating:
            logger.warning("Generation already in progress - user attempted to start another")
            messagebox.showwarning("Already Running", "Video generation is already in progress!")
            return
        
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            logger.warning("User attempted to generate without entering prompt")
            messagebox.showerror("Error", "Please enter a video prompt!")
            return
        
        logger.info(f"Generation started - Mode: {self.selected_mode}, Prompt: {prompt[:50]}...")
        
        # Disable button and start progress
        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED, text="⏳ Generating...")
        self.progress.start()
        self.status_var.set("Loading AI model (first time takes 2-3 minutes)...")
        
        # Run in background thread
        thread = threading.Thread(
            target=self._generate_video_thread,
            args=(prompt,),
            daemon=True
        )
        thread.start()
    
    def _generate_video_thread(self, prompt):
        """Background thread for video generation - SIMPLIFIED"""
        start_time = time.time()
        try:
            self.status_var.set("Initializing AI video generator...")
            logger.info("Initializing AI video generator...")
            self.root.update()
            
            if self.selected_mode == "smooth":
                # SMOOTH FLOWING VIDEO (RED BUTTON)
                logger.info("Starting SMOOTH FLOWING generation (optical flow interpolation)")
                self.status_var.set("Loading AI model for smooth flowing video...")
                self.root.update()
                
                model_load_time = time.time()
                from src.video_generator import DiffusersBackend
                backend = DiffusersBackend(
                    "segmind/SSD-1B",
                    "cuda" if torch.cuda.is_available() else "cpu"
                )
                model_load_elapsed = time.time() - model_load_time
                logger.info(f"AI model loaded in {model_load_elapsed:.2f} seconds")
                
                generator = SmoothVideoGenerator(backend)
                logger.info("SmoothVideoGenerator initialized")
                
                self.status_var.set("Generating smooth 30 FPS video (6 keyframes + interpolation)...")
                self.root.update()
                
                gen_time = time.time()
                output_path = generator.generate_smooth_video(
                    prompt=prompt,
                    num_keyframes=6,
                    frames_per_transition=4,
                    include_voiceover=False,
                    sound_effect=None
                )
                gen_elapsed = time.time() - gen_time
                logger.info(f"Smooth video generation completed in {gen_elapsed:.2f} seconds")
                logger.info(f"Output: {output_path}")
            
            else:  # quick
                # QUICK PREVIEW VIDEO (GREEN BUTTON)
                logger.info("Starting QUICK PREVIEW generation (direct frames)")
                self.status_var.set("Loading AI model for quick preview video...")
                self.root.update()
                
                model_load_time = time.time()
                num_frames = self.frames_var.get()
                generator = VideoGenerator()
                model_load_elapsed = time.time() - model_load_time
                logger.info(f"VideoGenerator loaded in {model_load_elapsed:.2f} seconds")
                
                self.status_var.set(f"Generating {num_frames} frames with AI...")
                self.root.update()
                logger.info(f"Generating {num_frames} frames...")
                
                gen_time = time.time()
                output_path = generator.generate_video(
                    prompt=prompt,
                    num_frames=num_frames,
                    include_voiceover=False
                )
                gen_elapsed = time.time() - gen_time
                logger.info(f"Quick video generation completed in {gen_elapsed:.2f} seconds")
                logger.info(f"Output: {output_path}")
            
            # Success!
            total_elapsed = time.time() - start_time
            self.progress.stop()
            self.status_var.set(f"✅ SUCCESS! Video saved to Downloads/AI Videos/")
            self.generate_btn.config(state=tk.NORMAL, text="🚀 GENERATE VIDEO")
            
            logger.info(f"Total generation time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)")
            logger.info("="*60)
            
            messagebox.showinfo(
                "Success!",
                f"Your AI video has been created!\n\n"
                f"Mode: {'Smooth 30 FPS' if self.selected_mode == 'smooth' else 'Quick Preview'}\n"
                f"Time: {total_elapsed/60:.2f} minutes\n"
                f"Location: {OUTPUT_DIR}\n\n"
                "You can now:\n"
                "• Open the folder to watch your video\n"
                "• Share it on social media\n"
                "• Generate another video with a different prompt!"
            )
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Generation failed after {elapsed:.2f} seconds")
            logger.error(f"Error: {str(e)}", exc_info=True)
            self.progress.stop()
            error_str = str(e)[:100]
            self.status_var.set(f"❌ Error: {error_str}")
            self.generate_btn.config(state=tk.NORMAL, text="🚀 GENERATE VIDEO")
            
            error_msg = f"Video generation failed:\n\n{str(e)}\n\n"
            error_msg += "Troubleshooting:\n"
            error_msg += "• Check internet connection\n"
            error_msg += "• Ensure 10GB free disk space\n"
            error_msg += "• First run downloads ~4GB AI model (2-3 minutes)\n"
            error_msg += "• Check logs/ folder for details\n"
            error_msg += "• GPU users: Check CUDA installation"
            
            messagebox.showerror("Generation Failed", error_msg)
        
        finally:
            self.is_generating = False
    
    def open_output_folder(self):
        """Open the output folder"""
        logger.info("User opened output folder")
        if OUTPUT_DIR.exists():
            logger.info(f"Opening folder: {OUTPUT_DIR}")
            os.startfile(str(OUTPUT_DIR))
        else:
            logger.warning("Output folder does not exist yet")
            messagebox.showwarning("Folder Not Found", "Output folder doesn't exist yet. Generate a video first!")


def main():
    """Launch the GUI"""
    logger.info("Launching main GUI window")
    root = tk.Tk()
    app = AIVideoGeneratorGUI(root)
    logger.info("GUI window created and ready")
    root.mainloop()
    logger.info("GUI window closed - application ending")


if __name__ == "__main__":
    logger.info("Application started as main")
    main()
