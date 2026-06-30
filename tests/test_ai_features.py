import pytest
import json
from dotenv import load_dotenv

load_dotenv()

from ai.failure_analyzer import analyze_failure
from ai.test_generator import generate_test_cases
from ai.response_validator import validate_response
from ai.data_generator import generate_test_data

@pytest.mark.ai 
class TestAIFeatures:

    def test_failure_analysis(self):
        result = analyze_failure(
            test_name="test_update_booking",
            request_data={"method": "PUT", "url": "/booking/5", "headers": {"Cookie":"token=expired"}},
            response_data={"status_code": 403,"body": "forbidden"},
            error_message="assert 403==200"
        )
        assert result is not None
        print(f"\nAI Analysis\n{result}")

    def test_generate_test_cases(self, booking_schema):
        result = generate_test_cases("/booking", "POST", booking_schema)
        assert result is not None
        assert isinstance(result, list)
        print(f"\nGenerated {len(result)} test cases")

    def test_validate_response(self, booking_api, booking_payload):
        response = booking_api.create_booking(booking_payload)
        assert response.status_code ==200

        result = validate_response(
            request_payload=booking_payload,
            response_body=response.json()["booking"]
        )
        assert result is not None
        print(f"\nAI Validation:{result}")



    def test_validate_response_mismatch(self, booking_payload):
        """AI Should catch when response doesn't match request"""
        """Note: need to handle- RequestBody & ResponseBody can be diff"""
        #fake response  with wrong data
        fake_response = {
            "firstname": "WRONG_NAME",
            "lastname": "WRONG_NAME",
            "totalprice": 9999
        }

        result = validate_response(
            request_payload=booking_payload,
            response_body=fake_response
        )
        assert result is not None
        assert result["valid"] == False
        assert len(result["issues"])>0
        print(f"\nMismatch detected:{result['issues']}")


    def test_ai_generated_cases_execution(self, booking_api, booking_schema):
        """Generate edge cases with AI then Actually run them"""
        cases = generate_test_cases("/booking", "POST", booking_schema)
        assert cases is not None

        for case in cases:
            response = booking_api.create_booking(case["payload"])
            print(f"\n {case['description']}: got {response.status_code}")

