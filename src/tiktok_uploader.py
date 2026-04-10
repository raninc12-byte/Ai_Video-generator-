"""
TikTok Video Uploader - Uploads generated videos to TikTok
"""
import logging
import os
from pathlib import Path
import requests
import json
from dotenv import load_dotenv
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import LOG_DIR

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "tiktok_upload.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TikTokUploader:
    """Handles uploading videos to TikTok"""
    
    def __init__(self):
        """Initialize TikTok API client"""
        self.client_key = os.getenv("TIKTOK_CLIENT_KEY", "")
        self.client_secret = os.getenv("TIKTOK_CLIENT_SECRET", "")
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "")
        
        # TikTok API endpoints
        self.base_url = "https://open.tiktokapis.com"
        self.oauth_token_url = f"{self.base_url}/v1/oauth/token"
        self.upload_url = f"{self.base_url}/v1/post/publish/action/upload"
        self.create_url = f"{self.base_url}/v1/post/publish/action/post"
        
        if not self.access_token:
            logger.warning("TIKTOK_ACCESS_TOKEN not set. Upload functionality may not work.")
            logger.info("Please set up TikTok OAuth credentials in .env file")
    
    def get_access_token(self):
        """Obtain access token using OAuth flow"""
        try:
            if self.access_token:
                logger.info("Using cached access token")
                return self.access_token
            
            logger.info("Requesting new access token from TikTok API...")
            
            payload = {
                "client_key": self.client_key,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
            
            response = requests.post(self.oauth_token_url, json=payload)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("data", {}).get("access_token")
            
            logger.info("Successfully obtained access token")
            return self.access_token
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obtaining access token: {e}")
            raise
    
    def upload_video(self, video_path, title="AI Generated Video", description=""):
        """Upload a video file to TikTok"""
        try:
            video_path = Path(video_path)
            
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            logger.info(f"Uploading video: {video_path}")
            logger.info(f"Title: {title}")
            
            # Get access token
            token = self.get_access_token()
            if not token:
                raise ValueError("Failed to obtain TikTok access token")
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/octet-stream"
            }
            
            # Read video file
            with open(video_path, "rb") as f:
                video_data = f.read()
            
            # Upload video to TikTok
            logger.info("Uploading video binary to TikTok...")
            response = requests.post(
                self.upload_url,
                headers=headers,
                data=video_data,
                timeout=300  # 5 minute timeout for large files
            )
            response.raise_for_status()
            
            upload_data = response.json()
            video_id = upload_data.get("data", {}).get("video_id")
            
            logger.info(f"Video uploaded successfully. Video ID: {video_id}")
            
            # Create post with metadata
            if video_id:
                post_response = self.create_post(video_id, title, description)
                return post_response
            
            return upload_data
        
        except FileNotFoundError as e:
            logger.error(f"File error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"API error during upload: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def create_post(self, video_id, title, description):
        """Create a TikTok post with the uploaded video"""
        try:
            logger.info(f"Creating TikTok post with video ID: {video_id}")
            
            token = self.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "data": {
                    "video_id": video_id,
                    "caption": f"{title}\n{description}" if description else title,
                    "privacy_level": "PUBLIC",
                    "allow_comment": True,
                    "allow_duet": True,
                    "allow_stitch": True
                }
            }
            
            response = requests.post(
                self.create_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            post_data = response.json()
            logger.info("TikTok post created successfully")
            
            return post_data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating post: {e}")
            raise
    
    def check_upload_status(self, video_id):
        """Check the status of uploaded video"""
        try:
            logger.info(f"Checking upload status for video ID: {video_id}")
            
            token = self.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # TikTok provides status checking endpoint
            status_url = f"{self.base_url}/v1/post/publish/status/{video_id}"
            response = requests.get(status_url, headers=headers)
            response.raise_for_status()
            
            status_data = response.json()
            logger.info(f"Upload status: {status_data}")
            
            return status_data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking status: {e}")
            raise


def main():
    """Test the TikTok uploader"""
    uploader = TikTokUploader()
    
    # Example: Upload a video
    # video_path = "path/to/video.mp4"
    # result = uploader.upload_video(
    #     video_path,
    #     title="My AI Generated Video",
    #     description="Created with AI, awesome content!"
    # )
    # print(result)
    
    print("TikTok Uploader initialized. Configure .env file with TikTok credentials to use.")


if __name__ == "__main__":
    main()
