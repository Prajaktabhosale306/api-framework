import requests
import os
class ollamaProvider:
    """runs AI locally on your laptop - completly free"""
    def __init__(self, model=os.getenv("AI_MODEL")):
        self.model =model
        self.base_url ="https://localhost:11434"

    def ask(self, prompt, max_tokens=1024):
        respose = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        if respose.status_code ==200:
            return respose.json()["respose"]
        return None
    

#How to install ollamma
# install: brew install ollamam(mac)
# Download model: ollama pull llamma3
# runs on localhost:11434
##