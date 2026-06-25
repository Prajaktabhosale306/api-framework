import pytest
import allure
@allure.epic("Booking API Tests")
@allure.feature("Booking Management")
class TestBooking:
    booking_id = None  # Class variable to store the booking ID across tests

    @allure.story("Create Booking")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_booking(self, booking_api):
        # Example test case for creating a booking
        booking_data = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-10"
            },
            "additionalneeds": "Breakfast"
        }
        response = booking_api.create_booking(booking_data)
        assert response.status_code == 200
        print(response.json())
        assert response.json()["bookingid"] is not None
        TestBooking.booking_id = response.json()["bookingid"]

    @allure.story("Get Booking")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_booking(self, booking_api):
        # Example test case for retrieving a booking
        response = booking_api.get_booking(TestBooking.booking_id)
        assert response.status_code == 200
        assert response.json()["firstname"] == "John"


    @allure.story("Delete Booking")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_booking(self, booking_api, auth_token):
        # Example test case for deleting a booking
        
        response = booking_api.delete_booking(TestBooking.booking_id, auth_token)
        assert response.status_code == 201  # Assuming 201 is the expected status code for successful deletion