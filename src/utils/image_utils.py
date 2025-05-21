"""
Utility functions for image processing
"""

import os
import io
from typing import Tuple, Optional, List
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice


def get_image_format(file_path: str) -> str:
    """
    Get the format of an image based on its file extension
    
    Args:
        file_path: Path to the image file
        
    Returns:
        The image format as a string (e.g., "png", "jpg")
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.jpg' or ext == '.jpeg':
        return 'jpg'
    elif ext == '.png':
        return 'png'
    elif ext == '.bmp':
        return 'bmp'
    elif ext == '.gif':
        return 'gif'
    else:
        return 'unknown'


def load_image_as_pixmap(file_path: str) -> Optional[QPixmap]:
    """
    Load an image file as a QPixmap
    
    Args:
        file_path: Path to the image file
        
    Returns:
        QPixmap object if successful, None otherwise
    """
    if not os.path.exists(file_path):
        print(f"Image file not found: {file_path}")
        return None
        
    pixmap = QPixmap(file_path)
    
    if pixmap.isNull():
        print(f"Failed to load image: {file_path}")
        return None
        
    return pixmap


def resize_image(pixmap: QPixmap, max_width: int, max_height: int) -> QPixmap:
    """
    Resize an image pixmap while maintaining aspect ratio
    
    Args:
        pixmap: The QPixmap to resize
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        
    Returns:
        Resized QPixmap
    """
    # If image is smaller than max dimensions, no need to resize
    if pixmap.width() <= max_width and pixmap.height() <= max_height:
        return pixmap
        
    # Scale to fit within the bounds while preserving aspect ratio
    return pixmap.scaled(
        max_width, 
        max_height,
        aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
        transformMode=Qt.TransformationMode.SmoothTransformation
    )


def pixmap_to_base64(pixmap: QPixmap, format: str = 'png') -> str:
    """
    Convert a QPixmap to a base64 encoded string
    
    Args:
        pixmap: The QPixmap to convert
        format: The image format to use (e.g., 'png', 'jpg')
        
    Returns:
        Base64 encoded string of the image
    """
    import base64
    
    # Create a QByteArray to store the image data
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    
    # Save the pixmap to the buffer in the specified format
    pixmap.save(buffer, format.upper())
    
    # Get the raw data and encode as base64
    image_data = byte_array.data()
    base64_data = base64.b64encode(image_data).decode('utf-8')
    
    return base64_data


def extract_dominant_colors(pixmap: QPixmap, num_colors: int = 5) -> List[Tuple[int, int, int]]:
    """
    Extract the dominant colors from an image
    
    Args:
        pixmap: The QPixmap to analyze
        num_colors: Number of dominant colors to extract
        
    Returns:
        List of tuples containing RGB values of dominant colors
    """
    # Convert pixmap to QImage
    image = pixmap.toImage()
    
    # Simple implementation - sample pixels
    colors = {}
    width = image.width()
    height = image.height()
    
    # Sample every 10th pixel
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            # Get color at pixel
            color = image.pixelColor(x, y)
            rgb = (color.red(), color.green(), color.blue())
            
            # Increment count for this color
            if rgb in colors:
                colors[rgb] += 1
            else:
                colors[rgb] = 1
    
    # Sort colors by frequency and return top N
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    
    # Return just the RGB values of the top colors
    return [color for color, _ in sorted_colors[:num_colors]]