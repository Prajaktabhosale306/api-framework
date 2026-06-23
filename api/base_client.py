import requests
import json

class BaseClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
        return response

    def post(self, endpoint, data=None, json_data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        return response

    def put(self, endpoint, data=None, json_data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        return response

    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=headers, timeout=self.timeout)
        return response