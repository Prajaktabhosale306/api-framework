import requests
import os
class ollamaProvider:
    """runs AI locally on your laptop - completly free"""
    def __init__(self, model=os.getenv("AI_MODEL")):
        self.model =model
        self.base_url ="http://localhost:11434"

    def ask(self, prompt, max_tokens=1024):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code ==200:
            return response.json()["response"]
        if response.status_code != 200:
            raise Exception(f"Ollama returned {response.status_code}: {response.text}")
    

#How to install ollamma
# install: brew install ollamam(mac)
# Download model: ollama pull llamma3
# runs on localhost:11434
##