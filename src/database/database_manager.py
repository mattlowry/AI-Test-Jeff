"""
Database manager for SQLite operations
"""

import sqlite3
import os
import json
from datetime import datetime


class DatabaseManager:
    """Manager for SQLite database operations"""
    
    def __init__(self, db_path='database.db'):
        """Initialize the database manager"""
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set the database path to be in the same directory
        self.db_path = os.path.join(current_dir, db_path)
        
        # Initialize the database
        self.initialize_db()
        
    def initialize_db(self):
        """Initialize the database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create projects table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                data TEXT NOT NULL
            )
            ''')
            
            # Create media table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
            ''')
            
            # Create chat_messages table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
            ''')
            
            # Create estimations table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS estimations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                total REAL NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
            ''')
            
            # Create estimation_items table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS estimation_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estimation_id INTEGER NOT NULL,
                item TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY (estimation_id) REFERENCES estimations(id)
            )
            ''')
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        
    def save_project(self, project_data):
        """Save a project to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            
            # Check if project already exists
            cursor.execute(
                "SELECT id FROM projects WHERE name = ?",
                (project_data["name"],)
            )
            result = cursor.fetchone()
            
            if result:
                # Update existing project
                project_id = result[0]
                cursor.execute(
                    "UPDATE projects SET updated_at = ?, data = ? WHERE id = ?",
                    (now, json.dumps(project_data), project_id)
                )
            else:
                # Insert new project
                cursor.execute(
                    "INSERT INTO projects (name, created_at, updated_at, data) VALUES (?, ?, ?, ?)",
                    (project_data["name"], now, now, json.dumps(project_data))
                )
                project_id = cursor.lastrowid
                
            # Save media files
            for media_file in project_data.get("media_files", []):
                # Determine media type
                media_type = "image" if media_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) else "video"
                
                # Check if media already exists
                cursor.execute(
                    "SELECT id FROM media WHERE project_id = ? AND file_path = ?",
                    (project_id, media_file)
                )
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO media (project_id, file_path, type, created_at) VALUES (?, ?, ?, ?)",
                        (project_id, media_file, media_type, now)
                    )
            
            # Save chat history
            for message in project_data.get("chat_history", []):
                cursor.execute(
                    "INSERT INTO chat_messages (project_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                    (project_id, message["role"], message["content"], now)
                )
            
            # Save estimation data
            estimation_data = project_data.get("estimation_data", {})
            if estimation_data:
                cursor.execute(
                    "INSERT INTO estimations (project_id, total, notes, created_at) VALUES (?, ?, ?, ?)",
                    (project_id, estimation_data.get("total", 0.0), estimation_data.get("notes", ""), now)
                )
                estimation_id = cursor.lastrowid
                
                for item in estimation_data.get("items", []):
                    cursor.execute(
                        "INSERT INTO estimation_items (estimation_id, item, quantity, unit, unit_price) VALUES (?, ?, ?, ?, ?)",
                        (estimation_id, item["item"], item["quantity"], item["unit"], item["unit_price"])
                    )
            
            conn.commit()
            conn.close()
            
            return True
        except sqlite3.Error as e:
            print(f"Database error saving project: {e}")
            return False
            
    def get_project(self, project_id):
        """Get a project by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT data FROM projects WHERE id = ?",
                (project_id,)
            )
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
        except sqlite3.Error as e:
            print(f"Database error getting project: {e}")
            return None
            
    def get_all_projects(self):
        """Get all projects"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, name, created_at, updated_at FROM projects ORDER BY updated_at DESC"
            )
            results = cursor.fetchall()
            
            conn.close()
            
            projects = []
            for row in results:
                projects.append({
                    "id": row[0],
                    "name": row[1],
                    "created_at": row[2],
                    "updated_at": row[3]
                })
            
            return projects
        except sqlite3.Error as e:
            print(f"Database error getting all projects: {e}")
            return []
            
    def delete_project(self, project_id):
        """Delete a project"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete related records first (due to foreign key constraints)
            cursor.execute("DELETE FROM estimation_items WHERE estimation_id IN (SELECT id FROM estimations WHERE project_id = ?)", (project_id,))
            cursor.execute("DELETE FROM estimations WHERE project_id = ?", (project_id,))
            cursor.execute("DELETE FROM chat_messages WHERE project_id = ?", (project_id,))
            cursor.execute("DELETE FROM media WHERE project_id = ?", (project_id,))
            
            # Delete the project itself
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except sqlite3.Error as e:
            print(f"Database error deleting project: {e}")
            return False