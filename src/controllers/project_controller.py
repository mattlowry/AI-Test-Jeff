"""
Project controller for handling project operations
"""

import json
import os
from database.database_manager import DatabaseManager


class ProjectController:
    """Controller for handling project operations"""
    
    def __init__(self):
        """Initialize the project controller"""
        self.db_manager = DatabaseManager()
        
    def save_project(self, file_path, project_data):
        """Save a project to a file"""
        try:
            # Make sure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save to JSON file
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=4)
                
            # Also save to database
            self.db_manager.save_project(project_data)
                
            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
            
    def load_project(self, file_path):
        """Load a project from a file"""
        try:
            # Load from JSON file
            with open(file_path, 'r') as f:
                project_data = json.load(f)
                
            return project_data
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
            
    def delete_project(self, project_id):
        """Delete a project from the database"""
        try:
            self.db_manager.delete_project(project_id)
            return True
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False
            
    def list_projects(self):
        """List all projects in the database"""
        try:
            return self.db_manager.get_all_projects()
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []