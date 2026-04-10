"""
AI Video Generator - Creates videos from text prompts using local models
"""
import logging
import os
from pathlib import Path
from datetime import datetime
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
import sys
import requests

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import (
    OUTPUT_DIR, LOG_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, 
    VIDEO_DURATION, MODEL_TYPE, TEXT_TO_IMAGE_MODEL, USE_GPU,
    OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "video_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Model Backend Classes
class DiffusersBackend:
    """Stable Diffusion backend using Hugging Face Diffusers"""
    
    def __init__(self, model_name, device):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load Stable Diffusion model"""
        try:
            from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
            
            logger.info(f"Loading Diffusers model: {self.model_name}")
            logger.info("This may take 2-5 minutes on first run...")
            
            self.model = StableDiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            self.model.scheduler = DPMSolverMultistepScheduler.from_config(
                self.model.scheduler.config
            )
            self.model = self.model.to(self.device)
            
            if self.device == "cuda":
                self.model.enable_attention_slicing()
            
            logger.info("Diffusers model loaded successfully!")
        except Exception as e:
            error_msg = f"Failed to load Diffusers model: {e}\n\nTroubleshooting:\n"
            error_msg += "1. Check your internet connection\n"
            error_msg += "2. Make sure you have at least 10GB free disk space\n"
            error_msg += "3. Try again - first download can take 2-5 minutes\n"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def generate_image(self, prompt):
        """Generate an image from text prompt"""
        with torch.no_grad():
            image = self.model(
                prompt,
                height=VIDEO_HEIGHT,
                width=VIDEO_WIDTH,
                num_inference_steps=30,
                guidance_scale=7.5
            ).images[0]
        return image


class OllamaBackend:
    """Ollama backend for local LLM/vision models"""
    
    def __init__(self, model_name, host):
        self.model_name = model_name
        self.host = host
        self.check_connection()
    
    def check_connection(self):
        """Check if Ollama is running"""
        try:
            logger.info(f"Checking Ollama connection at {self.host}")
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("Ollama is running!")
                models = response.json().get('models', [])
                logger.info(f"Available models: {[m.get('name') for m in models]}")
            else:
                raise Exception("Ollama returned unexpected status")
        except Exception as e:
            error_msg = f"Failed to connect to Ollama at {self.host}\n\n"
            error_msg += "Troubleshooting:\n"
            error_msg += "1. Make sure Ollama is installed: https://ollama.ai\n"
            error_msg += "2. Start Ollama: 'ollama serve'\n"
            error_msg += "3. Pull a model: 'ollama pull llava' (for vision)\n"
            error_msg += f"4. Verify it's running at {self.host}\n"
            error_msg += f"Error: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def generate_image(self, prompt):
        """Generate image using Ollama (enhanced prompt or placeholder)"""
        try:
            logger.info(f"Using Ollama to enhance prompt: {prompt}")
            
            # Use Ollama to enhance the prompt
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": f"Enhance this image description for beautiful visuals: {prompt}",
                    "stream": False
                },
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                enhanced_prompt = response.json().get('response', prompt)
                logger.info(f"Enhanced prompt: {enhanced_prompt}")
                
                # Create a gradient placeholder image
                # In the future, this could integrate with Ollama vision models
                img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color='blue')
                return img
            else:
                logger.warning("Ollama generation failed, using gradient placeholder")
                img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color='purple')
                return img
        except Exception as e:
            logger.error(f"Ollama error: {e}, using placeholder")
            img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color='black')
            return img


class ModelFactory:
    """Factory for creating model backends"""
    
    @staticmethod
    def create_model(model_type, device="cpu"):
        """Create and return appropriate model backend"""
        if model_type == "diffusers":
            return DiffusersBackend(TEXT_TO_IMAGE_MODEL, device)
        elif model_type == "ollama":
            return OllamaBackend(OLLAMA_MODEL, OLLAMA_HOST)
        else:
            logger.warning(f"Unknown model type {model_type}, defaulting to diffusers")
            return DiffusersBackend(TEXT_TO_IMAGE_MODEL, device)





class VideoGenerator:
    """Generates AI videos from text prompts"""
    
    def __init__(self, model_type=None, model_name=None):
        """Initialize the video generator with models
        
        Args:
            model_type: "diffusers" or "ollama" (defaults to config setting)
            model_name: Specific model name (overrides config)
        """
        self.model_type = model_type or MODEL_TYPE
        self.device = "cuda" if (USE_GPU and torch.cuda.is_available()) else "cpu"
        logger.info(f"Using device: {self.device}")
        logger.info(f"Using model type: {self.model_type}")
        
        self.text_to_image_model = None
        self.load_models()
    
    def load_models(self):
        """Load the text-to-image model using factory"""
        try:
            self.text_to_image_model = ModelFactory.create_model(self.model_type, self.device)
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise
    
    def generate_images_from_prompt(self, prompt, num_frames=10):
        """Generate a series of images from a text prompt"""
        try:
            logger.info(f"Generating {num_frames} frames for prompt: {prompt}")
            images = []
            
            for i in range(num_frames):
                logger.info(f"Generating frame {i+1}/{num_frames}")
                
                # Add variation to prompt for each frame
                varied_prompt = f"{prompt}, frame {i+1} of {num_frames}"
                
                # Use the model backend's generate_image method
                image = self.text_to_image_model.generate_image(varied_prompt)
                images.append(image)
            
            logger.info(f"Successfully generated {len(images)} frames")
            return images
        
        except Exception as e:
            logger.error(f"Error generating images: {e}")
            raise
    
    def add_text_overlay(self, image, text, position="bottom"):
        """Add text overlay to an image"""
        try:
            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Create a copy to avoid modifying original
            image_copy = image.copy()
            draw = ImageDraw.Draw(image_copy)
            
            # Try to use a nice font, fallback to default
            try:
                font_size = 50
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            if position == "bottom":
                x = (VIDEO_WIDTH - text_width) // 2
                y = VIDEO_HEIGHT - text_height - 50
            elif position == "center":
                x = (VIDEO_WIDTH - text_width) // 2
                y = (VIDEO_HEIGHT - text_height) // 2
            else:
                x = 50
                y = 50
            
            # Draw text with background for better readability
            padding = 10
            draw.rectangle(
                [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                fill=(0, 0, 0, 200)
            )
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            return image_copy
        except Exception as e:
            logger.error(f"Error adding text overlay: {e}")
            return image
    
    def create_video_from_images(self, images, output_path, fps=VIDEO_FPS, duration=VIDEO_DURATION):
        """Create a video from a list of images"""
        try:
            logger.info(f"Creating video with {len(images)} frames at {fps} fps")
            
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert images to numpy arrays FIRST
            logger.info("Converting all images to numpy arrays...")
            image_arrays = []
            for idx, img in enumerate(images):
                logger.info(f"Processing image {idx}: type={type(img).__name__}")
                
                # Step 1: Always convert to numpy array if it's a PIL Image
                if isinstance(img, Image.Image):
                    logger.info(f"  -> Converting PIL Image to ndarray")
                    arr = np.array(img)
                else:
                    arr = img
                
                # Step 2: Ensure it's an ndarray
                if not isinstance(arr, np.ndarray):
                    logger.info(f"  -> Converting {type(arr).__name__} to ndarray")
                    arr = np.array(arr)
                
                # Step 3: Ensure uint8 dtype
                if arr.dtype != np.uint8:
                    if arr.dtype in [np.float32, np.float64]:
                        # Check if values are in [0, 1] or [0, 255]
                        max_val = arr.max()
                        if max_val <= 1.0:
                            logger.info(f"  -> Scaling float [{arr.min():.2f}, {arr.max():.2f}] to uint8")
                            arr = (arr * 255).astype(np.uint8)
                        else:
                            logger.info(f"  -> Converting float [{arr.min():.2f}, {arr.max():.2f}] to uint8")
                            arr = arr.astype(np.uint8)
                    else:
                        logger.info(f"  -> Converting dtype {arr.dtype} to uint8")
                        arr = arr.astype(np.uint8)
                
                # Step 4: Ensure proper shape (H, W, 3) for RGB
                if len(arr.shape) == 2:
                    logger.info(f"  -> Converting grayscale {arr.shape} to RGB")
                    arr = np.stack([arr, arr, arr], axis=-1)
                elif len(arr.shape) == 3:
                    if arr.shape[2] == 4:
                        logger.info(f"  -> Converting RGBA {arr.shape} to RGB")
                        arr = arr[:, :, :3]
                    elif arr.shape[2] == 3:
                        logger.info(f"  -> RGB image ready: {arr.shape}")
                    else:
                        logger.warning(f"  -> Unexpected channels {arr.shape[2]}, keeping as is")
                else:
                    logger.warning(f"  -> Unexpected shape {arr.shape}")
                
                # Final validation
                if not isinstance(arr, np.ndarray):
                    raise ValueError(f"Image {idx} failed to convert to ndarray: {type(arr)}")
                if arr.dtype != np.uint8:
                    raise ValueError(f"Image {idx} dtype is {arr.dtype}, expected uint8")
                
                logger.info(f"  -> Final: type={type(arr).__name__}, dtype={arr.dtype}, shape={arr.shape}")
                image_arrays.append(arr)
            
            logger.info(f"All {len(image_arrays)} images converted successfully")
            
            # Write video
            logger.info(f"Writing {len(image_arrays)} frames to {output_path}")
            writer = imageio.get_writer(output_path, fps=fps, codec='libx264', pixelformat='yuv420p')
            
            for i, frame in enumerate(image_arrays):
                try:
                    # Verify one final time before writing
                    if not isinstance(frame, np.ndarray):
                        raise TypeError(f"Frame {i} is {type(frame).__name__}, not ndarray")
                    if frame.dtype != np.uint8:
                        raise TypeError(f"Frame {i} dtype is {frame.dtype}, not uint8")
                    
                    writer.append_data(frame)
                    logger.info(f"  Frame {i} written successfully: {frame.shape}")
                except Exception as frame_err:
                    logger.error(f"Error writing frame {i}: {frame_err}")
                    logger.error(f"Frame type: {type(frame).__name__}")
                    logger.error(f"Frame dtype: {frame.dtype if hasattr(frame, 'dtype') else 'N/A'}")
                    logger.error(f"Frame shape: {frame.shape if hasattr(frame, 'shape') else 'N/A'}")
                    raise
            
            writer.close()
            
            logger.info(f"Video created successfully: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise
    
    def generate_video(self, prompt, output_filename=None, num_frames=10):
        """Main method to generate a complete video from a text prompt"""
        try:
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"ai_video_{timestamp}.mp4"
            
            output_path = OUTPUT_DIR / output_filename
            
            logger.info(f"Starting video generation for prompt: {prompt}")
            
            # Generate images
            images = self.generate_images_from_prompt(prompt, num_frames=num_frames)
            
            # Optionally add text overlay
            images = [self.add_text_overlay(img, "AI Generated", position="top") for img in images]
            
            # Create video
            video_path = self.create_video_from_images(images, str(output_path))
            
            logger.info(f"Video generation complete: {video_path}")
            return str(video_path)
        
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            raise


def main():
    """Test the video generator"""
    import sys
    
    # Allow model type to be specified via command line or environment
    model_type = MODEL_TYPE
    if len(sys.argv) > 1:
        model_type = sys.argv[1].lower()
    
    logger.info(f"Starting video generation with model: {model_type}")
    
    generator = VideoGenerator(model_type=model_type)
    
    # Example prompt
    prompt = "A futuristic city with neon lights and flying cars at night, cinematic"
    
    # Generate video
    video_path = generator.generate_video(prompt, num_frames=8)
    print(f"Generated video: {video_path}")


if __name__ == "__main__":
    main()
