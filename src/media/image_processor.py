"""Image Processing for ProFlow 240"""

import logging
from pathlib import Path
from typing import Optional

from PIL import Image, ImageOps, ImageEnhance
from PyQt6.QtGui import QPixmap, QImage
import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Display dimensions (adjust as needed)
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 480


class ImageProcessor:
    """Process images for ProFlow 240 display"""
    
    def __init__(self, width: int = DISPLAY_WIDTH, height: int = DISPLAY_HEIGHT):
        self.width = width
        self.height = height
    
    def load_image(self, image_path: str) -> Optional[QPixmap]:
        """
        Load and convert image to QPixmap
        
        Args:
            image_path: path to image file
        
        Returns:
            QPixmap or None if error
        """
        try:
            path = Path(image_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {image_path}")
            
            # Load with PIL
            img = Image.open(image_path)
            logger.info(f"Image loaded: {path.name} ({img.size[0]}x{img.size[1]})")
            
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (0, 0, 0))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize maintaining aspect ratio
            img.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)
            
            # Create new image with padding if needed
            resized_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            offset = ((self.width - img.size[0]) // 2, (self.height - img.size[1]) // 2)
            resized_img.paste(img, offset)
            
            # Convert to QPixmap
            qimg = QImage(resized_img.tobytes(), resized_img.width, resized_img.height,
                         resized_img.width * 3, QImage.Format.Format_RGB888)
            qpixmap = QPixmap.fromImage(qimg)
            
            logger.info(f"Image processed successfully")
            return qpixmap
            
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
    
    def process_for_device(self, image_path: str, brightness: int = 100,
                          contrast: int = 100) -> Optional[bytes]:
        """
        Process image and convert to device format
        
        Args:
            image_path: path to image
            brightness: brightness level (0-200, 100=normal)
            contrast: contrast level (0-200, 100=normal)
        
        Returns:
            bytes or None if error
        """
        try:
            # Load image
            img = Image.open(image_path)
            
            # Convert to RGB
            if img.mode != 'RGB':
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (0, 0, 0))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert('RGB')
            
            # Resize
            img.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)
            resized_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            offset = ((self.width - img.size[0]) // 2, (self.height - img.size[1]) // 2)
            resized_img.paste(img, offset)
            
            # Adjust brightness
            if brightness != 100:
                enhancer = ImageEnhance.Brightness(resized_img)
                resized_img = enhancer.enhance(brightness / 100.0)
            
            # Adjust contrast
            if contrast != 100:
                enhancer = ImageEnhance.Contrast(resized_img)
                resized_img = enhancer.enhance(contrast / 100.0)
            
            # Convert to bytes (RGB565 format for typical embedded displays)
            img_array = np.array(resized_img, dtype=np.uint8)
            
            # Convert RGB to RGB565 (16-bit color)
            r = (img_array[:, :, 0] >> 3) & 0x1F
            g = (img_array[:, :, 1] >> 2) & 0x3F
            b = (img_array[:, :, 2] >> 3) & 0x1F
            
            rgb565 = ((r << 11) | (g << 5) | b).astype(np.uint16)
            
            # Convert to bytes
            return rgb565.tobytes()
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return None
