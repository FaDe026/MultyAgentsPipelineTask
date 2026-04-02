from datetime import datetime
from zoneinfo import ZoneInfo
from agents.base_agent import Agent


class MarketAnalystAgent(Agent):

    def run(self, data: dict):

        role = data["role"]

        prompt = f"""
Analyze the IT job market for the role: {role}

IMPORTANT RULES:
1. Return ONLY valid JSON. Do NOT use markdown code blocks (no ```json).
2. JSON KEYS must be CLEAN - NO trailing or leading spaces.
   - Use "skill_map" NOT "skill_map "
   - Use "languages" NOT "languages "
   - Use "name" NOT "name "
3. All string values must also be trimmed (no trailing spaces).

JSON format:

{{
  "skill_map": {{
    "languages": [
      {{
        "name": "string",
        "demand": "critical | important | nice-to-have",
        "trend": "growing | stable | declining"
      }}
    ],
    "frameworks": [
      {{
        "name": "technology name",
        "demand": "critical | important | nice-to-have",
        "trend": "growing | stable | declining"
      }}
    ],
    "infrastructure": [
      {{
        "name": "string",
        "demand": "critical | important | nice-to-have",
        "trend": "growing | stable | declining"
      }}
    ],
    "soft_skills": [
      {{
        "name": "string",
        "demand": "critical | important | nice-to-have",
        "trend": "growing | stable | declining"
      }}
    ]
  }}
}}
"""

        result = self.llm.generate_json(prompt)

        data["skill_map"] = result.get("skill_map", {})

        return data