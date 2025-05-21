#!/usr/bin/env python3
"""
Debug script to check environment variables and API connections
"""

import os
import sys
from dotenv import load_dotenv
import requests

def main():
    """Check environment variables and API connections"""
    print("=== Debugging Environment Variables ===")
    
    # Get the absolute path to the .env file
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    print(f"Looking for .env file at: {dotenv_path}")
    
    # Check if .env file exists
    if os.path.exists(dotenv_path):
        print(f".env file exists at {dotenv_path}")
        
        # Try to load the .env file
        print("Loading .env file...")
        load_dotenv(dotenv_path)
        print("Done loading .env file.")
    else:
        print(f"ERROR: .env file not found at {dotenv_path}")
    
    # Check for environment variables
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if claude_api_key:
        key_fragment = claude_api_key[:10] + "..." + claude_api_key[-4:]
        print(f"CLAUDE_API_KEY: Found (starts with {key_fragment})")
        
        # Try to validate Claude API key with a simple request
        try:
            headers = {
                "x-api-key": claude_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Hello!"}]
            }
            
            print("\nTesting Claude API connection...")
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                print("SUCCESS: Connected to Claude API")
                assistant_response = response.json().get("content", [{"text": ""}])[0]["text"]
                print(f"Claude response: '{assistant_response[:50]}...'")
            else:
                print(f"ERROR: Claude API returned status code {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"ERROR connecting to Claude API: {str(e)}")
    else:
        print("ERROR: CLAUDE_API_KEY not found in environment variables")
    
    # Check Google credentials
    google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_creds:
        print(f"\nGOOGLE_APPLICATION_CREDENTIALS: Found ({google_creds})")
        if os.path.exists(google_creds):
            print(f"Google credentials file exists at {google_creds}")
        else:
            print(f"ERROR: Google credentials file not found at {google_creds}")
    else:
        print("\nGOOGLE_APPLICATION_CREDENTIALS: Not found")
    
    print("\n=== Environment check complete ===")

if __name__ == "__main__":
    main()