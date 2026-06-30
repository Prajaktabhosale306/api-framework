import json
from ai.agent.healing_agent import HealingAgent
from ai.agent.guard_agent import GuardAgent
from ai.agent.regression_agent import RegressionAgent
from ai.providers.ai_provider_manager import AIClient
from utils.logger import get_logger

logger = get_logger(__name__)
ai= AIClient()

class AgentOrchestrator:
    """
    Routes failures to right agent.
    Single failure -> Healing agent
    Mutiple failures -> RegressionAgent first then HealingAgent
    on demand GuardAgent
    """

    def __init__(self):
        self.result =[]

    def handle_failure(self, test_name, request_data, response_data, error_message):
        """Called by the pytest plugin when a test fails."""
        agent = HealingAgent()
        result = agent.run(
            {
                "test_name": test_name,
                "request":request_data,
                "response": response_data,
                "error": error_message
            }
        )
        self.result.append(result)
        return result
    
    def handle_multiple_failures(self, failures):
        """Called when multiple test fails - find common root cause first."""
        regression = RegressionAgent()
        pattern = regression.run({"failures":failures})

        if pattern.get("analysis", {}).get("is_environment_issue"):
            logger.info("Environment issue detected - skipping individual healing")
            return pattern
        
        #Try Healing each individually
        healed = []
        for failure in failures:
            result = self.handle_failure(
                failure["test_name"],
                failure["request"],
                failure["response"],
                failure["error"]
            )
            healed.append(result)

        return{
            "pattern": pattern,
            "individual_results": healed,
            "headed_count": sum(1 for r in healed if r.get(healed))
        }
    
    def explore(self, endpoint, method, base_url, schema, auth_token=None):
        """Run the test generator agent to discover edge cases."""

    def health_check(self, base_url, endpoints, threshold_ms=2000):
        """Run the guard agent to check API health"""
        agent = GuardAgent()
        return agent.run({
            "base_url": base_url,
            "endpoints": endpoints,
            "threshold_ms": threshold_ms
        })
    

