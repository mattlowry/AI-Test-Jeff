"""
Media viewer widget for displaying images and videos
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea,
                            QPushButton, QFileDialog, QHBoxLayout,
                            QFrame, QStyle)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QCursor, QIcon


class MediaViewer(QWidget):
    """Widget for viewing images and videos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_media = None
        self.media_list = []  # List to store all loaded media files
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout with proper margins and spacing
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Title with better styling
        title_label = QLabel("Media Viewer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title_label)

        # Scroll area for media content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(350)  # Increased height
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)  # Remove frame for cleaner look

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # Media display label with modern styling
        self.media_label = QLabel()
        self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.media_label.setMinimumSize(QSize(450, 300))  # Larger size
        self.media_label.setText("No media loaded")
        self.media_label.setStyleSheet("background-color: rgba(0, 0, 0, 0.05); border-radius: 8px; padding: 10px;")
        self.content_layout.addWidget(self.media_label)

        # Thumbnail gallery for multiple images
        thumbnail_section = QWidget()
        thumbnail_section_layout = QVBoxLayout(thumbnail_section)
        thumbnail_section_layout.setContentsMargins(0, 5, 0, 5)
        thumbnail_section_layout.setSpacing(5)

        # Add gallery label
        gallery_label = QLabel("Image Gallery")
        gallery_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        gallery_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        thumbnail_section_layout.addWidget(gallery_label)

        # Thumbnail layout with better spacing
        self.thumbnail_layout = QHBoxLayout()
        self.thumbnail_layout.setSpacing(8)
        self.thumbnail_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add thumbnail scroll area with better styling
        thumbnail_scroll = QScrollArea()
        thumbnail_scroll.setWidgetResizable(True)
        thumbnail_scroll.setMaximumHeight(85)
        thumbnail_scroll.setMinimumHeight(85)
        thumbnail_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        thumbnail_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        thumbnail_scroll.setStyleSheet("border-radius: 4px;")

        # Thumbnail widget
        self.thumbnail_widget = QWidget()
        self.thumbnail_widget.setLayout(self.thumbnail_layout)
        thumbnail_scroll.setWidget(self.thumbnail_widget)

        thumbnail_section_layout.addWidget(thumbnail_scroll)
        self.content_layout.addWidget(thumbnail_section)

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

        # Buttons layout with better spacing
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        button_layout.setContentsMargins(0, 5, 0, 5)
        button_layout.setSpacing(10)

        # Import button with better styling and icon
        import_button = QPushButton("Import Media")
        import_button.setMinimumWidth(120)
        import_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        import_button.setIconSize(QSize(20, 20))
        import_button.clicked.connect(self.import_media)
        button_layout.addWidget(import_button)

        # Clear button with icon
        clear_button = QPushButton("Clear")
        clear_button.setMinimumWidth(80)
        clear_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        clear_button.setIconSize(QSize(20, 20))
        clear_button.clicked.connect(self.clear_media)
        button_layout.addWidget(clear_button)

        # Add stretch to push the media count to the right
        button_layout.addStretch()

        # Media count label with better styling
        self.media_count_label = QLabel("Media: 0 files")
        self.media_count_label.setStyleSheet("padding: 5px; font-weight: bold;")
        button_layout.addWidget(self.media_count_label)

        layout.addWidget(button_section)

        # Status bar section
        status_section = QWidget()
        status_layout = QHBoxLayout(status_section)
        status_layout.setContentsMargins(5, 0, 5, 0)

        # Status label with better styling
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("padding: 3px; font-style: italic;")
        status_layout.addWidget(self.status_label)

        layout.addWidget(status_section)
        
    def load_media(self, file_path):
        """Load media file from the given path"""
        if not os.path.exists(file_path):
            self.status_label.setText(f"Error: File not found: {file_path}")
            return

        self.current_media = file_path

        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        # Add to media list if not already present
        if file_path not in self.media_list:
            self.media_list.append(file_path)

            # Create thumbnail for the gallery
            self.add_thumbnail(file_path)

            # Update the media count
            self.media_count_label.setText(f"Media: {len(self.media_list)} files")

        # Handle different file types
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            self.load_image(file_path)
            # Update parent tab if needed
            if hasattr(self.parent(), "project_data") and file_path not in self.parent().project_data.get("media_files", []):
                self.parent().project_data["media_files"].append(file_path)
                self.status_label.setText(f"Added image to project: {os.path.basename(file_path)}")
                print(f"Added image to project from media viewer: {file_path}")

        elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
            self.load_video(file_path)
            # Update parent tab if needed
            if hasattr(self.parent(), "project_data") and file_path not in self.parent().project_data.get("media_files", []):
                self.parent().project_data["media_files"].append(file_path)
                self.status_label.setText(f"Added video to project: {os.path.basename(file_path)}")
                print(f"Added video to project from media viewer: {file_path}")
        else:
            self.media_label.setText(f"Unsupported file format: {ext}")
            self.status_label.setText(f"Error: Unsupported file format: {ext}")
            
    def load_image(self, file_path):
        """Load and display an image"""
        if not os.path.exists(file_path):
            self.media_label.setText(f"File not found: {file_path}")
            self.status_label.setText(f"Error: File not found: {os.path.basename(file_path)}")
            print(f"Error: Image file not found: {file_path}")
            return

        # Print debug info
        print(f"Loading image from path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")

        # Use QImage first to diagnose issues
        image = QImage(file_path)
        if image.isNull():
            self.media_label.setText(f"Failed to load image: {file_path}")
            self.status_label.setText(f"Error: Failed to load image: {os.path.basename(file_path)}")
            print(f"Error: QImage failed to load: {file_path}")
            return

        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(image)

        if not pixmap.isNull():
            # Scale pixmap to fit the label while maintaining aspect ratio
            pixmap = pixmap.scaled(
                self.media_label.width(),
                self.media_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.media_label.setPixmap(pixmap)
            self.status_label.setText(f"Loaded image: {os.path.basename(file_path)}")
            print(f"Successfully loaded image: {file_path}, size: {pixmap.width()}x{pixmap.height()}")
        else:
            self.media_label.setText(f"Failed to load image: {file_path}")
            self.status_label.setText(f"Error: Failed to load image: {os.path.basename(file_path)}")
            print(f"Error: Failed to load image: {file_path}")
            
    def load_video(self, file_path):
        """Load and display a video
        
        Note: This is a placeholder. For actual video playback, you would need
        additional libraries like PyQt6 Multimedia or python-vlc.
        """
        self.media_label.setText(f"Video preview: {os.path.basename(file_path)}\n\nVideo playback would be implemented here using PyQt6 Multimedia or VLC.")
        self.status_label.setText(f"Loaded video: {os.path.basename(file_path)}")
        print(f"Loaded video (preview only): {file_path}")
        
    def import_media(self):
        """Import media from file dialog with multiple file selection"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Import Media (Multiple Files Supported)", "",
            "Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov);;All Files (*)"
        )

        if file_paths:
            # Load the last file selected to display in the viewer
            last_file = file_paths[-1]
            self.load_media(last_file)

            # If this is part of a project tab, tell the parent to handle the imports
            if hasattr(self.parent(), "import_media"):
                for file_path in file_paths:
                    self.parent().import_media(file_path)

                # Update status with count of imported files
                self.status_label.setText(f"Imported {len(file_paths)} media files")
                print(f"Imported {len(file_paths)} media files")
            
    def add_thumbnail(self, file_path):
        """Add a thumbnail to the gallery"""
        if not os.path.exists(file_path):
            return

        # Create a thumbnail label (clickable)
        thumb_label = QLabel()
        thumb_label.setFixedSize(60, 60)
        thumb_label.setFrameShape(QFrame.Shape.Box)
        thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Connect mouse press event using setProperty and installEventFilter
        thumb_label.setProperty("file_path", file_path)
        thumb_label.installEventFilter(self)

        # Handle different file types
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            # Load image and create thumbnail
            image = QImage(file_path)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                pixmap = pixmap.scaled(
                    50, 50,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                thumb_label.setPixmap(pixmap)
            else:
                thumb_label.setText("Error")
        else:
            # For video, just show a text label
            thumb_label.setText("Video")

        # Add to thumbnail layout
        self.thumbnail_layout.addWidget(thumb_label)

    def eventFilter(self, obj, event):
        """Handle events for thumbnail labels"""
        if event.type() == event.Type.MouseButtonPress:
            if hasattr(obj, 'property') and obj.property("file_path"):
                file_path = obj.property("file_path")
                # Load the selected file
                if os.path.exists(file_path):
                    self.current_media = file_path

                    # Display the selected media
                    _, ext = os.path.splitext(file_path)
                    ext = ext.lower()

                    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                        self.load_image(file_path)
                    elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
                        self.load_video(file_path)

                return True
        return super().eventFilter(obj, event)

    def clear_media(self):
        """Clear the current media display and gallery"""
        self.current_media = None
        self.media_label.clear()
        self.media_label.setText("No media loaded")

        # Clear the media list
        self.media_list.clear()

        # Clear thumbnails
        for i in reversed(range(self.thumbnail_layout.count())):
            widget = self.thumbnail_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Update media count
        self.media_count_label.setText("Media: 0 files")
        self.status_label.setText("Media cleared")
        print("Media viewer cleared")