from datetime import datetime
from zoneinfo import ZoneInfo

class AgentPipeline:

    def __init__(self, agents):
        self.agents = agents

    def run(self, role: str) -> dict:
        print(f"\n=== Agent 1: {self.agents[0].__class__.__name__} ===")
        data = self.agents[0].run(role)

        for i, agent in enumerate(self.agents[1:], start=2):

            name = agent.__class__.__name__
            print(f"\n=== Agent {i}: {name} ===")
            data = agent.run(data)

        return {
            "role": role,
            "generated_at": datetime.now(
                ZoneInfo("Europe/Moscow")
            ).replace(microsecond=0).isoformat(),
            **data
        }