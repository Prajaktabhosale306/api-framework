class AgentMemory:
    """Tracks what the agent tried and results."""

    def __init__(self):
        self.attempts =[]

    def add_attempt(self, action, result, success):
        self.attempts.append({
            "action": action,
            "result": result,
            "success":success
        })
    def get_history(self):
        return [a for a in self.attempts if a["success"]]
    
    def failed_attempts(self):
        return [a for a in self.attempts if not a["success"]]
    
    def last_action(self):
        return self.attempts[-1] if self.attempts else None
    def clear(self):
        self.attempts = []
    