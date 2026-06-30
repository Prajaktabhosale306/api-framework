import json

from ai.agent.base_agent import BaseAgent
from ai.agent.tools import classify_failure, retry_request, suggest_fix
from ai.providers.ai_provider_manager import AIClient


ai = AIClient()


class HealingAgent(BaseAgent):
    """Autonomously fixes and retries failing tests."""

    def __init__(self):
        super().__init__(name="HealingAgent", max_retries=1)

    def run(self, context):
        """
        context = {
            "test_name": str,
            "request": {
                "method": str,
                "url": str,
                "headers": dict,
                "body": dict
            },
            "response": {
                "status_code": int,
                "body": dict
            },
            "error": str
        }
        """
        self.logger.info(f"Healing: {context['test_name']}")

        while self.has_budget():
            observation = self.observe(context)
            action = self.think(observation)

            if action == "give_up":
                self.logger.info("Cannot fix autonomously.")
                break

            result = self.act(action, context)

            if result and result.get("healed"):
                self.logger.info(
                    f"Healed in {len(self.memory.attempts)} attempts!"
                )
                return {
                    "healed": True,
                    **self.get_report(),
                    "fix": result,
                }

            context["previous_attempt"] = result

        return {
            "healed": False,
            **self.get_report(),
        }

    def think(self, observation):
        """Decide what fix to try."""

        failure_type = classify_failure(
            observation.get("error", ""),
            observation.get("response", {}).get("status_code", 0),
        )

        history = json.dumps(self.memory.get_history(), indent=2)

        prompt = f"""
You are a test-healing agent.

Failure Type:
{failure_type}

Error:
{observation.get("error")}

Request:
{json.dumps(observation.get("request", {}), indent=2)}

Response:
{json.dumps(observation.get("response", {}), indent=2)}

Previous Attempts:
{history}

Choose ONE action:

- fix_payload
- fix_headers
- give_up

Return JSON:

{{
    "action": "...",
    "reasoning": "..."
}}
"""

        decision = ai.ask_json(prompt)

        if decision:
            self.logger.info(
                f"Decision: {decision.get('action')} - {decision.get('reasoning')}"
            )
            return decision.get("action", "give_up")

        return "give_up"

    def act(self, action, context):
        """Execute the selected fix."""

        fix = suggest_fix(
            context["request"],
            context["response"],
            context["error"],
        )

        if not fix:
            self.memory.add_attempt(action, "No fix generated", False)
            return None

        if action == "fix_payload" and fix.get("fixed_payload"):
            result = retry_request(
                method=context["request"].get("method", "POST"),
                url=context["request"].get("url", ""),
                payload=fix["fixed_payload"],
                headers=context["request"].get("headers", {}),
            )

        elif action == "fix_headers" and fix.get("fixed_headers"):
            result = retry_request(
                method=context["request"].get("method", "POST"),
                url=context["request"].get("url", ""),
                payload=context["request"].get("body", {}),
                headers=fix["fixed_headers"],
            )

        else:
            self.memory.add_attempt(action, "No applicable fix", False)
            return None

        success = result.get("status_code") in [200, 201]

        self.memory.add_attempt(action, result, success)

        if success:
            return {
                "healed": True,
                "fix": fix,
                "result": result,
            }

        return result