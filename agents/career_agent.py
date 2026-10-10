# agents/career_agent.py
# ---------------------------------------------------------------------------
# Agent 2 — Career Advisor
#
# Takes the student profile AND the Skill Analyzer output (Agent 1) and
# returns a structured markdown report with seven sections:
#   ## Primary Career Path
#   ## Alternative Paths
#   ## Industry Outlook
#   ## Salary Ranges
#   ## Top Hiring Companies
#   ## Strengths
#   ## Challenges
# ---------------------------------------------------------------------------

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------
_PROMPT_TEMPLATE = """You are a senior career advisor for college students in India.
Use the student profile and skill analysis below to give career guidance.

## Student Profile
- Degree / Branch : {degree}
- Current Year    : {year}
- Technical Skills: {tech_skills}
- Target Role     : {target_role}

## Skill Analysis Summary
{skill_analysis}

## Instructions
Write EXACTLY seven markdown sections (use these headings verbatim):
### Primary Career Path
- One recommended path with a one-line rationale.

### Alternative Paths
- 2-3 alternative career paths as bullets.

### Industry Outlook
- 2-3 bullets on demand, growth trends, and future prospects.

### Salary Ranges
- Entry-level and mid-level salary in India (₹ LPA) and globally (USD/yr).

### Top Hiring Companies
- 4-5 companies hiring for {target_role} (mix of Indian and global).

### Strengths
- 2-3 existing strengths the student can leverage.

### Challenges
- 2-3 challenges they may face and brief mitigation tips.

Be brief. Use bullet points. No filler text."""


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------
def run_career_agent(profile: dict, skill_analysis: str) -> str:
    """
    Run Agent 2 — Career Advisor.

    Parameters
    ----------
    profile        : Same dict used by Agent 1.
    skill_analysis : Full markdown output from Agent 1.

    Returns
    -------
    str : Markdown-formatted career recommendation report.
    """
    # Truncate skill_analysis to ~800 chars to stay within prompt token budget
    truncated_analysis = skill_analysis[:800]

    prompt = _PROMPT_TEMPLATE.format(
        degree         = profile.get("degree",      "Not specified"),
        year           = profile.get("year",        "Not specified"),
        tech_skills    = profile.get("tech_skills", "Not specified"),
        target_role    = profile.get("target_role", "Not specified"),
        skill_analysis = truncated_analysis,
    )
    return call_llm(prompt)
