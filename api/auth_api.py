import os
from .base_client import BaseClient

class AuthAPI(BaseClient):

    def __init__(self, base_url, username, password):
        super().__init__(base_url)
        self.username = username
        self.password = password

    def create_token(self):
        endpoint = "/auth"

        data = {
            "username": self.username,
            "password": self.password
        }

        response = self.post(endpoint, json_data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to create token: {response.status_code} - {response.text}")    
        return response

        
    
