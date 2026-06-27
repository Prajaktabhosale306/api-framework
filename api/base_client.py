from time import time
import requests
import json
from utils.logger import get_logger
from utils.allure_helper import attach_request, attach_response
logger = get_logger(__name__)
class BaseClient:
    #Purpose: Single place for all HTTP Logic
    #Its a DRY (Don't repeat Yourself) Principle applied to HTTP. Instead of writing requests.get() in every test, I centralize it. All API classes inherit from baseclient- they got logging, allure attachements & retry logic for free
    def __init__(self, base_url, timeout=10, retries=3, delay=2):
        self.base_url = base_url # store base URL for all requests
        self.timeout = timeout #Max wait time for response, prevents tests hanging forever if API is down
        self.session = requests.Session() # reuse TCP Connection across calls, faster than creating new connection for each request- so insted of n nuber of TCP handshake it will use only 1
        self._retry_count = retries #number of time we can rerequesting
        self.delay = delay #wait between retry, don't flood the server with immidiate retries

    def get(self, endpoint, params=None, headers=None): 
        url = f"{self.base_url}{endpoint}" # Build full URL
        logger.info(f"GET Request URL: {url}, Params: {params}, Headers: {headers}") # log what we're doing
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout) #make a call
        
        attach_request("GET", url, headers, params)  #attach to allure report
        attach_response(response) # attach response to allure 
        self._log_response(response) #log + Body
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

    #Underscore _ = Private method, only use internaly
    def _log_response(self, response):
        logger.info(f"Response Status Code: {response.status_code}") #For Status: Always visble- to understand pass or Fail
        logger.debug(f"Response Body: {response.text[:500]}")  #Only in log file - some response error are too big so limit 500 chars

    #Private method
    def _request(self, method, endpoint, payload=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        for attempt in range(1, self._retry_count + 1):
            response = self.session.request(method, url, json=payload, headers=headers)
            if response.status_code < 500:
                break
            logger.warning(f"Attempt {attempt} failed with status code {response.status_code}. Retrying in {self.delay} seconds...")
            time.sleep(self.delay)
        return response