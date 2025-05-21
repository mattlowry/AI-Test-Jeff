"""
Project model for the Electrical Estimator application
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class ProjectModel:
    """
    Project model class for storing and managing project data
    
    Attributes:
        id: Optional project ID (if stored in database)
        name: Project name
        created_at: Creation timestamp
        updated_at: Last update timestamp
        media_files: List of media file paths
        chat_history: List of chat messages
        estimation_data: Dictionary of estimation data
    """
    
    def __init__(
        self,
        name: str = "New Project",
        project_id: Optional[int] = None,
        media_files: Optional[List[str]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
        estimation_data: Optional[Dict[str, Any]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        """
        Initialize a new project
        
        Args:
            name: Project name
            project_id: Optional project ID
            media_files: List of media file paths
            chat_history: List of chat messages
            estimation_data: Dictionary of estimation data
            created_at: Creation timestamp (ISO format)
            updated_at: Last update timestamp (ISO format)
        """
        self.id = project_id
        self.name = name
        self.media_files = media_files or []
        self.chat_history = chat_history or []
        self.estimation_data = estimation_data or {"items": [], "total": 0.0, "notes": ""}
        
        # Set timestamps
        now = datetime.now().isoformat()
        self.created_at = created_at or now
        self.updated_at = updated_at or now
    
    def add_media_file(self, file_path: str) -> None:
        """
        Add a media file to the project
        
        Args:
            file_path: Path to the media file
        """
        if file_path not in self.media_files:
            self.media_files.append(file_path)
            self.updated_at = datetime.now().isoformat()
    
    def remove_media_file(self, file_path: str) -> bool:
        """
        Remove a media file from the project
        
        Args:
            file_path: Path to the media file
            
        Returns:
            True if file was removed, False if not found
        """
        if file_path in self.media_files:
            self.media_files.remove(file_path)
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def add_chat_message(self, role: str, content: str) -> None:
        """
        Add a chat message to the project history
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        self.chat_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.updated_at = datetime.now().isoformat()
    
    def update_estimation_data(self, estimation_data: Dict[str, Any]) -> None:
        """
        Update the estimation data
        
        Args:
            estimation_data: New estimation data
        """
        self.estimation_data = estimation_data
        self.updated_at = datetime.now().isoformat()
    
    def add_estimation_item(self, item_data: Dict[str, Any]) -> None:
        """
        Add an item to the estimation
        
        Args:
            item_data: Item data dictionary
        """
        self.estimation_data["items"].append(item_data)
        # Update total
        self._recalculate_total()
        self.updated_at = datetime.now().isoformat()
    
    def update_estimation_item(self, index: int, item_data: Dict[str, Any]) -> bool:
        """
        Update an estimation item
        
        Args:
            index: Index of the item to update
            item_data: New item data
            
        Returns:
            True if item was updated, False if index is out of range
        """
        if 0 <= index < len(self.estimation_data["items"]):
            self.estimation_data["items"][index] = item_data
            self._recalculate_total()
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def remove_estimation_item(self, index: int) -> bool:
        """
        Remove an estimation item
        
        Args:
            index: Index of the item to remove
            
        Returns:
            True if item was removed, False if index is out of range
        """
        if 0 <= index < len(self.estimation_data["items"]):
            self.estimation_data["items"].pop(index)
            self._recalculate_total()
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def _recalculate_total(self) -> None:
        """Recalculate the total cost of all estimation items"""
        self.estimation_data["total"] = sum(
            item["quantity"] * item["unit_price"] 
            for item in self.estimation_data["items"]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the project to a dictionary for serialization
        
        Returns:
            Dictionary representation of the project
        """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "media_files": self.media_files,
            "chat_history": self.chat_history,
            "estimation_data": self.estimation_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectModel':
        """
        Create a project from a dictionary
        
        Args:
            data: Dictionary representation of the project
            
        Returns:
            ProjectModel instance
        """
        return cls(
            name=data.get("name", "Imported Project"),
            project_id=data.get("id"),
            media_files=data.get("media_files", []),
            chat_history=data.get("chat_history", []),
            estimation_data=data.get("estimation_data", {"items": [], "total": 0.0, "notes": ""}),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def save_to_file(self, file_path: str) -> bool:
        """
        Save the project to a JSON file
        
        Args:
            file_path: Path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Update timestamp
            self.updated_at = datetime.now().isoformat()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Convert to dictionary and save as JSON
            with open(file_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving project to file: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, file_path: str) -> Optional['ProjectModel']:
        """
        Load a project from a JSON file
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            ProjectModel instance if successful, None otherwise
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return cls.from_dict(data)
        except Exception as e:
            print(f"Error loading project from file: {e}")
            return None