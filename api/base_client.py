import requests
import json
from utils.logger import get_logger
from utils.allure_helper import attach_request, attach_response
logger = get_logger(__name__)
class BaseClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET Request URL: {url}, Params: {params}, Headers: {headers}")
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        #attach to allure report
        attach_request("GET", url, headers, params)
        attach_response(response)
        self._log_response(response)
        return response

    def post(self, endpoint, data=None, json_data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST Request URL: {url}, Data: {data}, JSON Data: {json_data}, Headers: {headers}")
        response = self.session.post(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        
        #attach to allure report
        attach_request("POST", url, headers, json_data)
        attach_response(response)

        self._log_response(response)
        return response

    def put(self, endpoint, data=None, json_data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT Request URL: {url}, Data: {data}, JSON Data: {json_data}, Headers: {headers}")
        response = self.session.put(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        #attach to allure report
        attach_request("PUT", url, headers, json_data)
        attach_response(response)
        self._log_response(response)
        return response

    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE Request URL: {url}, Headers: {headers}")
        response = self.session.delete(url, headers=headers, timeout=self.timeout)
        #attach to allure report
        attach_request("DELETE", url, headers)
        attach_response(response)
        self._log_response(response)
        return response

    def _log_response(self, response):
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
