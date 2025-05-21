# Electrical Estimator Application

A PyQt6 application for creating electrical estimates using AI image analysis.

## Overview

This application allows electrical contractors to:

1. Upload images or videos of electrical work
2. Use AI (Claude, Google Vision, Google Video Intelligence) to analyze the media
3. Generate detailed estimates for electrical work
4. Save and manage project estimates

## Project Structure

```
ElectricalEstimator/
├── requirements.txt
├── README.md
├── src/
│   ├── main.py                  # Application entry point
│   ├── gui/                     # PyQt6 GUI components
│   │   ├── main_window.py       # Main application window
│   │   ├── project_tab.py       # Project tab widget
│   │   ├── media_viewer.py      # Media viewing widget
│   │   ├── chat_widget.py       # Chat interface widget
│   │   └── estimation_widget.py # Estimation details widget
│   ├── models/                  # Data models
│   │   └── project_model.py     # (To be implemented)
│   ├── controllers/             # Controllers for business logic
│   │   └── project_controller.py# Project operations controller
│   ├── utils/                   # Utility functions
│   │   ├── image_utils.py       # Image processing utilities
│   │   └── video_utils.py       # Video processing utilities
│   ├── database/                # Database components
│   │   └── database_manager.py  # SQLite database manager
│   ├── media/                   # Media handlers
│   │   └── media_handler.py     # (To be implemented)
│   └── api/                     # API integrations
│       ├── claude_api.py        # Claude API integration
│       ├── google_vision_api.py # Google Vision API integration
│       └── google_video_api.py  # Google Video Intelligence integration
└── resources/                   # Application resources
    └── icons/                   # (To be added)
```

## Features

- **Project Management**: Create, save and load estimation projects
- **Media Integration**: Upload and analyze images and videos
- **AI Analysis**: Use Claude and Google Cloud APIs to analyze electrical systems
- **Chat Interface**: Interact with AI to refine estimates
- **Estimation Tools**: Build detailed electrical estimates with cost breakdowns
- **SQLite Database**: Local storage for project data

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up API keys:
   - Claude API key
   - Google Cloud API credentials (for Vision and Video Intelligence APIs)

## Usage

Run the application using:

```
python src/main.py
```

## API Requirements

### Claude API (Sonnet 3.7)

- **API Key**: Required for authentication
- **Endpoints**:
  - `https://api.anthropic.com/v1/messages` - For sending messages and receiving responses
- **Features**:
  - Text analysis
  - Image understanding
  - Multi-turn conversations

### Google Cloud Vision API

- **Credentials**: Google Cloud service account credentials
- **Features**:
  - Image labeling
  - Object detection
  - Text extraction (OCR)

### Google Cloud Video Intelligence API

- **Credentials**: Google Cloud service account credentials (same as Vision)
- **Features**:
  - Label detection
  - Object tracking
  - Shot detection

## Recommended Libraries

- **PyQt6**: Core UI framework
- **requests**: For API requests
- **anthropic**: Official Python client for Claude API
- **google-cloud-vision**: Google Cloud Vision API client
- **google-cloud-videointelligence**: Google Cloud Video Intelligence API client
- **python-dotenv**: For environment variable management
- **pillow**: For image processing
- **opencv-python**: For video processing (extracting frames, etc.)

## Development Notes

This is a prototype application with placeholder implementations for some components. 
The main focus is on establishing the architecture and core UI components.

Key areas for further development:
1. Implement actual API integrations with proper API keys
2. Complete the video processing functionality
3. Enhance the UI with more features and better styling
4. Implement more sophisticated estimation algorithms