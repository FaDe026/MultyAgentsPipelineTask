import json
import os
from dotenv import load_dotenv
import re

load_dotenv()
REPORT_DIR = os.getenv("REPORT_DIR")


def ensure_report_dir():
    os.makedirs(REPORT_DIR, exist_ok=True)

def role_to_filename(role: str):
    role = role.lower()
    role = re.sub(r"\s+", "_", role)
    role = re.sub(r"[^\w_]", "", role)
    return f"{role}_report"


def save_json(data):
    ensure_report_dir()

    role = data.get("role", "unknown")
    filename = role_to_filename(role) + "_report.json"

    path = os.path.join(REPORT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_keys(obj):
    if isinstance(obj, dict):
        return {k.strip(): clean_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_keys(item) for item in obj]
    return obj


def save_markdown(data):
    ensure_report_dir()

    data = clean_keys(data)

    role = data.get("role", "unknown")
    filename = role_to_filename(role) + "_report.md"
    path = os.path.join(REPORT_DIR, filename)

    skill_map = data.get("skill_map", {})
    skill_rows = []
    for category, skills in skill_map.items():
        for skill in skills:
            skill_rows.append(
                f"| {category} | {skill.get('name', 'N/A')} | "
                f"{skill.get('demand', 'N/A')} | {skill.get('trend', 'N/A')} |"
            )
    skill_map_md = "| Категория | Навык | Востребованность | Тренд |\n|-----------|-------|------------------|-------|\n" + "\n".join(skill_rows)

    salary_table = data.get("salary_table", {})
    salary_rows = []
    for grade, regions in salary_table.items():
        for region, values in regions.items():
            salary_rows.append(
                f"| {grade} | {region} | {values.get('min', 'N/A')} | "
                f"{values.get('median', 'N/A')} | {values.get('max', 'N/A')} |"
            )
    salary_table_md = "| Грейд | Регион | Min | Median | Max |\n|-------|--------|-----|--------|-----|\n" + "\n".join(salary_rows)

    learning_path = data.get("learning_path", [])
    learning_rows = []
    for phase in learning_path:
        resources = phase.get("resources", [])
        resource_titles = ", ".join([r.get("title", "") for r in resources])
        learning_rows.append(
            f"### {phase.get('phase', 'Phase')}\n"
            f"**Темы:** {', '.join(phase.get('topics', []))}\n\n"
            f"**Ресурсы:** {resource_titles}\n\n"
            f"**Milestone:** {phase.get('milestone', '')}\n"
        )
    learning_path_md = "\n".join(learning_rows)

    gap_analysis = data.get("gap_analysis", {})
    gap_analysis_md = (
        f"**Quick Wins (2-4 недели):** {', '.join(gap_analysis.get('quick_wins', []))}\n\n"
        f"**Long Term (3+ месяца):** {', '.join(gap_analysis.get('long_term', []))}"
    )

    portfolio = data.get("portfolio_project", {})
    portfolio_md = (
        f"### {portfolio.get('title', 'N/A')}\n\n"
        f"{portfolio.get('description', 'N/A')}\n\n"
        f"**Технологии:** {', '.join(portfolio.get('skills_demonstrated', []))}"
    )

    top_employers = data.get("top_employers", [])
    market_trend = data.get("market_trend", "N/A")
    market_trend_reason = data.get("market_trend_reason", "N/A")

    verification = data.get("verification", {})
    quality_score = verification.get("quality_score", "N/A")
    quality_reason = verification.get("reason", "N/A")
    warnings = verification.get("warnings", [])

    md = f"""# Career Market Report

**Role:** {role}

**Generated at:** {data.get("generated_at", "Unknown")}

---

## Skill Map

{skill_map_md}

---

## Salary Table

{salary_table_md}

---

## Market Trend

**Trend:** {market_trend}

**Reason:** {market_trend_reason}

---

## Top Employers

{', '.join(top_employers) if top_employers else 'N/A'}

---

## Learning Path

{learning_path_md}

---

## Gap Analysis

{gap_analysis_md}

---

## Portfolio Project

{portfolio_md}

---

## Verification

**Quality Score:** {quality_score}/100
**Reason:** {quality_reason}

**Warnings:**
{chr(10).join(f'- {w}' for w in warnings) if warnings else '- No warnings'}

**Is Consistent:** {verification.get('is_consistent', 'N/A')}
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(md)