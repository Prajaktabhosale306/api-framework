import os
import anthropic

class AnthropicProvider:
    """Claude_AI - Paid, Higest quality"""

    def __init__(self, model="claude-sonnet-4.0.6"):
        api_key =os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise Exception("ANTHROPIC_API_KEY not found in .env")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model =model

    def ask(self, prompt, max_token=1024):
        try:
            message =self.client.message.create(
               model = self.model,
               max_token=max_token,
               message=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return None