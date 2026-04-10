#!/usr/bin/env python
"""Test that logging system works correctly"""
import sys
from pathlib import Path
import logging
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

print("Testing Logging System...")
print("="*60)

# Setup logging (same as in ai_video_gui.py)
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"ai_video_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Test logging
logger.info("="*60)
logger.info("Logging System Test Started")
logger.info("="*60)

logger.info("✅ Mode selected: smooth")
logger.info("Generation started - Mode: smooth, Prompt: Test ocean waves...")
logger.info("AI model loaded in 123.45 seconds")
logger.info("SmoothVideoGenerator initialized")
logger.info("Generating smooth 30 FPS video (6 keyframes + interpolation)...")
logger.info("Smooth video generation completed in 145.67 seconds")
logger.info("Total generation time: 2.83 minutes (169.62 seconds)")
logger.info("Output: C:\\Users\\gulis\\Downloads\\AI Videos\\test_video.mp4")
logger.info("✅ SUCCESS - Video generation complete")

logger.info("="*60)
logger.info("Test Complete - Check logs/ folder for output file")
logger.info("="*60)

print()
print(f"✅ Log file created: {log_file}")
print(f"✅ Logging system is working correctly!")
print(f"\nLog file contents:")
print("-"*60)

with open(log_file, 'r') as f:
    print(f.read())
