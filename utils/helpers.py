#purpose: centralized request body, we have default values added, we can override it while calling
def get_booking_payload(firstname="Prajakta", lastname="Bhosale", totalprice=100, depositpaid=True, checkin="2023-01-01", checkout="2023-01-02", additionalneeds=None):
    return {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": additionalneeds
    }