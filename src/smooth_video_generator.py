"""
Smooth Video Generator - Creates flowing AI videos like Sora
Uses frame interpolation to create smooth motion between AI-generated keyframes
"""

import logging
from pathlib import Path
from datetime import datetime
from PIL import Image
import numpy as np
import cv2
import imageio
import sys
import torch

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import OUTPUT_DIR, LOG_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "smooth_video_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SmoothVideoGenerator:
    """Generates smooth flowing videos like Sora using frame interpolation"""
    
    def __init__(self, diffusers_model=None):
        """
        Initialize with optional Diffusers model for AI image generation
        
        Args:
            diffusers_model: Optional DiffusersBackend instance for generating images
        """
        self.diffusers_model = diffusers_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Smooth Video Generator initialized (device: {self.device})")
    
    def interpolate_frames(self, frame1, frame2, num_intermediate=3):
        """
        Create smooth intermediate frames between two images using optical flow
        
        Args:
            frame1: PIL Image or numpy array (source frame)
            frame2: PIL Image or numpy array (target frame)
            num_intermediate: Number of frames to generate between them
            
        Returns:
            List of numpy arrays (smooth transition from frame1 to frame2)
        """
        # Convert PIL to numpy if needed
        if isinstance(frame1, Image.Image):
            frame1 = np.array(frame1)
        if isinstance(frame2, Image.Image):
            frame2 = np.array(frame2)
        
        # Ensure frames are uint8
        if frame1.dtype != np.uint8:
            frame1 = (frame1 * 255).astype(np.uint8) if frame1.max() <= 1.0 else frame1.astype(np.uint8)
        if frame2.dtype != np.uint8:
            frame2 = (frame2 * 255).astype(np.uint8) if frame2.max() <= 1.0 else frame2.astype(np.uint8)
        
        # Convert to grayscale for optical flow
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Generate intermediate frames
        interpolated_frames = [frame1]
        
        for i in range(1, num_intermediate + 1):
            # Interpolation factor (0 to 1)
            alpha = i / (num_intermediate + 1)
            
            # Warp frame1 towards frame2 using optical flow
            h, w = flow.shape[:2]
            x, y = np.meshgrid(np.arange(w), np.arange(h))
            
            # Apply flow
            x_warped = (x + flow[..., 0] * alpha).astype(np.float32)
            y_warped = (y + flow[..., 1] * alpha).astype(np.float32)
            
            # Remap to get warped frame
            warped = cv2.remap(
                frame1,
                x_warped, y_warped,
                cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REPLICATE
            )
            
            # Also blend the colors from both frames for smoother transition
            blended = cv2.addWeighted(warped, 1 - alpha, frame2, alpha, 0)
            
            interpolated_frames.append(blended.astype(np.uint8))
        
        interpolated_frames.append(frame2)
        return interpolated_frames
    
    def generate_smooth_video(self, prompt, num_keyframes=4, frames_per_transition=4, 
                             include_voiceover=False, sound_effect=None):
        """
        Generate a smooth flowing video like Sora
        
        Args:
            prompt: Text description for video
            num_keyframes: Number of AI-generated keyframes (fewer than total frames)
            frames_per_transition: How many smooth frames to create between keyframes
            include_voiceover: Whether to add voiceover
            sound_effect: Optional sound effect name
            
        Returns:
            Path to generated video
        """
        if self.diffusers_model is None:
            raise ValueError("No Diffusers model provided. Cannot generate AI images.")
        
        try:
            logger.info(f"Generating smooth video: '{prompt}'")
            logger.info(f"Keyframes: {num_keyframes}, Frames per transition: {frames_per_transition}")
            
            # Step 1: Generate AI keyframes
            logger.info("Step 1/3: Generating AI keyframes...")
            keyframes = []
            
            for i in range(num_keyframes):
                # Vary prompt slightly for each keyframe to create motion
                variation = f"{prompt} frame {i+1} of {num_keyframes}"
                logger.info(f"  Generating keyframe {i+1}/{num_keyframes}...")
                
                img = self.diffusers_model.generate_image(variation)
                keyframes.append(np.array(img))
            
            # Step 2: Interpolate between keyframes for smooth motion
            logger.info("Step 2/3: Creating smooth transitions between frames...")
            all_frames = []
            
            for i in range(len(keyframes)):
                # Add current keyframe
                all_frames.append(keyframes[i])
                
                # Add smooth interpolation to next keyframe
                if i < len(keyframes) - 1:
                    next_keyframe = keyframes[i + 1]
                    interpolated = self.interpolate_frames(
                        keyframes[i],
                        next_keyframe,
                        num_intermediate=frames_per_transition
                    )
                    # Add all except the first (which is the current keyframe)
                    all_frames.extend(interpolated[1:])
            
            total_frames = len(all_frames)
            logger.info(f"Generated {len(keyframes)} keyframes + {total_frames - len(keyframes)} interpolated frames = {total_frames} total frames")
            
            # Step 3: Encode to video
            logger.info("Step 3/3: Encoding to MP4 video...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"ai_video_smooth_{timestamp}.mp4"
            
            fps = 30
            writer = imageio.get_writer(str(output_path), fps=fps, codec='libx264', pixelformat='yuv420p')
            
            for i, frame in enumerate(all_frames):
                # Ensure correct format
                if isinstance(frame, np.ndarray):
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8) if frame.max() <= 1.0 else frame.astype(np.uint8)
                
                writer.append_data(frame)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"  Encoded {i+1}/{total_frames} frames")
            
            writer.close()
            logger.info(f"✓ Smooth video created: {output_path}")
            logger.info(f"  Total duration: {total_frames/fps:.1f} seconds")
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Error generating smooth video: {e}")
            raise


def demo():
    """Test the smooth video generator"""
    try:
        from src.video_generator import DiffusersBackend
        
        logger.info("Loading Stable Diffusion model...")
        backend = DiffusersBackend("segmind/SSD-1B", "cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info("Generating smooth flowing video...")
        gen = SmoothVideoGenerator(backend)
        
        video_path = gen.generate_smooth_video(
            "A beautiful sunset over mountains with water",
            num_keyframes=4,
            frames_per_transition=4
        )
        
        logger.info(f"✓ Video generated: {video_path}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    demo()
