"""
Simple AI Video Generator - No heavy dependencies
Creates visually interesting videos using PIL and color generation
"""
import logging
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio
import numpy as np
import colorsys
import random
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import OUTPUT_DIR, LOG_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "video_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SimpleVideoGenerator:
    """Generates colorful AI videos without heavy ML libraries"""
    
    def __init__(self):
        """Initialize the generator"""
        logger.info("Simple Video Generator initialized")
        self.video_width = 1080
        self.video_height = 1920
    
    def generate_gradient_frame(self, frame_num, total_frames, hue_offset=0):
        """Generate a gradient frame"""
        img = Image.new('RGB', (self.video_width, self.video_height), color='black')
        pixels = img.load()
        
        for y in range(self.video_height):
            for x in range(self.video_width):
                # Calculate color based on position and frame
                hue = ((x / self.video_width + y / self.video_height) / 2 + hue_offset) % 1.0
                saturation = 0.8 + 0.2 * (frame_num / max(total_frames - 1, 1))
                value = 0.3 + 0.7 * ((frame_num + 1) / total_frames)
                
                r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
                pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))
        
        return img
    
    def add_text_and_effects(self, img, text, frame_num, total_frames):
        """Add text and effects to frame"""
        draw = ImageDraw.Draw(img)
        
        # Add animated text
        font_size = 80 + int(20 * (frame_num / max(total_frames - 1, 1)))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (animated)
        y_offset = int(300 * (frame_num / total_frames))
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (self.video_width - text_width) // 2
        y = (self.video_height - text_height) // 2 + y_offset
        
        # Draw text with shadow
        draw.text((x + 5, y + 5), text, fill=(0, 0, 0), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        return img
    
    def generate_video(self, prompt, output_filename=None, num_frames=10):
        """Generate a video"""
        try:
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"ai_video_{timestamp}.mp4"
            
            output_path = OUTPUT_DIR / output_filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Generating video: {prompt}")
            logger.info(f"Frames: {num_frames}")
            
            # Generate frames
            frames = []
            for frame_num in range(num_frames):
                logger.info(f"  Frame {frame_num + 1}/{num_frames}")
                
                # Create gradient background
                img = self.generate_gradient_frame(frame_num, num_frames, hue_offset=0.5)
                
                # Add text
                img = self.add_text_and_effects(img, prompt[:30], frame_num, num_frames)
                
                # Apply slight blur  for smooth effect
                img = img.filter(ImageFilter.GaussianBlur(radius=2))
                
                frames.append(img)
            
            # Write video
            logger.info(f"Writing video: {output_path}")
            writer = imageio.get_writer(output_path, fps=30, codec='libx264', pixelformat='yuv420p')
            for frame in frames:
                # Convert PIL Image to numpy array if needed
                if isinstance(frame, Image.Image):
                    frame = np.array(frame)
                writer.append_data(frame)
            writer.close()
            
            logger.info(f"✓ Video created: {output_path}")
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Error: {e}")
            raise


def main():
    """Test the generator"""
    gen = SimpleVideoGenerator()
    video_path = gen.generate_video("Beautiful Gradient Animation", num_frames=8)
    print(f"Generated: {video_path}")


if __name__ == "__main__":
    main()
