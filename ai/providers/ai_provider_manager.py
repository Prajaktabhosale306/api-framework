import os
import json
from utils.logger import get_logger

logger = get_logger(__name__)

class AIClient:
    """Main AI client - picks the right provider based on .env config
    Change AI Provider in .enve to switch models. no code change needed"""

    def __init__(self) -> None:
        provider_name =os.getenv("AI_PROVIDER", "ollama")
        self.provider = self.load_provider(provider_name)
        logger.info(f"AI_Provider:{provider_name}")

    def load_provider(self, name):
        if name == "ollama":
            from ai.providers.ollama_provider import ollamaProvider
            return ollamaProvider(model=os.getenv("AI_MODEL", "gemma3:4b"))
        elif name == "gemini":
            from ai.providers.gemini_provider import GeminiProvider
            return GeminiProvider(model=os.getenv("AI_MODEL", "Gemini-2.0-flash"))
        elif name == "anthropic":
            from ai.providers.anthropic_provider import AnthropicProvider
            return AnthropicProvider(model=os.getenv("AI_MODEL", "claude-sonnet-4.6"))
        else:
            raise Exception(f"Unknown AI Provider: {name}")
        
    def ask(self, prompt, max_tokens=1024):
        """Send promt to whatever provider is configured"""
        logger.info(f"AI Request: {prompt[:100]}...")
        response =self.provider.ask(prompt, max_tokens)
        if response:
            logger.debug(f"AI Response:{response[:200]}...")
        else:
            logger.error("AI Returned no response")
        return response
    
    def ask_json(self, prompt, max_tokens=1024):
        response = self.ask(prompt, max_tokens)
        if response is None:
            return None 
        response = response.strip()
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"AI response is not valid JSON: {e}")
            logger.debug(f"Raw AI Response:\n{response}")
            return None
