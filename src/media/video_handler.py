"""Video Processing for ProFlow 240"""

import logging
from pathlib import Path
from typing import Optional, List

import cv2

logger = logging.getLogger(__name__)

# Display dimensions
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 480


class VideoHandler:
    """Handle video files for ProFlow 240"""
    
    def __init__(self, width: int = DISPLAY_WIDTH, height: int = DISPLAY_HEIGHT):
        self.width = width
        self.height = height
    
    def extract_frames(self, video_path: str, max_frames: int = 100) -> Optional[List[bytes]]:
        """
        Extract frames from video
        
        Args:
            video_path: path to video file
            max_frames: maximum number of frames to extract
        
        Returns:
            List of frame bytes or None if error
        """
        try:
            path = Path(video_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {video_path}")
            
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise RuntimeError(f"Cannot open video: {video_path}")
            
            frames = []
            frame_count = 0
            
            while frame_count < max_frames:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Resize frame
                frame = cv2.resize(frame, (self.width, self.height))
                
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to bytes
                frame_bytes = frame.tobytes()
                frames.append(frame_bytes)
                
                frame_count += 1
            
            cap.release()
            
            logger.info(f"Extracted {len(frames)} frames from video")
            return frames if frames else None
            
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            return None
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        Get video information
        
        Args:
            video_path: path to video file
        
        Returns:
            dict with video info or None if error
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise RuntimeError(f"Cannot open video: {video_path}")
            
            info = {
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
            }
            
            cap.release()
            
            logger.info(f"Video info: {info['width']}x{info['height']} @ {info['fps']}fps, {info['frame_count']} frames")
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
