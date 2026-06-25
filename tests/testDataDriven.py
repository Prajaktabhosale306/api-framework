import pytest
import json

def load_test_data():
    with open("testdata/bookings.json") as file:
        return json.load(file)
    
class TestDataDriven:
    @pytest.mark.parametrize("data", load_test_data())
    def test_create_booking(self, booking_api, data):
        response = booking_api.create_booking(data)
        assert response.status_code == 200
        booking = response.json().get("booking")
        assert booking is not None, response.text
        assert booking["firstname"] == data["firstname"]
        assert booking["lastname"] == data["lastname"]
        assert booking["totalprice"] == data["totalprice"]
        assert booking["depositpaid"] == data["depositpaid"]
        assert booking["bookingdates"]["checkin"] == data["bookingdates"]["checkin"]
        assert booking["bookingdates"]["checkout"] == data["bookingdates"]["checkout"]