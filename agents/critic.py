import json
from agents.base_agent import Agent


class CriticAgent(Agent):

    def run(self, data: dict):

        prompt = f"""
You are a VERY strict AI report auditor.

Review the following multi-agent generated career report and return ONLY valid JSON:

{json.dumps(data, indent=2)}

CRITICAL VALIDATION RULES:

1. JSON STRUCTURE:
   - All required fields present (skill_map, salary_table, learning_path, gap_analysis, portfolio_project)
   - No empty strings in critical fields (market_trend_reason, description)

2. SKILL CONSISTENCY:
   - gap_analysis.quick_wins and long_term must contain TECHNICAL skills only (from languages/frameworks/infrastructure)
   - DO NOT allow soft skills in gap_analysis
   - skills_demonstrated must include ≥3 technologies from skill_map

3. SALARY VALIDATION:
   - Salary must increase: Junior < Middle < Senior < Lead
  - Check if salary levels match skill requirements:
     * If skill_map has many "critical" demand skills → salaries should be HIGH (Senior median ≥150k RUB or ≥4000 USD)
     * If skill_map has many "growing" trend skills → salaries should be COMPETITIVE (market trend = "growing")
     * If most skills are "nice-to-have" → salaries should be MODERATE (not inflated)
   - Verify consistency: High salaries must be justified by critical/growing skills
   - Deduct points if salaries don't match skill demand levels

4. LEARNING PATH:
   - Exactly 3 phases (Foundations, Practice, Portfolio)
   - Each phase must have ≥ 2 resources

5. LOGICAL CONTRADICTIONS (Most Important):
   - SKILL TREND vs LEARNING PATH:
     Check if any skill in `learning_path` or `gap_analysis` is marked as "declining" in `skill_map`.
     If a skill is declining, it should NOT be a priority for learning (unless it's for legacy maintenance, which must be explicitly stated).
     > If found: ADD WARNING and REDUCE score significantly.

   - SKILL DEMAND vs LEARNING PATH:
     Skills marked "critical" should appear in `learning_path` or `gap_analysis`. If critical skills are ignored, it's a bad plan.

SCORING:
- Give quality score for report
- Deduct 5 points for EACH violated rule or minor issues
- Deduct 10 points if salaries don't match skill demand levels
- Deduct 15 points if critical skills exist but salaries are too low
- If any critical rule violated, is_consistent = false   

Return ONLY valid JSON.

Format:

{{
  "quality_score": integer (0-100),
  "reason": "reason must explain the quality_score",
  "warnings": ["issues found"],
  "is_consistent": true or false
}}
"""

        result = self.llm.generate_json(prompt)

        data["verification"] = result

        return data