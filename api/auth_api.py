import os
from .base_client import BaseClient

class AuthAPI(BaseClient):
    def create_token(self, username, password):
        endpoint = "/auth"
        data = {
            "username": os.getenv("API_USERNAME"),
            "password": os.getenv("API_PASSWORD")
        }
        response = self.post(endpoint, json_data=data)
        return response