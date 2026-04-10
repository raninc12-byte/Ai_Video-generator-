"""
Direct Text-to-Video Generator
Generates continuous video directly from text prompts (no intermediate images)
Uses ModelScope text-to-video diffusion model
"""

import logging
from pathlib import Path
from datetime import datetime
import torch
import imageio
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import OUTPUT_DIR, LOG_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "direct_video_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DirectVideoGenerator:
    """Generates continuous video directly from text (no intermediate images)"""
    
    def __init__(self):
        """Initialize the text-to-video generator"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.pipe = None
        logger.info(f"Direct Video Generator initialized (device: {self.device})")
    
    def load_model(self):
        """Load the text-to-video model"""
        try:
            logger.info("Loading text-to-video model (ModelScope)...")
            logger.info("This may take 1-2 minutes on first run...")
            
            from diffusers import DiffusionPipeline
            
            # ModelScope text-to-video model
            model_id = "damo-viyu/text-to-video-ms-1.7b"
            
            logger.info(f"Downloading model: {model_id}")
            
            self.pipe = DiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            self.pipe = self.pipe.to(self.device)
            
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
            
            logger.info("✓ Text-to-video model loaded successfully!")
            
        except Exception as e:
            error_msg = f"Failed to load text-to-video model: {e}\n"
            error_msg += "Make sure you have:\n"
            error_msg += "- At least 10GB free disk space\n"
            error_msg += "- Internet connection (for first-time download)\n"
            error_msg += "- 8GB+ VRAM for GPU\n"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def generate_video(self, prompt, num_frames=30, height=576, width=1024, num_inference_steps=30):
        """
        Generate video directly from text prompt
        
        Args:
            prompt: Text description for the video
            num_frames: Number of frames (30 = 1 second at 30 FPS)
            height: Video height (must be divisible by 8)
            width: Video width (must be divisible by 8)
            num_inference_steps: Quality steps (more = better but slower)
            
        Returns:
            Path to generated video file
        """
        try:
            if self.pipe is None:
                self.load_model()
            
            # Ensure dimensions are divisible by 8
            height = (height // 8) * 8
            width = (width // 8) * 8
            
            logger.info(f"Generating video: '{prompt}'")
            logger.info(f"Settings: {num_frames} frames, {height}x{width}, {num_inference_steps} steps")
            logger.info("This may take 5-10 minutes...")
            
            # Generate video
            with torch.no_grad():
                output = self.pipe(
                    prompt=prompt,
                    height=height,
                    width=width,
                    num_frames=num_frames,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=7.5
                )
            
            # Extract video frames
            video_frames = output.frames[0] if hasattr(output, 'frames') else output
            
            # Convert to numpy arrays if needed
            if not isinstance(video_frames, list):
                video_frames = [video_frames]
            
            # Ensure proper format
            frames = []
            for frame in video_frames:
                if isinstance(frame, torch.Tensor):
                    # Convert tensor to PIL Image then to numpy
                    from PIL import Image
                    if frame.dim() == 4:
                        frame = frame.squeeze(0)
                    
                    # Normalize to 0-255
                    frame = frame.cpu()
                    if frame.dtype == torch.float32:
                        frame = (frame * 255).type(torch.uint8)
                    
                    # Convert to numpy
                    frame = frame.permute(2, 0, 1).numpy()  # CHW to HWC? No, keep as is
                    frame = np.transpose(frame, (1, 2, 0))  # CHW -> HWC if needed
                    frame = np.asarray(frame, dtype=np.uint8)
                else:
                    frame = np.asarray(frame, dtype=np.uint8)
                
                frames.append(frame)
            
            logger.info(f"Generated {len(frames)} frames")
            
            # Save to video file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"continuous_video_{timestamp}.mp4"
            
            logger.info(f"Saving video to: {output_path}")
            
            fps = 30
            writer = imageio.get_writer(str(output_path), fps=fps, codec='libx264', pixelformat='yuv420p')
            
            for i, frame in enumerate(frames):
                # Ensure proper shape and type
                if frame.dtype != np.uint8:
                    if frame.max() <= 1.0:
                        frame = (frame * 255).astype(np.uint8)
                    else:
                        frame = frame.astype(np.uint8)
                
                writer.append_data(frame)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"  Wrote {i+1}/{len(frames)} frames")
            
            writer.close()
            
            duration = len(frames) / fps
            logger.info(f"✓ Video created successfully!")
            logger.info(f"  Location: {output_path}")
            logger.info(f"  Duration: {duration:.1f} seconds at {fps} FPS")
            logger.info(f"  Resolution: {height}x{width}")
            logger.info(f"  Total frames: {len(frames)}")
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            raise


def demo():
    """Test the direct video generator"""
    try:
        gen = DirectVideoGenerator()
        
        logger.info("Generating continuous video...")
        video_path = gen.generate_video(
            "A beautiful sunset over mountains with ocean waves",
            num_frames=30,
            height=576,
            width=1024,
            num_inference_steps=30
        )
        
        logger.info(f"✓ Video generated: {video_path}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    demo()
