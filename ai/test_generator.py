import json
from ai.providers.ai_provider_manager import AIClient

ai=AIClient()

def generate_test_cases(endpoint, method, schema):
    """AI generated edge cases test payloads"""

    prompt = f"""Generate 5 edge case test payloads for:
    Endpoint: {method} {endpoint}
    Schema: {json.dumps(schema, intent=2)}
    
    Include: boundry values, missing fields, wrong types, special characters.
    Return as JSON array: [{{"payload:{{}}, "expected_status:": 400, "description": "..."}}]"""

    return ai.ask_json(prompt)