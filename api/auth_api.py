from .base_client import BaseClient

class AuthAPI(BaseClient):
    def create_token(self, username, password):
        endpoint = "/auth"
        data = {
            "username": username,
            "password": password
        }
        response = self.post(endpoint, json_data=data)
        return response