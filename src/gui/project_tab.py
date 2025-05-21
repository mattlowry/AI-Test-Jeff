"""
Project tab widget for the Electrical Estimator application
"""

import os
import sys
import re
import traceback
from dotenv import load_dotenv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                            QTextEdit, QListWidget, QPushButton, QLabel,
                            QScrollArea, QLineEdit, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QPixmap, QImage

from gui.media_viewer import MediaViewer
from gui.chat_widget import ChatWidget
from gui.estimation_widget import EstimationWidget
from api.claude_api import ClaudeAPI
from api.gemini_api import GeminiAPI
from api.google_vision_api import GoogleVisionAPI
from media.media_handler import MediaHandler


class ProjectTab(QWidget):
    """Project tab widget that contains the main project interface"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_data = {
            "name": "New Project",
            "media_files": [],
            "chat_history": [],
            "estimation_data": {},
            "pricing_data": {
                "hourly_rate": 75.00,
                "increment": 15
            }
        }

        # No longer need animation variables - now handled by chat_widget
        
        # Ensure environment variables are loaded
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
        load_dotenv(dotenv_path)
        
        # Flag to track which API to use
        # 0 = Gemini, 1 = Claude, 2 = Vision API
        self.api_choice = 0  # Default to Gemini API
        self.gemini_api_initialized = False
        self.claude_api_initialized = False
        self.vision_api_initialized = False

        # Initialize Gemini API client
        try:
            # Try to get key directly from environment
            api_key = os.environ.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

            # Initialize with the key
            self.gemini_api = GeminiAPI(api_key=api_key)
            self.gemini_api_initialized = True
            print("Successfully initialized Gemini API")
        except Exception as e:
            self.gemini_api_initialized = False
            err_msg = f"Failed to initialize Gemini API: {str(e)}\n\nCheck your API key in the .env file."
            print(f"ERROR: {err_msg}")
            QMessageBox.warning(self, "Gemini API Initialization Failed", err_msg)

        # Initialize Claude API client
        try:
            # Try to get key directly from environment
            api_key = os.environ.get("CLAUDE_API_KEY") or os.getenv("CLAUDE_API_KEY")

            # Initialize with the key
            self.claude_api = ClaudeAPI(api_key=api_key)
            self.claude_api_initialized = True
            print("Successfully initialized Claude API")
        except Exception as e:
            self.claude_api_initialized = False
            err_msg = f"Failed to initialize Claude API: {str(e)}\n\nCheck your API key in the .env file."
            print(f"ERROR: {err_msg}")
            # Only show warning if Gemini isn't initialized either
            if not self.gemini_api_initialized:
                QMessageBox.warning(self, "Claude API Initialization Failed", err_msg)

        # Initialize Google Vision API client
        try:
            # Try to get credentials path from environment
            credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

            # Initialize with the credentials
            self.vision_api = GoogleVisionAPI(credentials_path=credentials_path)
            self.vision_api_initialized = True
            print("Successfully initialized Google Vision API")
        except Exception as e:
            self.vision_api_initialized = False
            err_msg = f"Failed to initialize Google Vision API: {str(e)}\n\nCheck your credentials."
            print(f"ERROR: {err_msg}")
            QMessageBox.warning(self, "Google Vision API Initialization Failed", err_msg)

        # Set overall API status based on what's available
        self.api_initialized = self.gemini_api_initialized or self.claude_api_initialized or self.vision_api_initialized

        # Initialize media handler
        self.media_handler = MediaHandler()

        # Add reference to pricing data for Vision API
        self.pricing_data = self.project_data.get("pricing_data", {
            "hourly_rate": 75.00,
            "increment": 15
        })

        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create a horizontal splitter for the main components
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel for media and chat
        left_panel = QSplitter(Qt.Orientation.Vertical)
        
        # Media viewer
        self.media_viewer = MediaViewer(self)
        left_panel.addWidget(self.media_viewer)
        
        # Chat widget
        self.chat_widget = ChatWidget(self)
        left_panel.addWidget(self.chat_widget)
        
        # Set left panel sizes
        left_panel.setSizes([500, 300])
        
        # Right panel for estimation details
        self.estimation_widget = EstimationWidget(self)
        
        # Add panels to main splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(self.estimation_widget)
        
        # Set main splitter sizes
        main_splitter.setSizes([700, 500])
        
        # Add main splitter to layout
        main_layout.addWidget(main_splitter)
        
        # Connect signals
        self.chat_widget.message_sent.connect(self.process_message)
        
    def import_media(self, file_path):
        """Import media file into the project"""
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"WARNING: File does not exist: {file_path}")
            return

        # Add file path to project data
        if file_path not in self.project_data["media_files"]:
            self.project_data["media_files"].append(file_path)
            print(f"Added media file to project: {file_path}")

        # Display the media in the media viewer
        self.media_viewer.load_media(file_path)
        
        # If API is initialized, provide a welcome message about the imported media
        if self.api_initialized and file_path:
            media_type = "image" if self.media_handler.is_image_file(file_path) else "video"
            filename = os.path.basename(file_path)
            welcome_msg = f"I've loaded your {media_type} '{filename}'. You can ask me questions about the electrical work shown in it, and I'll help generate an estimate."
            self.chat_widget.add_assistant_message(welcome_msg)
        
    def process_message(self, message):
        """Process a message from the chat widget"""
        # Add user message to project data
        self.project_data["chat_history"].append({"role": "user", "content": message})

        # Check if any API is initialized
        if not self.api_initialized:
            self.chat_widget.add_assistant_message("No API initialized. Please check your API credentials in the .env file.")
            return

        # Show a thinking message with animated dots using chat_widget's animation
        self.chat_widget.add_assistant_message("Thinking...")

        # Get currently loaded media files
        current_media = self.project_data["media_files"]

        # Debug - print project_data media_files
        print(f"Media files in project_data: {current_media}")

        # Use media_viewer.current_media if available
        if hasattr(self, 'media_viewer') and self.media_viewer.current_media:
            if self.media_viewer.current_media not in current_media:
                current_media.append(self.media_viewer.current_media)
                print(f"Added current media from viewer: {self.media_viewer.current_media}")

        # Also check media_list from media_viewer
        if hasattr(self, 'media_viewer') and hasattr(self.media_viewer, 'media_list'):
            for media in self.media_viewer.media_list:
                if media not in current_media and os.path.exists(media):
                    current_media.append(media)
                    print(f"Added media from media_list: {media}")

        # Verify the media files exist
        valid_media = []
        for media_path in current_media:
            if os.path.exists(media_path):
                valid_media.append(media_path)
                print(f"Found valid media: {media_path}")
            else:
                print(f"WARNING: Media file not found: {media_path}")

        # Get images from valid media
        image_paths = [f for f in valid_media if self.media_handler.is_image_file(f)]

        # Print debug information
        print(f"Found {len(image_paths)} valid images for processing:")
        for img in image_paths:
            print(f"  - {img}")

        # Handle case where we have no images
        if not image_paths and "image" in message.lower():
            self.chat_widget.remove_last_message()
            self.chat_widget.add_assistant_message(
                "I don't see any images loaded in this project. Please import an image using the 'Import Media' button first."
            )
            return

        try:
            # Check if there are any video files but no images
            video_paths = [f for f in valid_media if self.media_handler.is_video_file(f)]
            if not image_paths and video_paths and self.api_choice == 2:
                # If using Google Vision API with only videos, show a message
                assistant_message = "Google Vision API can only analyze images, not videos. Please either upload images or switch to Gemini or Claude API for video analysis."
            # Process based on which API we're using
            elif self.api_choice == 0 and self.gemini_api_initialized:
                # Using Gemini API
                assistant_message = self.process_with_gemini_api(image_paths, message)
            elif self.api_choice == 1 and self.claude_api_initialized:
                # Using Claude API
                assistant_message = self.process_with_claude_api(image_paths, message)
            elif self.api_choice == 2 and self.vision_api_initialized:
                # Using Google Vision API
                assistant_message = self.process_with_vision_api(image_paths, message)
            else:
                # Try to use any available API
                if self.gemini_api_initialized:
                    assistant_message = self.process_with_gemini_api(image_paths, message)
                elif self.claude_api_initialized:
                    assistant_message = self.process_with_claude_api(image_paths, message)
                elif self.vision_api_initialized:
                    assistant_message = self.process_with_vision_api(image_paths, message)
                else:
                    # No working API available
                    self.chat_widget.remove_last_message()
                    self.chat_widget.add_assistant_message(
                        "No working API available. Please check your API credentials."
                    )
                    return

            # The thinking animation is now handled by chat_widget
            # So we just need to add the real response with a slight delay
            QTimer.singleShot(300, lambda: self._add_response(assistant_message))

            # Process the response for estimation data
            self.process_for_estimation(message, assistant_message)

        except Exception as e:
            # The thinking animation is now handled by chat_widget

            # Add error message
            error_msg = f"Error processing request: {str(e)}"
            print(f"ERROR: {error_msg}")
            traceback.print_exc()

            # Add error message with visual indication and animation
            QTimer.singleShot(300, lambda: self._add_response(f"❌ {error_msg}"))

    def process_with_gemini_api(self, image_paths, message):
        """Process a message using the Gemini API"""
        # Format chat history for Gemini API
        formatted_history = []
        for msg in self.chat_widget.get_chat_history():
            if msg["role"] != "thinking":  # Skip thinking messages
                formatted_history.append({"role": msg["role"], "content": msg["content"]})

        # Remove the last message (which is the "thinking" message)
        if formatted_history and formatted_history[-1]["content"] == "Thinking...":
            formatted_history.pop()

        # Craft a specialized prompt for electrical estimation
        system_prompt = """
        You are an AI electrical estimator assistant. Your job is to:
        1. Analyze images of electrical systems, panels, rooms, or building plans
        2. Identify the electrical components visible in the images
        3. Provide detailed estimates for materials, labor, and total costs
        4. Answer questions about electrical work in a clear, professional manner

        VERY IMPORTANT FORMATTING INSTRUCTIONS:
        When providing estimates or listing materials, follow these specific formats:

        For tables, use this exact markdown format with these exact column headers:
        | Item | Quantity | Unit | Unit Price |
        |------|----------|------|------------|
        | Receptacle 15A | 10 | ea | $5.50 |
        | EMT Conduit 3/4" | 50 | ft | $2.25 |

        For lists, use this exact format with one item per line:
        - 10 ea Receptacle 15A - $5.50 each
        - 50 ft EMT Conduit 3/4" - $2.25 per foot

        Always include the quantity, unit, description, and price for each item.
        Be consistent in your formatting throughout your response.

        For units, use these standardized abbreviations:
        - ea (each) for individual components
        - ft (feet) for linear measurements
        - sq ft (square feet) for area measurements

        If asked for a cost estimate, ALWAYS include an itemized list of materials and labor.
        Format your response in a way that can be easily parsed by a computer program.
        """

        # Print API call information
        print(f"Sending message to Gemini API with {len(image_paths)} images")

        # Send message to Gemini API
        response = self.gemini_api.get_electrical_estimate(
            image_paths=image_paths,
            prompt=message,
            chat_history=formatted_history[:-1] if formatted_history else []  # Exclude current message
        )

        # Get the assistant's response
        print(f"DEBUG - Gemini API response structure: {response.keys()}")
        
        if "content" in response:
            # Handle different response formats
            content = response["content"]
            print(f"DEBUG - Content type: {type(content)}")
            
            if isinstance(content, list) and len(content) > 0:
                # List format
                if isinstance(content[0], dict) and "text" in content[0]:
                    assistant_message = content[0]["text"]
                else:
                    # Try to extract from content directly
                    assistant_message = str(content[0])
            elif isinstance(content, str):
                # String format
                assistant_message = content
            else:
                # Unknown format - try to convert to string
                assistant_message = str(content)
                
            print("Received response from Gemini API")
        else:
            # Check for other response formats
            if "text" in response:
                assistant_message = response["text"]
                print("Received response from Gemini API (text format)")
            elif "candidates" in response and len(response["candidates"]) > 0:
                candidate = response["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        assistant_message = parts[0]["text"]
                    else:
                        assistant_message = str(parts)
                else:
                    assistant_message = str(candidate)
                print("Received response from Gemini API (candidates format)")
            else:
                assistant_message = "Sorry, I couldn't process your request. Please check the console for errors."
                print(f"Unexpected API response format: {response}")
                if "error" in response:
                    print(f"API error: {response['error']}")

        return assistant_message

    def process_with_claude_api(self, image_paths, message):
        """Process a message using the Claude API"""
        # Format chat history for Claude API
        formatted_history = []
        for msg in self.chat_widget.get_chat_history():
            if msg["role"] != "thinking":  # Skip thinking messages
                formatted_history.append({"role": msg["role"], "content": msg["content"]})

        # Remove the last message (which is the "thinking" message)
        if formatted_history and formatted_history[-1]["content"] == "Thinking...":
            formatted_history.pop()

        # Craft a specialized prompt for electrical estimation
        system_prompt = """
        You are an AI electrical estimator assistant. Your job is to:
        1. Analyze images of electrical systems, panels, rooms, or building plans
        2. Identify the electrical components visible in the images
        3. Provide detailed estimates for materials, labor, and total costs
        4. Answer questions about electrical work in a clear, professional manner

        VERY IMPORTANT FORMATTING INSTRUCTIONS:
        When providing estimates or listing materials, follow these specific formats:

        For tables, use this exact markdown format with these exact column headers:
        | Item | Quantity | Unit | Unit Price |
        |------|----------|------|------------|
        | Receptacle 15A | 10 | ea | $5.50 |
        | EMT Conduit 3/4" | 50 | ft | $2.25 |

        For lists, use this exact format with one item per line:
        - 10 ea Receptacle 15A - $5.50 each
        - 50 ft EMT Conduit 3/4" - $2.25 per foot

        Always include the quantity, unit, description, and price for each item.
        Be consistent in your formatting throughout your response.

        For units, use these standardized abbreviations:
        - ea (each) for individual components
        - ft (feet) for linear measurements
        - sq ft (square feet) for area measurements

        If asked for a cost estimate, ALWAYS include an itemized list of materials and labor.
        Format your response in a way that can be easily parsed by a computer program.
        """

        # Print API call information
        print(f"Sending message to Claude API with {len(image_paths)} images")

        # Send message to Claude API
        response = self.claude_api.get_electrical_estimate(
            image_paths=image_paths,
            prompt=message,
            chat_history=formatted_history[:-1] if formatted_history else []  # Exclude current message
        )

        # Get the assistant's response
        print(f"DEBUG - Claude API response structure: {response.keys()}")
        
        if "content" in response:
            # Handle different response formats
            content = response["content"]
            print(f"DEBUG - Content type: {type(content)}")
            
            if isinstance(content, list) and len(content) > 0:
                # Old API format with list of content items
                if isinstance(content[0], dict) and "text" in content[0]:
                    assistant_message = content[0]["text"]
                else:
                    # Try to extract from content directly
                    assistant_message = str(content[0])
            elif isinstance(content, str):
                # New API format - directly in content as string
                assistant_message = content
            else:
                # Unknown format - try to convert to string
                assistant_message = str(content)
                
            print("Received response from Claude API")
        else:
            # Check for alternative response formats
            if "message" in response and "content" in response["message"]:
                # Another potential format
                assistant_message = response["message"]["content"]
                print("Received response from Claude API (alternative format)")
            else:
                assistant_message = "Sorry, I couldn't process your request. Please check the console for errors."
                print(f"Unexpected API response format: {response}")
                if "error" in response:
                    print(f"API error: {response['error']}")

        return assistant_message

    def process_with_vision_api(self, image_paths, message):
        """Process a message using the Google Vision API"""
        print(f"Processing {len(image_paths)} images with Google Vision API")

        # Check if we have any images to process
        if not image_paths:
            return "I don't see any valid images to analyze. Please import some images first."

        # Results to store electrical components found
        all_components = []
        all_text = []
        electrical_specs = []

        # Process each image with Vision API
        for image_path in image_paths:
            print(f"Analyzing image: {image_path}")
            analysis = self.vision_api.detect_electrical_components(image_path)

            # Extract components found
            components = analysis.get("electrical_components", [])
            specs = analysis.get("electrical_specifications", [])
            text_items = analysis.get("raw_analysis", {}).get("text", [])

            # Add to results
            all_components.extend(components)
            all_text.extend(text_items)
            electrical_specs.extend(specs)

        # Generate a human-readable response
        response_parts = []

        # Initialize component_dict to avoid reference before assignment
        component_dict = {}

        # Add a greeting and summary of analysis
        response_parts.append(f"I've analyzed the image{'s' if len(image_paths) > 1 else ''} using Google Vision API.")

        if all_components:
            response_parts.append("\n### Electrical Components Detected\n")
            # Create a table for components
            response_parts.append("| Item | Quantity | Unit | Unit Price |")
            response_parts.append("|------|----------|------|------------|")

            # Update the components dictionary
            component_dict.clear()
            for comp in all_components:
                comp_type = comp.get("type", "unknown")
                description = comp.get("description", comp_type)
                score = comp.get("confidence", 0.0)

                # Only include high-confidence detections
                if score < 0.6:
                    continue

                # Generate a key for component dict
                key = description.lower()

                # Add or update the component count
                if key in component_dict:
                    component_dict[key]["quantity"] += 1
                else:
                    # Assign a default price based on component type
                    unit_price = 0.0
                    if "panel" in key:
                        unit_price = 150.00
                    elif "breaker" in key:
                        unit_price = 35.00
                    elif "outlet" in key or "receptacle" in key:
                        unit_price = 5.50
                    elif "switch" in key:
                        unit_price = 8.25
                    elif "light" in key or "fixture" in key:
                        unit_price = 45.00
                    elif "conduit" in key:
                        unit_price = 2.25
                    elif "wire" in key or "cable" in key:
                        unit_price = 1.75
                    else:
                        unit_price = 10.00

                    component_dict[key] = {
                        "description": description,
                        "quantity": 1,
                        "unit": "ea",
                        "unit_price": unit_price
                    }

            # Add components to table
            total_estimate = 0.0
            for key, comp in component_dict.items():
                row = f"| {comp['description']} | {comp['quantity']} | {comp['unit']} | ${comp['unit_price']:.2f} |"
                response_parts.append(row)
                total_estimate += comp["quantity"] * comp["unit_price"]

            # Add an estimated labor section based on components
            labor_hours = min(4.0, len(component_dict) * 0.5)  # estimate labor hours
            labor_rate = self.pricing_data.get("hourly_rate", 75.0)
            labor_cost = labor_hours * labor_rate

            response_parts.append("\n### Labor Estimate\n")
            response_parts.append("| Item | Quantity | Unit | Unit Price |")
            response_parts.append("|------|----------|------|------------|")
            response_parts.append(f"| Labor | {labor_hours:.2f} | hour | ${labor_rate:.2f} |")

            # Add total cost
            total_estimate += labor_cost
            response_parts.append(f"\n### Total Estimate: ${total_estimate:.2f}\n")

        else:
            response_parts.append("I couldn't identify any specific electrical components in the image. Please ensure the image clearly shows electrical components.")

        # Add text found in image
        if all_text:
            response_parts.append("\n### Text Found in Images\n")

            # Filter out short or low-confidence text
            text_items = [item["text"] for item in all_text if len(item["text"]) > 1]

            # Limit to top 10 items
            if text_items:
                for i, text in enumerate(text_items[:10]):
                    response_parts.append(f"- \"{text}\"")
            else:
                response_parts.append("No significant text detected in the images.")

        # Add recommendations based on what was found
        response_parts.append("\n### Recommendations\n")
        # Ensure component_dict exists - it should be initialized above but make sure it's not None
        if 'component_dict' not in locals() or component_dict is None:
            component_dict = {}

        if component_dict:
            component_keys = ' '.join(component_dict.keys()).lower()
            if "panel" in component_keys:
                response_parts.append("- Ensure proper grounding for the electrical panel")
                response_parts.append("- Verify all breakers are properly sized for their circuits")
            elif "outlet" in component_keys or "receptacle" in component_keys:
                response_parts.append("- Check GFCI protection requirements for wet locations")
                response_parts.append("- Ensure outlets are properly spaced according to code")
            else:
                response_parts.append("- Consult local electrical codes for specific requirements")
                response_parts.append("- Use appropriate safety equipment during installation")
        else:
            response_parts.append("- Consider providing clearer images of electrical components")
            response_parts.append("- Consult a licensed electrician for a detailed inspection")

        # Add a note about the AI nature of this estimate
        response_parts.append("\n*Note: This is an AI-generated estimate based on computer vision analysis. For a precise quote, consult with a licensed electrician who can inspect the site in person.*")

        # Join all parts into a single message
        return "\n".join(response_parts)
    
    def process_for_estimation(self, user_message, assistant_message):
        """
        Process the assistant's message to extract estimation data
        Uses multiple approaches to identify and extract items
        """
        # Check if the message contains estimation-related keywords
        if any(keyword in user_message.lower() for keyword in ["estimate", "cost", "price", "quote", "material", "bill", "items"]):
            # Split the message into lines
            lines = assistant_message.split('\n')
            extracted_items = []
            
            # Look for tables in the response (usually indicated by | characters)
            table_pattern = r"\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"
            table_matches = re.findall(table_pattern, assistant_message)
            if table_matches:
                # Find column indices for item, quantity, unit, and price
                headers = table_matches[0] if len(table_matches) > 0 else []
                if len(headers) >= 4:
                    item_idx = -1
                    qty_idx = -1
                    unit_idx = -1 
                    price_idx = -1
                    
                    # Try to identify column purposes
                    for i, header in enumerate(headers):
                        header_lower = header.lower()
                        if any(word in header_lower for word in ["item", "description", "component", "material"]):
                            item_idx = i
                        elif any(word in header_lower for word in ["qty", "quantity", "amount", "count"]):
                            qty_idx = i
                        elif any(word in header_lower for word in ["unit", "measure"]):
                            unit_idx = i
                        elif any(word in header_lower for word in ["price", "cost", "rate"]):
                            price_idx = i
                    
                    # If we couldn't identify columns, make a best guess
                    if item_idx == -1:
                        item_idx = 0  # Usually first column is description
                    if qty_idx == -1 and unit_idx == -1:
                        qty_idx = 1  # Usually second column is quantity
                    if unit_idx == -1 and qty_idx != 1:
                        unit_idx = 2  # If quantity isn't second, unit is usually third
                    if price_idx == -1:
                        price_idx = 3  # Price is usually last column
                    
                    # Process table rows (skip header)
                    for row in table_matches[1:]:
                        # Try to extract data
                        if len(row) > max(item_idx, qty_idx, unit_idx, price_idx):
                            try:
                                description = row[item_idx].strip()
                                
                                # Extract quantity
                                qty_text = row[qty_idx].strip() if qty_idx >= 0 else ""
                                qty_match = re.search(r"(\d+\.?\d*)", qty_text)
                                quantity = float(qty_match.group(1)) if qty_match else 1
                                
                                # Extract unit
                                unit = row[unit_idx].strip().lower() if unit_idx >= 0 else "ea"
                                if not unit or unit in ["n/a", "-"]:
                                    unit = "ea"
                                
                                # Extract price
                                price_text = row[price_idx].strip() if price_idx >= 0 else ""
                                price_match = re.search(r"(\d+\.?\d*)", price_text.replace(",", ""))
                                price = float(price_match.group(1)) if price_match else 0
                                
                                if description and price > 0:
                                    extracted_items.append({
                                        "item": description,
                                        "quantity": quantity,
                                        "unit": unit,
                                        "unit_price": price
                                    })
                            except Exception as e:
                                print(f"Error extracting from table row: {e}")
            
            # Process list items and regular lines
            for line in lines:
                line = line.strip()
                
                # Skip header lines and short lines
                if len(line) < 5 or line.startswith('#') or line.startswith('|'):
                    continue
                
                # Skip continuation lines without numbers
                if not any(c.isdigit() for c in line):
                    continue
                
                # Method 1: Find lines with quantity, unit and price using common patterns
                
                # Look for lines with both quantity indicators and price indicators
                quantity_pattern = r"(\d+\.?\d*)\s*(ea|each|ft|feet|foot|m|meter|meters|pcs|pieces|rolls|boxes|inch|in)"
                price_pattern = r"[\$\€\£]\s*(\d+\.?\d*)"
                
                qty_match = re.search(quantity_pattern, line.lower())
                price_match = re.search(price_pattern, line)
                
                if qty_match and price_match:
                    try:
                        quantity = float(qty_match.group(1))
                        unit = qty_match.group(2).lower()
                        unit_price = float(price_match.group(1))
                        
                        # Normalize unit
                        if unit in ["each", "pcs", "pieces"]:
                            unit = "ea"
                        elif unit in ["foot", "feet"]:
                            unit = "ft"
                        elif unit in ["meter", "meters"]:
                            unit = "m"
                        
                        # Extract description - try to find text after the quantity or between quantity and price
                        description_start = line.lower().find(qty_match.group(0)) + len(qty_match.group(0))
                        description_end = line.find("$") if "$" in line else len(line)
                        
                        description = line[description_start:description_end].strip()
                        # Clean up the description (remove dashes, extra spaces, etc.)
                        description = re.sub(r"^\s*[-:\–]\s*", "", description)
                        description = re.sub(r"\s+", " ", description).strip()
                        
                        # If description is empty or just punctuation, use the whole line as context
                        if not description or all(c in ".,:-– " for c in description):
                            description = line.replace(qty_match.group(0), "").replace(price_match.group(0), "")
                            description = re.sub(r"\s+", " ", description).strip()
                        
                        # Skip if we couldn't extract a meaningful description
                        if description and not description.isspace():
                            extracted_items.append({
                                "item": description,
                                "quantity": quantity,
                                "unit": unit,
                                "unit_price": unit_price
                            })
                    except Exception as e:
                        print(f"Error extracting from line: {e}")
                
                # Method 2: Try to extract from bulleted or numbered lists with price at end
                list_pattern = r"^[\*\-\•\d\.]+\s+(.+?)\s*[\:\-]\s*[\$\€\£]\s*(\d+\.?\d*)\s*(ea|each|per\s+\w+)?"
                list_match = re.search(list_pattern, line)
                
                if list_match and not any(item["item"] == list_match.group(1).strip() for item in extracted_items):
                    try:
                        description = list_match.group(1).strip()
                        unit_price = float(list_match.group(2))
                        unit = "ea"  # Default unit
                        quantity = 1  # Default quantity
                        
                        # Try to extract quantity from the description
                        qty_in_desc = re.search(r"(\d+\.?\d*)\s*(ea|each|ft|feet|foot|m|meter|meters)", description.lower())
                        if qty_in_desc:
                            quantity = float(qty_in_desc.group(1))
                            unit = qty_in_desc.group(2).lower()
                            # Remove the quantity part from description
                            description = description.replace(qty_in_desc.group(0), "").strip()
                        
                        # Normalize unit
                        if unit in ["each"]:
                            unit = "ea"
                        elif unit in ["foot", "feet"]:
                            unit = "ft"
                        elif unit in ["meter", "meters"]:
                            unit = "m"
                        
                        # Check if we have a meaningful description 
                        if description and not description.isspace():
                            extracted_items.append({
                                "item": description,
                                "quantity": quantity,
                                "unit": unit,
                                "unit_price": unit_price
                            })
                    except Exception as e:
                        print(f"Error extracting from list item: {e}")
                        
                # Method 3: Look for items with quantity, description and price in format: "Qty x Item - $Price each"
                item_pattern = r"(\d+\.?\d*)\s*[xX]\s*([^-$]+)[\s\-]*[\$\€\£]\s*(\d+\.?\d*)"
                item_match = re.search(item_pattern, line)
                
                if item_match and not any(item["item"] == item_match.group(2).strip() for item in extracted_items):
                    try:
                        quantity = float(item_match.group(1))
                        description = item_match.group(2).strip()
                        unit_price = float(item_match.group(3))
                        
                        # Look for unit in the description
                        unit_match = re.search(r"\b(ea|each|ft|feet|foot|m|meter|meters)\b", description.lower())
                        unit = unit_match.group(1).lower() if unit_match else "ea"
                        
                        # Normalize unit
                        if unit in ["each"]:
                            unit = "ea"
                        elif unit in ["foot", "feet"]:
                            unit = "ft"
                        elif unit in ["meter", "meters"]:
                            unit = "m"
                        
                        extracted_items.append({
                            "item": description,
                            "quantity": quantity,
                            "unit": unit,
                            "unit_price": unit_price
                        })
                    except Exception as e:
                        print(f"Error extracting from formatted item: {e}")
            
            # Add all extracted items to the estimation
            if extracted_items:
                print(f"Extracted {len(extracted_items)} items from Claude's response")
                for item in extracted_items:
                    print(f"Adding item: {item}")
                    self.estimation_widget.add_item_from_ai(item)
            else:
                print("No items extracted from Claude's response")
    
    # Removed animation methods as they're now handled by the chat_widget

    def _add_response(self, message):
        """Add a response from the AI with animation effect"""
        # Add the response message
        self.chat_widget.add_assistant_message(message)
        self.project_data["chat_history"].append({"role": "assistant", "content": message})

    def set_pricing_data(self, pricing_data):
        """Set the pricing data and update related components"""
        self.project_data["pricing_data"] = pricing_data
        self.pricing_data = pricing_data  # Add a direct reference for use in the Vision API
        # Update estimation widget with new pricing data
        self.estimation_widget.update_pricing(pricing_data)

    def toggle_api(self):
        """Cycle through available APIs: Gemini -> Claude -> Vision -> Gemini"""
        # Determine next API to try
        next_api = (self.api_choice + 1) % 3

        # Keep cycling if the next API isn't initialized
        attempts = 0
        while attempts < 3:  # Only try each option once
            if next_api == 0 and self.gemini_api_initialized:
                self.api_choice = 0
                break
            elif next_api == 1 and self.claude_api_initialized:
                self.api_choice = 1
                break
            elif next_api == 2 and self.vision_api_initialized:
                self.api_choice = 2
                break
            else:
                next_api = (next_api + 1) % 3
                attempts += 1

        if attempts >= 3:
            # None of the APIs are available
            QMessageBox.warning(
                self,
                "No APIs Available",
                "No APIs are properly initialized. Please check your API credentials."
            )
            return self.api_choice

        # Update the UI to reflect the current API
        api_names = ["Gemini API", "Claude API", "Google Vision API"]
        api_name = api_names[self.api_choice]
        self.chat_widget.add_assistant_message(f"Switched to {api_name} for image analysis.")
        return self.api_choice

    def get_project_data(self):
        """Get all project data for saving"""
        # Update with latest data from widgets
        self.project_data["estimation_data"] = self.estimation_widget.get_estimation_data()
        self.project_data["chat_history"] = self.chat_widget.get_chat_history()

        return self.project_data