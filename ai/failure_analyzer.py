import json
from ai.providers.ai_provider_manager import AIClient

ai=AIClient()

def analyse_failure(test_name, request_data, response_data, error_message):
    """When a test fails, AI explains why"""

    prompt = f"""You are an API Testing expert. A test just failed. Analyse it.
Test Name : {test_name}
Request Sent: 
{json.dumps(request_data, indent=2)}

Response Received:
{json.dumps(response_data, indent=2)}

Error message:{error_message}

Provide short analysis:
1. ROOT CAUSE: (One sentence- what went wrong)
2. CATEGORY: (Bug in API / Test Issue / Auth Problem / Data issue / Server issue)
3. SUGGESTED FIX: (one sentence - what to do next)"""
    return ai.ask(prompt)