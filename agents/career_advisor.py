import json
from agents.base_agent import Agent


class CareerAdvisorAgent(Agent):

    def run(self, data: dict):

        prompt = f"""
You are an experienced career advisor.

Based on the following career market report:
{json.dumps(data, indent=2)}

Create a structured learning roadmap for becoming successful in this role.

IMPORTANT RULES:
1. FORMAT: Return ONLY valid JSON. Do NOT use markdown code blocks (no ```json).
2. STRUCTURE: learning_path must have EXACTLY 3 phases.
3. RESOURCES: Each phase must have at least 2 resources.
   - Allowed types: "course", "book", "documentation", "article".
4. PORTFOLIO: 
   - skills_demonstrated must include at least 3 technical skills from languages, frameworks 
   or infrastructure sections of skill_map.
5. GAP ANALYSIS:
  - quick_wins: TECHNICAL skills only (from languages/frameworks/infrastructure).
     These should be learnable in 2-4 weeks (narrow scope, beginner-friendly).
     DO NOT include soft skills.
   - long_term: ADVANCED TECHNICAL skills only (from languages/frameworks/infrastructure).
     These require 3+ months of dedicated study (complex, advanced).
     DO NOT include soft skills.
6. PORTFOLIO PROJECT:
   - Must describe a concrete, implementable project idea 
     with title, description, and list of technologies used.

JSON Schema:
{{
  "learning_path": [
    {{
      "phase": "Foundations (30 days)",
      "topics": ["topic"],
      "resources": [
        {{ "title": "resource title", "type": "course|book|documentation|article" }}
      ],
      "milestone": "achievable milestone"
    }},
    {{
      "phase": "Practice (30 days)",
      "topics": ["topic"],
      "resources": [
        {{ "title": "resource title", "type": "course|book|documentation|article" }}
      ],
      "milestone": "achievable milestone"
    }},
    {{
      "phase": "Portfolio (30 days)",
      "topics": ["topic"],
      "resources": [
        {{ "title": "resource title", "type": "course|book|documentation|article" }}
      ],
      "milestone": "achievable milestone"
    }}
  ],
  "gap_analysis": {{
    "quick_wins": ["skill"],
    "long_term": ["skill"]
  }},
  "portfolio_project": {{
    "title": "project title",
    "description": "project description",
    "skills_demonstrated": ["technology from skill_map"]
  }}
}}
"""

        result = self.llm.generate_json(prompt)

        data.update(result)

        return data