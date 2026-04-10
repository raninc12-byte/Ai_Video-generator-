"""
AI Video Generator - Simple GUI Application
One-click video generation from text prompts
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from pathlib import Path
import sys
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.video_generator import VideoGenerator
from config.settings import OUTPUT_DIR, LOG_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "gui_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AIVideoGeneratorApp:
    """GUI Application for AI Video Generation"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("AI Video Generator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.generator = None
        self.is_generating = False
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        logger.info("GUI Application started")
    
    def setup_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🎬 AI Video Generator",
            font=("Helvetica", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Prompt section
        prompt_label = ttk.Label(
            main_frame,
            text="📝 Describe your video:",
            font=("Helvetica", 12, "bold")
        )
        prompt_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Prompt text input
        self.prompt_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            width=50,
            wrap=tk.WORD,
            font=("Helvetica", 11)
        )
        self.prompt_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        self.prompt_text.insert("1.0", "A beautiful sunset over mountains with waves crashing on the beach")
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="10")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        options_frame.columnconfigure(1, weight=1)
        
        # Frames slider
        ttk.Label(options_frame, text="Number of Frames:", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.frames_var = tk.IntVar(value=8)
        frames_slider = ttk.Scale(
            options_frame,
            from_=3,
            to=15,
            orient=tk.HORIZONTAL,
            variable=self.frames_var,
            command=self.update_frames_label
        )
        frames_slider.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10)
        
        self.frames_label = ttk.Label(options_frame, text="8 frames", font=("Helvetica", 10))
        self.frames_label.grid(row=0, column=2, sticky=tk.W)
        
        # Generate button
        self.generate_btn = ttk.Button(
            main_frame,
            text="🎥 GENERATE VIDEO",
            command=self.on_generate_click,
            width=30
        )
        self.generate_btn.grid(row=4, column=0, pady=(0, 15))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="📊 Status", padding="10")
        status_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        # Status message
        self.status_label = ttk.Label(
            status_frame,
            text="Ready! Enter a prompt and click the button to generate a video.",
            font=("Helvetica", 10),
            foreground="green"
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate'
        )
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Info text
        self.info_text = scrolledtext.ScrolledText(
            status_frame,
            height=8,
            width=50,
            wrap=tk.WORD,
            font=("Courier", 9),
            state=tk.DISABLED
        )
        self.info_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        
        ttk.Label(
            footer_frame,
            text=f"📁 Videos saved to: {OUTPUT_DIR}",
            font=("Helvetica", 9),
            foreground="blue"
        ).pack(side=tk.LEFT)
    
    def update_frames_label(self, value):
        """Update frames label when slider changes"""
        frames = int(float(value))
        self.frames_label.config(text=f"{frames} frames")
    
    def update_info(self, message, status="info"):
        """Update the info text area"""
        self.info_text.config(state=tk.NORMAL)
        if self.info_text.get("1.0", tk.END).strip():
            self.info_text.insert(tk.END, "\n")
        self.info_text.insert(tk.END, message)
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
    
    def on_generate_click(self):
        """Handle generate button click"""
        if self.is_generating:
            messagebox.showwarning("Generating", "Already generating a video. Please wait.")
            return
        
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt for the video.")
            return
        
        # Disable button and show progress
        self.generate_btn.config(state=tk.DISABLED)
        self.is_generating = True
        self.progress.start()
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.config(state=tk.DISABLED)
        
        self.update_info("🔄 Initializing AI model...")
        self.update_info("This may take a moment on first run...")
        
        # Run generation in background thread
        frames = int(self.frames_var.get())
        thread = threading.Thread(target=self.generate_video, args=(prompt, frames))
        thread.start()
    
    def generate_video(self, prompt, frames):
        """Generate video in background thread"""
        try:
            # Initialize generator if needed
            if self.generator is None:
                self.update_info("📥 Loading AI model...")
                self.update_info("⏳ This takes 2-5 minutes FIRST TIME (downloading 4GB model)")
                self.update_info("   Subsequent generations will be much faster!")
                self.update_info("")
                self.generator = VideoGenerator()
                self.update_info("✅ Model loaded! Starting video generation...")
            
            self.update_info(f"🎬 Generating {frames} frames...")
            self.update_info(f"📝 Prompt: {prompt}")
            self.update_info("")
            self.update_info("⏳ This takes 5-15 minutes depending on frame count...")
            
            # Generate video
            video_path = self.generator.generate_video(
                prompt,
                num_frames=frames
            )
            
            self.update_info("")
            self.update_info(f"✅ Video generated successfully!")
            self.update_info(f"📁 Saved to: {video_path}")
            
            # Update status
            self.status_label.config(
                text=f"✅ Video saved! Open Downloads/AI Videos folder to view.",
                foreground="green"
            )
            
            messagebox.showinfo(
                "Success! 🎉",
                f"Video generated!\n\n"
                f"Go to: Downloads\\AI Videos\n\n"
                f"File: {Path(video_path).name}"
            )
        
        except Exception as e:
            error_msg = str(e)
            self.update_info("")
            self.update_info(f"❌ Error: {error_msg}")
            self.status_label.config(text="❌ Generation failed", foreground="red")
            logger.error(f"Generation failed: {e}")
            messagebox.showerror("Generation Failed", error_msg)
        
        finally:
            # Re-enable button and hide progress
            self.progress.stop()
            self.generate_btn.config(state=tk.NORMAL)
            self.is_generating = False
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AIVideoGeneratorApp(root)
    app.run()


if __name__ == "__main__":
    main()
