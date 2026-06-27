import os #for accessing environment variables
from .base_client import BaseClient 
#Centralized Authorization (Based on Single Responsibity principle, Should not be part of booking api) 
class AuthAPI(BaseClient): # Baseclient inherits self.post

    def create_token(self):
        endpoint = "/auth"
        #read from environment
        data = {
            "username": os.getenv("API_USERNAME"),
            "password": os.getenv("API_PASSWORD")
        }

        response = self.post(endpoint, json_data=data) #calls Base_client post - getting logging/allure
        if response.status_code != 200:
            raise Exception(f"Failed to create token: {response.status_code} - {response.text}")    #Exception instead of failure
        return response.json()["token"] #return just token string not complete response

        
    
