#!/usr/bin/env python3
"""
Electrical Estimator Application
Main entry point for the application
"""

import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Main entry point for the application"""
    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    print(f"Loading .env from: {dotenv_path}")
    load_dotenv(dotenv_path)
    
    # Check if API key is loaded
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not claude_api_key:
        print("WARNING: CLAUDE_API_KEY not found in environment variables")
    else:
        print("CLAUDE_API_KEY loaded successfully")
    
    # Initialize Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Electrical Estimator")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()