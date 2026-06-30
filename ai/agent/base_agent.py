from abc import ABC, abstractmethod
from ai.agent.memory import AgentMemory
from utils.logger import get_logger

class BaseAgent(ABC):
    """Every agent follows: observe -> Act -> Observe loop"""
    
    def __init__(self, name, max_retries=3):
        self.name = name
        self.memory= AgentMemory()
        self.max_retries = max_retries
        self.logger = get_logger(f"agent.{name}")

    @abstractmethod
    def run(self, context):
        """Main agent loop. override in each agent."""
        pass

    def observe(self, context):
        """Gather inforamation about situation.."""
        self.logger.info(f"[{self.name}] Observing...")
        return context
    
    @abstractmethod
    def think(self, obsevation):
        """Decide what action to take"""
        pass
    
    @abstractmethod
    def act(self, action, context):
        """Execute the decided action."""
        pass
    
    def has_budget(self):
        return len(self.memory.attempts)<self.max_retries
    def get_report(self):
        return{
            "agent":self.name,
            "attempts":self.memory.get_history(),
            "total_actions":len(self.memory.attempts)
        }