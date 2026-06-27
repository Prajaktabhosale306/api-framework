import json
from ai.providers.ai_provider_manager import AIClient

ai=AIClient()

def generate_test_data(count=5):
    """Create test data"""

    prompt = """AI creates realistic data for any api"""

    prompt = f"""Generete {count} realistic test payloads.
    Context: {description}
    Schema to follow:
    {json.dumps(schema, intent=2)}
    Return as JSON array {count} object matching the schema above"""
    return ai.ask_json(prompt)