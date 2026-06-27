from api.base_client import BaseClient
#purpose: All Booking CRUD operations, test calls these methods, never a raw HTTP
class BookingAPI(BaseClient):
    def create_booking(self, booking_data):
        endpoint = "/booking"
        response = self.post(endpoint, json_data=booking_data)
        return response

    def get_booking(self, booking_id):
        endpoint = f"/booking/{booking_id}"
        response = self.get(endpoint)
        return response

    def update_booking(self, booking_id, booking_data):
        endpoint = f"/booking/{booking_id}"
        response = self.put(endpoint, json_data=booking_data)
        return response

    def delete_booking(self, booking_id, token):
        endpoint = f"/booking/{booking_id}"
        response = self.delete(endpoint, headers={"Cookie": f"token={token}"})
        return response