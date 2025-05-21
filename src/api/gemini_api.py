"""
Gemini API integration module
"""

import os
import json
import base64
import requests
from typing import List, Dict, Any, Optional


class GeminiAPI:
    """
    Integration with the Gemini API (specifically Gemini 2.5 Pro Preview)
    
    This class provides methods for interacting with the Gemini API,
    including sending messages with text and image attachments.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini API client
        
        Args:
            api_key: The Gemini API key. If None, attempts to load from environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set it in the environment as GEMINI_API_KEY or pass it to the constructor.")
            
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro-latest:generateContent"
        self.model = "gemini-2.5-pro-latest"
        
    def send_message(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        image_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to the Gemini API
        
        Args:
            messages: List of message objects with 'role' and 'content'
            system_prompt: Optional system prompt to guide Gemini's behavior
            max_tokens: Maximum number of tokens in the response
            temperature: Controls randomness (0.0 to 1.0)
            image_paths: Optional list of image file paths to include
            
        Returns:
            The API response as a dictionary
        """
        # Build the API URL with key
        url_with_key = f"{self.api_url}?key={self.api_key}"

        # Format messages for Gemini API
        parts = []

        # Add system prompt as the first part if provided
        if system_prompt:
            parts.append({"text": f"System instructions: {system_prompt}\n\n"})

        # Add chat history if available
        if messages:
            history_text = ""
            for msg in messages[:-1]:  # Exclude the current message which will be processed separately
                role_prefix = "User: " if msg["role"] == "user" else "Assistant: "
                history_text += f"{role_prefix}{msg['content']}\n\n"

            if history_text:
                parts.append({"text": f"Previous conversation:\n{history_text}"})

        # Add the current prompt
        if messages:
            current_msg = messages[-1]
            current_prompt = current_msg["content"]
            parts.append({"text": f"User: {current_prompt}\n\nPlease provide a detailed analysis and cost estimate."})

        # Add images
        if image_paths:
            for img_path in image_paths:
                try:
                    with open(img_path, "rb") as img_file:
                        img_data = base64.b64encode(img_file.read()).decode("utf-8")

                    # Get media type from file extension
                    file_ext = os.path.splitext(img_path)[1].lower()
                    media_type = "image/jpeg"  # Default

                    if file_ext == ".png":
                        media_type = "image/png"
                    elif file_ext in [".jpg", ".jpeg"]:
                        media_type = "image/jpeg"

                    # Add image to parts
                    parts.append({
                        "inline_data": {
                            "mime_type": media_type,
                            "data": img_data
                        }
                    })
                except Exception as e:
                    print(f"Error processing image {img_path}: {e}")

        # Prepare the request payload
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 64
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
            
        try:
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(url_with_key, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Format the response to match Claude API format for compatibility
            gemini_response = response.json()

            # Extract the generated text from Gemini's response format
            if "candidates" in gemini_response and len(gemini_response["candidates"]) > 0:
                candidate = gemini_response["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    text_parts = [part.get("text", "") for part in candidate["content"]["parts"] if "text" in part]
                    text_response = "".join(text_parts)

                    # Convert to Claude-like format for compatibility
                    return {
                        "content": [{"text": text_response}],
                        "model": self.model,
                        "role": "assistant",
                        "original_response": gemini_response  # Keep original for debugging
                    }
            elif "candidates" in gemini_response and len(gemini_response["candidates"]) > 0:
                # Alternative format
                candidate = gemini_response["candidates"][0]
                if "content" in candidate:
                    content = candidate["content"]
                    if isinstance(content, str):
                        # If content is directly a string
                        return {
                            "content": [{"text": content}],
                            "model": self.model,
                            "role": "assistant",
                            "original_response": gemini_response
                        }
                    elif isinstance(content, dict) and "text" in content:
                        # If content has a text field
                        return {
                            "content": [{"text": content["text"]}],
                            "model": self.model,
                            "role": "assistant",
                            "original_response": gemini_response
                        }

            # Print the response for debugging
            print(f"DEBUG - Gemini API response format: {json.dumps(gemini_response, indent=2)}")

            # If we can't extract properly, return a formatted error message
            error_msg = "Could not extract response from Gemini API. Check the console for the raw response."
            return {
                "content": [{"text": error_msg}],
                "model": self.model,
                "role": "assistant",
                "original_response": gemini_response
            }
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            if hasattr(e, "response") and e.response:
                print(f"Response: {e.response.text}")
            return {"error": str(e)}
    
    def get_electrical_estimate(
        self,
        image_paths: List[str],
        prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Get an electrical estimate based on images and prompts
        
        Args:
            image_paths: List of paths to images showing electrical work
            prompt: Description of what needs to be estimated
            chat_history: Optional chat history for context
            
        Returns:
            The estimation response
        """
        # Craft a specialized system prompt for electrical estimation
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
        
        messages = []
        
        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history)
        
        # Add the current prompt
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        # Send to Gemini API with images
        response = self.send_message(
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for more consistent estimates
            image_paths=image_paths
        )
        
        return response