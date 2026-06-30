import pytest
import allure

@allure.epic("Agentic AI")
@allure.feature("Self-Healing")
class TestAgentDemo:

    def test_healing_agent_trigger(self, booking_api):
        """Intentionally send bad payload - agent should try to heal"""
        bad_payload = {
            "firstname": "",
            "lastname": "",
            "totalprice":-100,
            "depositpaid":"not_boolean",
            "bookingdates":{
                "checkin":"invalid-date",
                "checkout":"invalid-date"
            }
        }
        response = booking_api.create_booking(bad_payload)
        #This assertion will FAIL -> triggers  the agent
        assert response.status_code == 400, f"Expected 400 but got got {response.status_code}"