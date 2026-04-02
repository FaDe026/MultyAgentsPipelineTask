from datetime import datetime
from zoneinfo import ZoneInfo

class AgentPipeline:

    def __init__(self, agents):
        self.agents = agents

    def run(self, role: str):

        data = {
            "role": role,
            "generated_at": datetime.now(
                ZoneInfo("Europe/Moscow")
            ).replace(microsecond=0).isoformat()
        }

        for i, agent in enumerate(self.agents, start=1):

            name = agent.__class__.__name__
            print(f"\n=== Agent {i}: {name} ===")
            data = agent.run(data)

        return data