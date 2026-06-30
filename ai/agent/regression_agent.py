import json

from ai.agent.base_agent import BaseAgent
from ai.agent.tools import analyze_pattern
from ai.providers.ai_provider_manager import AIClient

ai = AIClient()


class RegressionAgent(BaseAgent):
    """Analyze multiple test failures to find common root cause."""

    def __init__(self):
        super().__init__(name="RegressionAgent", max_retries=2)

    def run(self, context):
        """
        context = {
            "failures": [
                {
                    "test_name": str,
                    "error": str,
                    "request": dict,
                    "response": dict
                }
            ]
        }
        """

        failures = context.get("failures", [])

        self.logger.info(f"Analyzing {len(failures)} failures for patterns...")

        if len(failures) < 2:
            return {
                "pattern_found": False,
                "reason": "Need 2+ failures to find patterns",
            }

        observation = self.observe(context)
        analysis = self.think(observation)

        return {
            "pattern_found": True,
            "analysis": analysis,
            "failure_count": len(failures),
            **self.get_report(),
        }

    def think(self, observation):
        """Find patterns across failures."""

        failures = observation.get("failures", [])

        prompt = f"""
        You are a regression analysis agent. Multiple tests failed together.
        Find the common root cause.

        Failures:
        {json.dumps(failures, indent=2)}

        Analyze:
        1. Are they hitting the same endpoint?
        2. Same error type?
        3. Same auth issue?
        4. Server-side problem?

        Return JSON:
        {{
            "root_cause": "One sentence",
            "category": "auth|server|data|endpoint|network",
            "affected_endpoints": ["..."],
            "is_environment_issue": true,
            "fix_suggestion": "One sentence"
        }}
        """

        result = ai.ask_json(prompt)

        self.memory.add_attempt(
            "pattern_analysis",
            result,
            result is not None,
        )

        return result

    def act(self, action, context):
        pass