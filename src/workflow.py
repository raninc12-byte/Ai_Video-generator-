"""
Main Workflow Orchestrator - Coordinates AI video generation and TikTok upload
"""
import logging
import argparse
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from video_generator import VideoGenerator
from tiktok_uploader import TikTokUploader
from config.settings import LOG_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "workflow.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AIVideoWorkflow:
    """Main workflow to generate AI videos and upload to TikTok"""
    
    def __init__(self):
        """Initialize the workflow components"""
        self.generator = None
        self.uploader = TikTokUploader()
        logger.info("Workflow initialized")
    
    def generate_and_upload(
        self,
        prompt: str,
        title: str,
        description: str = "",
        upload: bool = False,
        num_frames: int = 10,
        output_filename: Optional[str] = None
    ):
        """
        Generate a video from a prompt and optionally upload to TikTok
        
        Args:
            prompt: Text description for video generation
            title: Title for TikTok post
            description: Description for TikTok post
            upload: Whether to upload to TikTok
            num_frames: Number of frames to generate
            output_filename: Custom output filename
        
        Returns:
            Dictionary with generation and upload results
        """
        try:
            results = {
                "status": "failed",
                "video_path": None,
                "upload_status": None,
                "error": None
            }
            
            # Step 1: Initialize video generator if not already done
            if self.generator is None:
                logger.info("Initializing video generator...")
                self.generator = VideoGenerator()
            
            # Step 2: Generate video
            logger.info(f"Starting video generation with prompt: {prompt}")
            video_path = self.generator.generate_video(
                prompt,
                output_filename=output_filename,
                num_frames=num_frames
            )
            results["video_path"] = video_path
            logger.info(f"✓ Video generated: {video_path}")
            
            # Step 3: Upload to TikTok if requested
            if upload:
                logger.info("Starting TikTok upload...")
                upload_result = self.uploader.upload_video(
                    video_path,
                    title=title,
                    description=description
                )
                results["upload_status"] = upload_result
                logger.info("✓ Video uploaded to TikTok")
            else:
                logger.info("Skipping TikTok upload (upload flag not set)")
            
            results["status"] = "success"
            return results
        
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            results["status"] = "failed"
            results["error"] = str(e)
            return results
    
    def batch_generate(self, prompts_file: str, upload: bool = False):
        """
        Generate videos from a batch of prompts in a file
        
        Args:
            prompts_file: Path to file with prompts (JSON or text format)
            upload: Whether to upload videos to TikTok
        """
        try:
            prompts_path = Path(prompts_file)
            
            if not prompts_path.exists():
                raise FileNotFoundError(f"Prompts file not found: {prompts_file}")
            
            logger.info(f"Loading prompts from: {prompts_file}")
            
            # Load prompts based on file format
            if prompts_path.suffix == ".json":
                import json
                with open(prompts_path, "r") as f:
                    prompts = json.load(f)
            else:
                with open(prompts_path, "r") as f:
                    prompts = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Loaded {len(prompts)} prompts")
            
            results = []
            for i, prompt in enumerate(prompts, 1):
                logger.info(f"\n--- Processing prompt {i}/{len(prompts)} ---")
                result = self.generate_and_upload(
                    prompt=prompt,
                    title=f"AI Video {i}",
                    description=prompt[:100],
                    upload=upload,
                    num_frames=10
                )
                results.append(result)
            
            logger.info(f"\n✓ Batch processing complete: {len(results)} videos processed")
            return results
        
        except Exception as e:
            logger.error(f"Batch generation failed: {e}")
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Video Generation and TikTok Upload Workflow"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Single video generation
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a single video from a text prompt"
    )
    generate_parser.add_argument(
        "prompt",
        type=str,
        help="Text prompt for video generation"
    )
    generate_parser.add_argument(
        "--title",
        type=str,
        default="AI Generated Video",
        help="Title for TikTok post"
    )
    generate_parser.add_argument(
        "--description",
        type=str,
        default="",
        help="Description for TikTok post"
    )
    generate_parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload video to TikTok after generation"
    )
    generate_parser.add_argument(
        "--frames",
        type=int,
        default=10,
        help="Number of frames to generate (default: 10)"
    )
    generate_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output filename"
    )
    
    # Batch generation
    batch_parser = subparsers.add_parser(
        "batch",
        help="Generate multiple videos from a file of prompts"
    )
    batch_parser.add_argument(
        "file",
        type=str,
        help="Path to file with prompts (JSON or text, one per line)"
    )
    batch_parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload all videos to TikTok"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create workflow
    workflow = AIVideoWorkflow()
    
    # Execute command
    if args.command == "generate":
        logger.info("=" * 60)
        logger.info("Starting AI Video Generation Workflow")
        logger.info("=" * 60)
        
        result = workflow.generate_and_upload(
            prompt=args.prompt,
            title=args.title,
            description=args.description,
            upload=args.upload,
            num_frames=args.frames,
            output_filename=args.output
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("Workflow Results")
        logger.info("=" * 60)
        logger.info(f"Status: {result['status']}")
        if result['video_path']:
            logger.info(f"Video: {result['video_path']}")
        if result['error']:
            logger.error(f"Error: {result['error']}")
        
        return 0 if result["status"] == "success" else 1
    
    elif args.command == "batch":
        logger.info("=" * 60)
        logger.info("Starting Batch Video Generation")
        logger.info("=" * 60)
        
        results = workflow.batch_generate(args.file, upload=args.upload)
        
        success_count = sum(1 for r in results if r["status"] == "success")
        logger.info(f"\nResults: {success_count}/{len(results)} successful")
        
        return 0 if success_count == len(results) else 1
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
