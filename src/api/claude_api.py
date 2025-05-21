"""
Claude API integration module
"""

import os
import json
import base64
import requests
from typing import List, Dict, Any, Optional


class ClaudeAPI:
    """
    Integration with the Claude API (specifically Claude Sonnet 3.7)
    
    This class provides methods for interacting with the Claude API,
    including sending messages with text and image attachments.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude API client
        
        Args:
            api_key: The Claude API key. If None, attempts to load from environment variable.
        """
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("Claude API key is required. Set it in the environment as CLAUDE_API_KEY or pass it to the constructor.")
            
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-7-sonnet-20250219"  # Claude 3.7 Sonnet model
        
    def send_message(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        image_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to the Claude API
        
        Args:
            messages: List of message objects with 'role' and 'content'
            system_prompt: Optional system prompt to guide Claude's behavior
            max_tokens: Maximum number of tokens in the response
            temperature: Controls randomness (0.0 to 1.0)
            image_paths: Optional list of image file paths to include
            
        Returns:
            The API response as a dictionary
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "anthropic-beta": "messages-2023-12-15"
        }
        
        # Process messages to include any images
        processed_messages = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            # Only user messages can contain images
            if role == "user" and image_paths:
                # Convert content to list format for multiple content parts
                content_parts = []
                
                # Add text content
                if content:
                    content_parts.append({
                        "type": "text",
                        "text": content
                    })
                
                # Add images
                for img_path in image_paths:
                    with open(img_path, "rb") as img_file:
                        img_data = base64.b64encode(img_file.read()).decode("utf-8")
                        
                    # Get media type from file extension
                    file_ext = os.path.splitext(img_path)[1].lower()
                    media_type = "image/jpeg"  # Default
                    
                    if file_ext == ".png":
                        media_type = "image/png"
                    elif file_ext in [".jpg", ".jpeg"]:
                        media_type = "image/jpeg"
                    
                    content_parts.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_data
                        }
                    })
                
                processed_messages.append({
                    "role": role,
                    "content": content_parts
                })
            else:
                # For non-image messages or assistant messages
                processed_messages.append({
                    "role": role,
                    "content": content
                })
        
        # Prepare the request payload
        payload = {
            "model": self.model,
            "messages": processed_messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Add system prompt if provided
        if system_prompt:
            payload["system"] = system_prompt
            
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
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
        
        # Send to Claude API with images
        response = self.send_message(
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for more consistent estimates
            image_paths=image_paths
        )
        
        return response