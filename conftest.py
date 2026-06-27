import pytest
import json
import os
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI
from utils.helpers import get_booking_payload
from dotenv import load_dotenv


load_dotenv()
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests against (qa, stage, prod)")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    config_file = f"config/{env}.json"
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    with open(config_file) as f:
        return json.load(f)
    
@pytest.fixture
def create_and_delete_booking(booking_api, auth_token):
     #Create a booking
    payload = get_booking_payload()
    response = booking_api.create_booking(payload)
    assert response.status_code == 200
    booking_id = response.json().get("bookingid")
    
    yield booking_id  # Provide the booking ID to the test

    # Cleanup: Delete the booking after the test#
    delete_response = booking_api.delete_booking(booking_id, auth_token)
    assert delete_response.status_code == 201  # Assuming 201 is the expected status code for successful deletion

@pytest.fixture
def create_booking(booking_api, auth_token):
    created_bookingIds = []  # List to store created booking IDs

    def _create_booking(payload=None):
        if payload is None:
            payload = get_booking_payload()
        response = booking_api.create_booking(payload)
        assert response.status_code == 200
        booking_id = response.json().get("bookingid")
        created_bookingIds.append(booking_id)  # Store the created booking ID
        return response
    
    yield _create_booking  # Provide the inner function to the test

    # Cleanup: Delete all created bookings after the test
    for booking_id in created_bookingIds:
        delete_response = booking_api.delete_booking(booking_id, auth_token)
        assert delete_response.status_code == 201  # Assuming 201 is the expected status code for successful deletion
        
                               
@pytest.fixture(scope="session")
def auth_token(config):
    auth_api = AuthAPI(config["baseUrl"])
    return auth_api.create_token()

@pytest.fixture(scope="session")
def booking_api(config):
    return BookingAPI(config["baseUrl"])

@pytest.fixture
def booking_payload():
    return get_booking_payload()  # Assuming get_booking_payload is imported from utils/helpers.py 

@pytest.fixture
def booking_schema():
    with open("testdata/schemas/booking_schema.json") as file:
        return json.load(file)