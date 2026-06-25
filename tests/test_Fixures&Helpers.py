import pytest
from utils.helpers import get_booking_payload
from utils.schema_validator import validate_json_schema
import allure

@allure.epic("Booking API Tests")
@allure.feature("Booking Management")
@allure.story("create bookings")
class TestFixturesAndHelpers:
    #Use Fixture - default payload, no customization
    def test_createbooking(self, booking_api, booking_payload, auth_token):
        with allure.step("Send request to create a booking"):
            response = booking_api.create_booking(booking_payload)
        with allure.step("Validate response status code and content"):
            assert response.status_code == 200
            assert response.json()["booking"]["firstname"] == booking_payload["firstname"]
            assert response.json()["booking"]["lastname"] == booking_payload["lastname"]
            assert response.json()["booking"]["totalprice"] == booking_payload["totalprice"]
            assert response.json()["booking"]["depositpaid"] == booking_payload["depositpaid"]
            assert response.json()["booking"]["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"]
            assert response.json()["booking"]["bookingdates"]["checkout"] == booking_payload["bookingdates"]["checkout"]
        

    def test_createbooking_with_zero_price(self, booking_api):
        payload = get_booking_payload(totalprice=0)
        response = booking_api.create_booking(payload)
        with allure.step("Validate response status code and content"):
            assert response.status_code == 200
            assert response.json()["booking"]["totalprice"] == 0

    def test_createbooking_with_special_chars (self, booking_api):
        payload = get_booking_payload(firstname="!@#$%^&*()")
        response = booking_api.create_booking(payload)
        with allure.step("Validate response status code and content"):
            assert response.status_code == 200
            assert response.json()["booking"]["firstname"] == "!@#$%^&*()"

    def test_createbooking_empty_names(self, booking_api):
        payload = get_booking_payload(firstname="", lastname="")
        response = booking_api.create_booking(payload)
        with allure.step("Validate response status code and content"):
            assert response.status_code == 200
            assert response.json()["booking"]["firstname"] == ""
            assert response.json()["booking"]["lastname"] == ""

    def test_create_andcleanup(self, create_booking):
        response = create_booking(get_booking_payload(firstname="Test"))
        # Verify that the booking was created
        with allure.step("Validate response status code and content"):
            assert response.status_code == 200
            assert response.json()["booking"]["firstname"] == "Test"
        #Auto-delete will be handled by the fixture after the test completes