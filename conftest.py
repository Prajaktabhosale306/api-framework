import pytest
import json
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI

@pytest.fixture(scope="session")
def config():
    with open("config/config.json") as config_file:
        config_data = json.load(config_file)
    return config_data

@pytest.fixture(scope="session")
def auth_api(config):
    return AuthAPI(config["baseUrl"])

@pytest.fixture(scope="session")
def auth_token(auth_api, config):
    username = config.get("username", "admin")
    password = config.get("password", "password123")
    response = auth_api.create_token(username, password)
    assert response.status_code == 200
    return response.json().get("token")

@pytest.fixture(scope="session")
def booking_api(config):
    return BookingAPI(config["baseUrl"])