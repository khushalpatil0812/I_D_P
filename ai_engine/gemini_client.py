import google.generativeai as genai
from flask import current_app

class GeminiClient:
    def __init__(self):
        self.model = None
    
    def initialize(self, api_key):
        """Initialize the Gemini API client"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            return True
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            return False
    
    def generate_content(self, prompt):
        """Generate content using Gemini API"""
        try:
            if not self.model:
                api_key = current_app.config.get('GEMINI_API_KEY')
                if not self.initialize(api_key):
                    return None
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

gemini_client = GeminiClient()
