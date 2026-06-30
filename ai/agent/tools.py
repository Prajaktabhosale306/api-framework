import json
import requests

from ai.providers.ai_provider_manager import AIClient
from utils.logger import get_logger

logger = get_logger(__name__)
ai = AIClient()


def suggest_fix(request_data, response_data, error_message):
    """Ask AI to suggest a fixed request."""

    prompt = f"""
    You are an API Testing expert. A test failed.

    Request:
    {json.dumps(request_data, indent=2)}

    Response:
    {json.dumps(response_data, indent=2)}

    Error:
    {error_message}

    Suggest a FIXED version of the request that would make it pass.

    Return JSON only:
    {{
        "fixed_payload": {{}},
        "fixed_headers": {{}},
        "reasoning": "..."
    }}
    """

    return ai.ask_json(prompt)


def retry_request(method, url, payload, headers):
    """Retry an API call with modified parameters."""

    try:
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            headers=headers,
            timeout=10,
        )

        return {
            "status_code": response.status_code,
            "body": response.text[:500],
        }

    except Exception as e:
        logger.error(f"Retry failed: {e}")

        return {
            "status_code": 0,
            "error": str(e),
        }


def classify_failure(error_message, status_code):
    """Classify what type of failure this is."""

    if status_code == 401 or status_code == 403:
        return "auth_issue"
    elif status_code == 400:
        return "bad_request"
    elif status_code >= 500:
        return "server_error"
    elif "timeout" in error_message.lower():
        return "timeout"
    elif "assert" in error_message.lower():
        return "assertion_failure"

    return "unknown"


def analyze_pattern(failures):
    """Find patterns across multiple failures."""

    prompt = f"""
    Analyze these test failures and find the common root cause.

    Failures:
    {json.dumps(failures, indent=2)}

    Return JSON:
    {{
        "root_cause": "...",
        "category": "...",
        "affected_area": "...",
        "fix_suggestion": "..."
    }}
    """

    return ai.ask_json(prompt)