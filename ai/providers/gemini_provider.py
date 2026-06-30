import os
from google import genai
from utils.logger import get_logger

logger = get_logger(__name__)


class GeminiProvider:
    """Google Gemini Provider"""

    def __init__(self, model="gemini-2.5-flash"):
        import google.genai as genai
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def ask(self, prompt, max_tokens=1024):
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            return response.text
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                logger.warning("Gemini quota exceeded. Skipping AI healing.")
                return None
            logger.exception("Gemini request failed")
            return None