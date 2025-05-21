"""
Media handler for managing images and videos in the Electrical Estimator application
"""

import os
import shutil
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from PyQt6.QtGui import QPixmap, QImage

from utils.image_utils import (
    get_image_format, 
    load_image_as_pixmap, 
    resize_image,
    pixmap_to_base64
)
from utils.video_utils import (
    get_video_format,
    get_video_thumbnail,
    extract_frames,
    get_video_metadata
)


class MediaHandler:
    """
    Handler for managing media files (images and videos)
    
    This class provides methods for:
    - Loading and managing media files
    - Converting between formats
    - Extracting data for AI processing
    """
    
    def __init__(self, media_dir: Optional[str] = None):
        """
        Initialize the media handler
        
        Args:
            media_dir: Directory to store copied media files. If None, will use a default path.
        """
        # Set up media directory
        if media_dir is None:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.media_dir = os.path.join(current_dir, "project_media")
        else:
            self.media_dir = media_dir
            
        # Create the directory if it doesn't exist
        os.makedirs(self.media_dir, exist_ok=True)
        
        print(f"MediaHandler initialized with media_dir: {self.media_dir}")
    
    def is_media_file(self, file_path: str) -> bool:
        """
        Check if a file is a supported media file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if supported, False otherwise
        """
        if not file_path or not os.path.exists(file_path):
            print(f"Media file does not exist: {file_path}")
            return False
            
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Check if it's a supported format
        is_supported = ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.mp4', '.avi', '.mov', '.wmv']
        if is_supported:
            print(f"Identified valid media file: {file_path} (type: {ext})")
        else:
            print(f"Unsupported media format: {file_path} (type: {ext})")
        return is_supported
    
    def is_image_file(self, file_path: str) -> bool:
        """
        Check if a file is a supported image file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if it's an image, False otherwise
        """
        if not file_path or not os.path.exists(file_path):
            print(f"Image file does not exist: {file_path}")
            return False
            
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Check if it's a supported image format
        is_image = ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        if is_image:
            print(f"Identified valid image file: {file_path} (type: {ext})")
        return is_image
    
    def is_video_file(self, file_path: str) -> bool:
        """
        Check if a file is a supported video file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if it's a video, False otherwise
        """
        if not file_path or not os.path.exists(file_path):
            print(f"Video file does not exist: {file_path}")
            return False
            
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Check if it's a supported video format
        is_video = ext in ['.mp4', '.avi', '.mov', '.wmv']
        if is_video:
            print(f"Identified valid video file: {file_path} (type: {ext})")
        return is_video
    
    def copy_media_to_project(self, file_path: str, project_id: str) -> Optional[str]:
        """
        Copy a media file to the project media directory
        
        Args:
            file_path: Original file path
            project_id: Project identifier
            
        Returns:
            New file path if successful, None otherwise
        """
        try:
            # Create project directory if it doesn't exist
            project_dir = os.path.join(self.media_dir, project_id)
            os.makedirs(project_dir, exist_ok=True)
            
            # Generate a unique filename
            filename = os.path.basename(file_path)
            base, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{base}_{timestamp}{ext}"
            
            # Set the destination path
            dest_path = os.path.join(project_dir, new_filename)
            
            # Copy the file
            shutil.copy2(file_path, dest_path)
            
            return dest_path
        except Exception as e:
            print(f"Error copying media file: {e}")
            return None
    
    def load_media(self, file_path: str) -> Dict[str, Any]:
        """
        Load a media file and return its metadata
        
        Args:
            file_path: Path to the media file
            
        Returns:
            Dictionary with media information
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
            
        if self.is_image_file(file_path):
            return self._load_image(file_path)
        elif self.is_video_file(file_path):
            return self._load_video(file_path)
        else:
            return {"error": f"Unsupported file format: {file_path}"}
    
    def _load_image(self, file_path: str) -> Dict[str, Any]:
        """
        Load an image file and return its metadata
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dictionary with image information
        """
        pixmap = load_image_as_pixmap(file_path)
        if pixmap is None:
            return {"error": f"Failed to load image: {file_path}"}
            
        # Get image information
        return {
            "type": "image",
            "format": get_image_format(file_path),
            "path": file_path,
            "filename": os.path.basename(file_path),
            "width": pixmap.width(),
            "height": pixmap.height(),
            "pixmap": pixmap,
            "base64": None  # Will be generated on demand
        }
    
    def _load_video(self, file_path: str) -> Dict[str, Any]:
        """
        Load a video file and return its metadata
        
        Args:
            file_path: Path to the video file
            
        Returns:
            Dictionary with video information
        """
        # Get video metadata
        metadata = get_video_metadata(file_path)
        
        # Generate thumbnail
        thumbnail_path = get_video_thumbnail(file_path)
        thumbnail = None
        if os.path.exists(thumbnail_path):
            thumbnail = load_image_as_pixmap(thumbnail_path)
        
        # Return video information
        return {
            "type": "video",
            "format": get_video_format(file_path),
            "path": file_path,
            "filename": os.path.basename(file_path),
            "width": metadata.get("width"),
            "height": metadata.get("height"),
            "duration": metadata.get("duration"),
            "fps": metadata.get("fps"),
            "thumbnail": thumbnail,
            "thumbnail_path": thumbnail_path,
            "metadata": metadata
        }
    
    def get_media_for_ai(self, file_path: str, max_size: Tuple[int, int] = (1024, 1024)) -> Dict[str, Any]:
        """
        Prepare media for AI processing
        
        Args:
            file_path: Path to the media file
            max_size: Maximum dimensions (width, height) for images
            
        Returns:
            Dictionary with media data for AI
        """
        if self.is_image_file(file_path):
            return self._prepare_image_for_ai(file_path, max_size)
        elif self.is_video_file(file_path):
            return self._prepare_video_for_ai(file_path, max_size)
        else:
            return {"error": f"Unsupported file format: {file_path}"}
    
    def _prepare_image_for_ai(self, file_path: str, max_size: Tuple[int, int]) -> Dict[str, Any]:
        """
        Prepare an image for AI processing
        
        Args:
            file_path: Path to the image file
            max_size: Maximum dimensions (width, height)
            
        Returns:
            Dictionary with image data for AI
        """
        # Load the image
        media_data = self._load_image(file_path)
        if "error" in media_data:
            return media_data
            
        # Resize if needed
        pixmap = media_data["pixmap"]
        if pixmap.width() > max_size[0] or pixmap.height() > max_size[1]:
            pixmap = resize_image(pixmap, max_size[0], max_size[1])
            
        # Convert to base64
        base64_data = pixmap_to_base64(pixmap, media_data["format"])
        
        # Return data for AI
        return {
            "type": "image",
            "format": media_data["format"],
            "path": file_path,
            "base64": base64_data,
            "width": pixmap.width(),
            "height": pixmap.height()
        }
    
    def _prepare_video_for_ai(self, file_path: str, max_size: Tuple[int, int]) -> Dict[str, Any]:
        """
        Prepare a video for AI processing by extracting frames
        
        Args:
            file_path: Path to the video file
            max_size: Maximum dimensions (width, height) for frames
            
        Returns:
            Dictionary with video frame data for AI
        """
        # Extract key frames (temporary directory)
        import tempfile
        temp_dir = tempfile.mkdtemp(prefix="video_frames_")
        
        # Extract frames (1 frame per second)
        frame_paths = extract_frames(file_path, temp_dir, frame_rate=1)
        
        # Prepare frames for AI
        frames = []
        for frame_path in frame_paths:
            if os.path.exists(frame_path):  # Some frames might be placeholders
                frame_data = self._prepare_image_for_ai(frame_path, max_size)
                frames.append(frame_data)
        
        # Get video metadata
        metadata = get_video_metadata(file_path)
        
        # Return data for AI
        return {
            "type": "video",
            "format": get_video_format(file_path),
            "path": file_path,
            "frames": frames,
            "frame_count": len(frames),
            "duration": metadata.get("duration"),
            "metadata": metadata
        }
    
    def cleanup_temp_files(self) -> None:
        """Clean up any temporary files created for media processing"""
        # Additional cleanup code could be added here if needed
        pass