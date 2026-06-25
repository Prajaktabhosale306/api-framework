import os
from .base_client import BaseClient

class AuthAPI(BaseClient):
    def create_token(self):
        endpoint = "/auth"
        data = {
            "username": os.getenv("API_USERNAME"),
            "password": os.getenv("API_PASSWORD")
        }
        response = self.post(endpoint, json_data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to create token: {response.status_code} - {response.text}")
        return response
