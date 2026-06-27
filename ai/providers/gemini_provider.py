import os
import google.generativeai as genai

class GeminiProvider:
    """Google Free AI API - (60 calls per minute free)"""

    def __init__(self, model="gemini-2.0-flash"):
        api_key =os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in .env")
        genai.configure(api_key=api_key)
        self.model =genai.GenerativeModel(model)

    def ask(self, prompt, max_token=1024):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return None
    
##
# 1. Goto https://aistudio.google.com/apikey
# 2. Sign in with google account
# 3. click "Create API Key"
# Copy key -> Add it to .env/ Github secret#
