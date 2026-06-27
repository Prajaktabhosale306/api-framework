import json
from ai.providers.ai_provider_manager import AIClient

ai=AIClient()


def validate_response(request_payload, response_body):
    """AI checks if response makes logical sense"""
    prompt = f"""Check if this API Response is logically correct:
    Request Sent: {json.dumps(request_payload)}
    Response Recieved: {json.dumps(response_body)}
    
    Check:
    1. Does response data match what was sent?
    2. Any logical inconsistancies?
    3. Any data corruption?

    Return JSON: {{""valid: true, "issues": []}} or {{""valid: false, "issues": []}} 
    """
    return ai.ask_json(prompt)