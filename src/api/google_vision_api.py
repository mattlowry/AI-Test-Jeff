"""
Google Cloud Vision API integration module
"""

import os
import io
import base64
from typing import List, Dict, Any, Optional

# Google Cloud Vision client library
try:
    from google.cloud import vision
    VISION_API_AVAILABLE = True
except ImportError:
    VISION_API_AVAILABLE = False
    print("Google Cloud Vision library not installed. Run: pip install google-cloud-vision")


class GoogleVisionAPI:
    """
    Integration with Google Cloud Vision API
    
    This class provides methods for analyzing images using
    Google's Vision API for object detection and image labeling.
    """
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the Google Vision API client
        
        Args:
            credentials_path: Path to the service account credentials JSON file.
                If None, attempts to load from environment variable.
        """
        # Set credentials path
        self.credentials_path = credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not self.credentials_path:
            print("Warning: Google Cloud credentials not found. Vision API will not work.")
            print("Set GOOGLE_APPLICATION_CREDENTIALS environment variable or pass credentials_path.")
        
        # Client will be initialized when needed
        self.client = None
        
    def _get_client(self):
        """
        Get or initialize the Vision client

        Returns:
            The Vision API client
        """
        # Only create client when needed
        if not self.client:
            try:
                if not VISION_API_AVAILABLE:
                    print("Google Cloud Vision API not available. Using placeholder.")
                    self.client = "PLACEHOLDER_CLIENT"
                    return self.client

                if self.credentials_path:
                    # Create client from service account JSON file
                    self.client = vision.ImageAnnotatorClient.from_service_account_json(self.credentials_path)
                    print(f"Created Google Vision client using credentials: {self.credentials_path}")
                else:
                    # Use default credentials (from environment)
                    self.client = vision.ImageAnnotatorClient()
                    print("Created Google Vision client using default credentials")

            except Exception as e:
                print(f"Error initializing Google Vision client: {e}")
                print("Using placeholder implementation instead")
                self.client = "PLACEHOLDER_CLIENT"

        return self.client
        
    def analyze_image(
        self, 
        image_path: str,
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze an image using Google Cloud Vision
        
        Args:
            image_path: Path to the image file to analyze
            features: List of features to analyze (e.g., ['LABEL_DETECTION', 'OBJECT_LOCALIZATION'])
                      If None, uses default features
            
        Returns:
            Dictionary containing analysis results
        """
        # Default features if none provided
        if features is None:
            features = ['LABEL_DETECTION', 'TEXT_DETECTION', 'OBJECT_LOCALIZATION']
            
        # Get client
        client = self._get_client()
        if not client or client == "PLACEHOLDER_CLIENT":
            return {"error": "Google Vision client not initialized", "labels": [], "text": [], "objects": []}
            
        try:
            # Check if we're using the placeholder client
            if client == "PLACEHOLDER_CLIENT":
                print("Using placeholder Google Vision implementation")
                # Return placeholder results
                return {
                    "labels": [
                        {"description": "Electric panel", "score": 0.95},
                        {"description": "Wiring", "score": 0.85},
                        {"description": "Circuit breaker", "score": 0.80},
                    ],
                    "text": [
                        {"text": "120V", "confidence": 0.98},
                        {"text": "MAIN", "confidence": 0.97},
                        {"text": "30A", "confidence": 0.95}
                    ],
                    "objects": [
                        {"name": "Electric panel", "score": 0.92, "coordinates": {"x": 100, "y": 200, "width": 50, "height": 30}},
                        {"name": "Wire", "score": 0.87, "coordinates": {"x": 150, "y": 220, "width": 100, "height": 5}}
                    ]
                }

            # Actual implementation using Vision API
            print(f"Analyzing image using Google Vision API: {image_path}")

            # Read the image file
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            # Build feature requests
            feature_requests = []
            for feature_type in features:
                feature = vision.Feature(type_=getattr(vision.Feature.Type, feature_type))
                feature_requests.append(feature)

            # Send request
            response = client.annotate_image({
                'image': image,
                'features': feature_requests,
            })

            # Process response into a more usable format
            result = {
                "labels": [],
                "text": [],
                "objects": []
            }

            # Extract labels
            if hasattr(response, 'label_annotations'):
                for label in response.label_annotations:
                    result["labels"].append({
                        "description": label.description,
                        "score": label.score
                    })

            # Extract text
            if hasattr(response, 'text_annotations') and response.text_annotations:
                # Skip the first one which is the entire text block
                for text in response.text_annotations[1:]:
                    result["text"].append({
                        "text": text.description,
                        "confidence": text.score if hasattr(text, 'score') else 0.9
                    })

            # Extract objects
            if hasattr(response, 'localized_object_annotations'):
                for obj in response.localized_object_annotations:
                    # Calculate bounding box in pixel coordinates
                    vertices = obj.bounding_poly.normalized_vertices
                    if len(vertices) >= 4:
                        result["objects"].append({
                            "name": obj.name,
                            "score": obj.score,
                            "coordinates": {
                                "x": vertices[0].x,
                                "y": vertices[0].y,
                                "width": vertices[1].x - vertices[0].x,
                                "height": vertices[2].y - vertices[0].y
                            }
                        })

            return result
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {"error": str(e), "labels": [], "text": [], "objects": []}
    
    def analyze_image_base64(
        self, 
        image_base64: str,
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze an image from base64 encoded data
        
        Args:
            image_base64: Base64 encoded image data
            features: List of features to analyze
                      If None, uses default features
            
        Returns:
            Dictionary containing analysis results
        """
        # Default features if none provided
        if features is None:
            features = ['LABEL_DETECTION', 'TEXT_DETECTION', 'OBJECT_LOCALIZATION']
            
        # Get client
        client = self._get_client()
        if not client or client == "PLACEHOLDER_CLIENT":
            return {"error": "Google Vision client not initialized", "labels": [], "text": [], "objects": []}
            
        try:
            # Check if we're using the placeholder client
            if client == "PLACEHOLDER_CLIENT":
                print("Using placeholder Google Vision implementation for base64 image")
                # Return placeholder results
                return {
                    "labels": [
                        {"description": "Electric panel", "score": 0.95},
                        {"description": "Wiring", "score": 0.85},
                        {"description": "Circuit breaker", "score": 0.80},
                    ],
                    "text": [
                        {"text": "120V", "confidence": 0.98},
                        {"text": "MAIN", "confidence": 0.97},
                        {"text": "30A", "confidence": 0.95}
                    ],
                    "objects": [
                        {"name": "Electric panel", "score": 0.92, "coordinates": {"x": 100, "y": 200, "width": 50, "height": 30}},
                        {"name": "Wire", "score": 0.87, "coordinates": {"x": 150, "y": 220, "width": 100, "height": 5}}
                    ]
                }

            # Actual implementation using Vision API
            print("Analyzing base64 image using Google Vision API")

            # Decode the base64 data
            image_content = base64.b64decode(image_base64)

            # Create Vision image object
            image = vision.Image(content=image_content)

            # Build feature requests
            feature_requests = []
            for feature_type in features:
                feature = vision.Feature(type_=getattr(vision.Feature.Type, feature_type))
                feature_requests.append(feature)

            # Send request
            response = client.annotate_image({
                'image': image,
                'features': feature_requests,
            })

            # Process response into a more usable format (same as in analyze_image)
            result = {
                "labels": [],
                "text": [],
                "objects": []
            }

            # Extract labels
            if hasattr(response, 'label_annotations'):
                for label in response.label_annotations:
                    result["labels"].append({
                        "description": label.description,
                        "score": label.score
                    })

            # Extract text
            if hasattr(response, 'text_annotations') and response.text_annotations:
                # Skip the first one which is the entire text block
                for text in response.text_annotations[1:]:
                    result["text"].append({
                        "text": text.description,
                        "confidence": text.score if hasattr(text, 'score') else 0.9
                    })

            # Extract objects
            if hasattr(response, 'localized_object_annotations'):
                for obj in response.localized_object_annotations:
                    # Calculate bounding box in pixel coordinates
                    vertices = obj.bounding_poly.normalized_vertices
                    if len(vertices) >= 4:
                        result["objects"].append({
                            "name": obj.name,
                            "score": obj.score,
                            "coordinates": {
                                "x": vertices[0].x,
                                "y": vertices[0].y,
                                "width": vertices[1].x - vertices[0].x,
                                "height": vertices[2].y - vertices[0].y
                            }
                        })

            return result
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {"error": str(e), "labels": [], "text": [], "objects": []}
    
    def detect_electrical_components(self, image_path: str) -> Dict[str, Any]:
        """
        Detect electrical components in an image
        
        This is a specialized wrapper around analyze_image that focuses on
        identifying electrical components like outlets, switches, panels, etc.
        
        Args:
            image_path: Path to the image file to analyze
            
        Returns:
            Dictionary containing detected electrical components with their details
        """
        # Get the general analysis
        analysis = self.analyze_image(image_path)
        
        # Filter for electrical components
        electrical_components = []
        electrical_keywords = [
            "outlet", "receptacle", "switch", "panel", "breaker", "circuit", 
            "conduit", "wire", "cable", "junction", "box", "light", "fixture",
            "transformer", "meter", "electrical"
        ]
        
        # Process labels to find electrical items
        for label in analysis.get("labels", []):
            description = label.get("description", "").lower()
            if any(keyword in description for keyword in electrical_keywords):
                # For each matching label, try to map it to a specific electrical component
                component_type = "unknown"
                for keyword in electrical_keywords:
                    if keyword in description:
                        component_type = keyword
                        break
                
                electrical_components.append({
                    "type": component_type,
                    "description": label.get("description"),
                    "confidence": label.get("score", 0),
                    "quantity": 1  # Default quantity
                })
                
        # Process objects to get location information
        for obj in analysis.get("objects", []):
            name = obj.get("name", "").lower()
            if any(keyword in name for keyword in electrical_keywords):
                # For each matching object, create a component with location info
                component_type = "unknown"
                for keyword in electrical_keywords:
                    if keyword in name:
                        component_type = keyword
                        break
                        
                electrical_components.append({
                    "type": component_type,
                    "description": obj.get("name"),
                    "confidence": obj.get("score", 0),
                    "quantity": 1,  # Default quantity
                    "location": obj.get("coordinates", {})
                })
                
        # Process text to find electrical specifications
        electrical_specifications = []
        for text_item in analysis.get("text", []):
            text = text_item.get("text", "")
            # Look for common electrical specifications in text
            if any(spec in text for spec in ["V", "A", "W", "Ω", "ohm", "amp", "volt", "watt"]):
                electrical_specifications.append({
                    "text": text,
                    "confidence": text_item.get("confidence", 0)
                })
                
        # Return the structured results
        return {
            "electrical_components": electrical_components,
            "electrical_specifications": electrical_specifications,
            "raw_analysis": analysis
        }