import json
from agents.base_agent import Agent


class SalaryEstimatorAgent(Agent):

    def run(self, data: dict):

        skill_map = data["skill_map"]

        prompt = f"""
Given the following skills:

{json.dumps(skill_map, indent=2)}

Estimate realistic MONTHLY salary ranges.

Rules:
- Russia salaries must be in thousands of RUB per month
- Remote salaries must be in USD per month
- Use realistic market ranges
- Do NOT include explanations
- top_employers must contain 3-5 real companies
- market_trend_reason must be a non-empty string with 1-2 sentences explaining the market_trend

Return ONLY valid JSON for JSON schema without any comments.

JSON schema:

{{
  "salary_table": {{
    "Junior": {{
      "Moscow": {{"min": number, "median": number, "max": number}},
      "Regions_RF": {{"min": number, "median": number, "max": number}},
      "Remote_USD": {{"min": number, "median": number, "max": number}}
    }},
    "Middle": {{
      "Moscow": {{"min": number, "median": number, "max": number}},
      "Regions_RF": {{"min": number, "median": number, "max": number}},
      "Remote_USD": {{"min": number, "median": number, "max": number}}
    }},
    "Senior": {{
      "Moscow": {{"min": number, "median": number, "max": number}},
      "Regions_RF": {{"min": number, "median": number, "max": number}},
      "Remote_USD": {{"min": number, "median": number, "max": number}}
    }},
    "Lead": {{
      "Moscow": {{"min": number, "median": number, "max": number}},
      "Regions_RF": {{"min": number, "median": number, "max": number}},
      "Remote_USD": {{"min": number, "median": number, "max": number}}
    }}
  }},
  "market_trend": "growing | stable | declining",
  "market_trend_reason": "string",
  "top_employers": ["string"]
}}
"""

        result = self.llm.generate_json(prompt)

        data["salary_table"] = result.get("salary_table", {})
        data["market_trend"] = result.get("market_trend", "")
        data["market_trend_reason"] = result.get("market_trend_reason", "")
        data["top_employers"] = result.get("top_employers", [])

        return data