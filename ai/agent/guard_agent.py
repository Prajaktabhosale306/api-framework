import json
import time

from ai.agent.base_agent import BaseAgent
from ai.agent.tools import retry_request
from ai.providers.ai_provider_manager import AIClient

ai = AIClient()


class GuardAgent(BaseAgent):
    """Monitor API health, response time, and detect degradation."""

    def __init__(self):
        super().__init__(name="GuardAgent", max_retries=5)
        self.metrics = []

    def run(self, context):
        """
        context = {
            "base_url": str,
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/booking"
                }
            ],
            "threshold_ms": int
        }
        """
        self.logger.info("Starting health check...")

        threshold = context.get("threshold_ms", 2000)
        issues = []

        for endpoint in context.get("endpoints", []):
            observation = self._check_endpoint(
                endpoint,
                context["base_url"]
            )

            self.metrics.append(observation)

            if observation["response_time_ms"] > threshold:
                issues.append(
                    {
                        "type": "slow_response",
                        "endpoint": endpoint["path"],
                        "response_time_ms": observation["response_time_ms"],
                        "threshold_ms": threshold,
                    }
                )

            if observation["status_code"] >= 500:
                issues.append(
                    {
                        "type": "server_error",
                        "endpoint": endpoint["path"],
                        "status_code": observation["status_code"],
                    }
                )

        analysis = self.think(
            {
                "metrics": self.metrics,
                "issues": issues,
            }
        )

        return {
            "healthy": len(issues) == 0,
            "metrics": self.metrics,
            "issues": issues,
            "analysis": analysis,
            **self.get_report(),
        }

    def _check_endpoint(self, endpoint, base_url):
        """Measure response time and status."""

        url = f"{base_url}{endpoint['path']}"
        method = endpoint.get("method", "GET")

        start = time.time()

        result = retry_request(
            method=method,
            url=url,
            payload=None,
            headers={},
        )

        elapsed = int((time.time() - start) * 1000)

        self.memory.add_attempt(
            f"{method} {endpoint['path']}",
            {
                "status": result.get("status_code"),
                "time_ms": elapsed,
            },
            result.get("status_code", 0) < 400,
        )

        return {
            "endpoint": endpoint["path"],
            "method": method,
            "status_code": result.get("status_code", 0),
            "response_time_ms": elapsed,
        }

    def think(self, observation):
        """Analyze metrics for patterns."""

        if not observation["issues"]:
            return {
                "status": "healthy",
                "summary": "All endpoints responding normally.",
            }

        prompt = f"""
You are an API health monitoring agent.

Metrics:
{json.dumps(observation['metrics'], indent=2)}

Issues Found:
{json.dumps(observation['issues'], indent=2)}

Return JSON in this format:

{{
    "status": "healthy" | "degraded" | "critical",
    "summary": "...",
    "recommendation": "..."
}}
"""

        result = ai.ask_json(prompt)

        return result or {
            "status": "unknown",
            "summary": "Could not analyze.",
        }

    def act(self, action, context):
        """No actions implemented for GuardAgent yet."""
        pass