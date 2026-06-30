import json

import allure
import pytest

from ai.failure_analyzer import analyze_failure
from ai.agent.orchestrator import AgentOrchestrator
from utils.logger import get_logger

logger = get_logger(__name__)
orchestrator = AgentOrchestrator()


def pytest_runtest_makereport(item, call):
    """Pytest hook - automatically runs after every test."""

    # Only on actual test execution (not setup/teardown)
    if call.when != "call":
        return

    # Only on failures
    if call.excinfo is None:
        return

    # Get last request/response if stored
    booking_api = item.funcargs.get("booking_api", None)
    if booking_api:
        request_data = getattr(booking_api, "_last_request_data", {})
        response_data = getattr(booking_api, "_last_response_data", {})
    else:
        request_data={}
        response_data={}
    error_message = str(call.excinfo.value)

    try:
        # Agentic: Try autonomous healing first
        result = orchestrator.handle_failure(
            test_name=item.name,
            request_data=request_data,
            response_data=response_data,
            error_message=error_message,
        )

        if result.get("healed"):
            allure.attach(
                json.dumps(result, indent=2),
                name="AI Agent: Self-Healed",
                attachment_type=allure.attachment_type.JSON,
            )

        else:
            # Fallback: AI failure analysis
            analysis = analyze_failure(
                test_name=item.name,
                request_data=request_data,
                response_data=response_data,
                error_message=error_message,
            )

            if analysis:
                allure.attach(
                    analysis,
                    name="AI Failure Analysis",
                    attachment_type=allure.attachment_type.TEXT,
                )

                allure.attach(
                    json.dumps(result, indent=2),
                    name="AI Agent: Healing Attempted",
                    attachment_type=allure.attachment_type.JSON,
                )

                logger.info(f"AI analysis:\n{analysis}")

    except Exception as e:
        logger.warning(f"AI analysis skipped: {e}")

        # Last fallback: If orchestrator crashes, still try basic analysis
        try:
            analysis = analyze_failure(
                test_name=item.name,
                request_data=request_data,
                response_data=response_data,
                error_message=error_message,
            )

            if analysis:
                allure.attach(
                    analysis,
                    name="AI Failure Analysis",
                    attachment_type=allure.attachment_type.TEXT,
                )

        except Exception:
            pass