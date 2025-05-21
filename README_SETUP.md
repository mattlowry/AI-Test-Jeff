# Setting Up the Electrical Estimator Application

This guide provides step-by-step instructions for setting up and running the Electrical Estimator application.

## Prerequisites

- Python 3.8 or newer
- Pip package manager
- API keys for Claude and Google Cloud (optional for Google APIs)

## Installation Steps

1. **Clone or download the repository**

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**

   The application requires API keys for the Claude API and optionally for Google Cloud services. 
   
   Create a `.env` file in the root directory with the following content:

   ```
   # Claude API Key (Required)
   CLAUDE_API_KEY="your_claude_api_key_here"

   # Google Cloud API Credentials (Optional)
   GOOGLE_APPLICATION_CREDENTIALS="path/to/your/google-credentials.json"
   ```

   Replace the placeholder values with your actual API keys.

4. **Google Cloud credentials (Optional)**

   If you want to use the Google Cloud Vision and Video Intelligence APIs:
   
   - Create a Google Cloud account if you don't have one
   - Create a new project
   - Enable the Vision API and Video Intelligence API
   - Create a service account and download the JSON credentials file
   - Set the path to this file in the `.env` file as shown above

## Running the Application

Run the application using:

```bash
python src/main.py
```

## Using the Application

### Creating a New Project

1. Launch the application
2. A new project tab will be created by default
3. Use the "Import Media" button to upload images or videos
4. The imported media will appear in the media viewer

### AI-Assisted Analysis

1. After importing media, use the chat interface to ask questions about the electrical work
2. Examples of questions:
   - "What electrical components do you see in this image?"
   - "How many outlets would be needed for this room?"
   - "Estimate the cost for rewiring this panel"

### Creating Estimates

1. Use the estimation panel on the right side to add items
2. Click "Add Item" to manually add components and costs
3. Items can be edited or removed as needed
4. The total cost is calculated automatically

### Saving and Loading Projects

1. Use File -> Save Project to save your current project
2. Use File -> Open Project to load a previously saved project
3. Projects are saved in a custom `.eep` format (Electrical Estimator Project)

## Troubleshooting

### API Connection Issues

- Verify that your API keys are correctly set in the `.env` file
- Check your internet connection
- For Claude API: Ensure your API key has not expired
- For Google Cloud: Verify that the APIs are enabled in your Google Cloud project

### Media Loading Problems

- Check that the file format is supported (PNG, JPG, JPEG, BMP for images; MP4, AVI, MOV for videos)
- Verify that the file is not corrupted
- For videos: The application uses OpenCV for processing - ensure it's correctly installed

## Development Notes

The application is structured in a modular way:

- `src/gui/`: UI components using PyQt6
- `src/api/`: API integrations for Claude and Google Cloud
- `src/models/`: Data models for projects and estimates
- `src/controllers/`: Business logic controllers
- `src/utils/`: Utility functions for image and video processing
- `src/database/`: Database management

If you're extending the application, follow this structure to maintain a clean architecture.

## License

This application is open-source software. See the LICENSE file for details.