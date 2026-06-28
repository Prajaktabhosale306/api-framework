import pytest
import allure
import json
from ai.failure_analyzer import analyse_failure
from utils.logger import get_logger

logger = get_logger(__name__)

def pytest_runtest_makereport(item, call):
    """Pytest hook - automatically runs after every test"""

    #Only on actual test execution(not setup/teardown)
    if call.when !="call":
        return
    
    #Only on failures
    if call.excinfo is None:
        return
    
    #Get last request/response if stored
    request_data = getattr(item, "_last_request", {})
    response_data = getattr(item, "_last_response", {})

    #Ask AI to analyze the failure
    try:
        logger.info(f"AI Analysing Failure{item.name}")
        analysis = analyse_failure(
            test_name=item.name,
            request_data=request_data,
            response_data=response_data,
            error_message=str(call.excinfo.value)
        )

        if analysis:
            #Attach to allure report
            allure. attach(
                analysis,
                name="AI Failure Analysis",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.info(f"AI analysis \n{analysis}")

    except Exception as e:
        logger.warning(f"AI analysis skipped: {e}")