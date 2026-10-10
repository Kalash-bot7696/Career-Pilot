# agents/skill_analyzer.py
# ---------------------------------------------------------------------------
# Agent 1 — Skill Analyzer
#
# Takes the student profile and returns a structured markdown report with
# three sections:
#   ## Current Skills
#   ## Required Skills  (for the target role)
#   ## Skill Gaps       (with brief reasons)
# ---------------------------------------------------------------------------

import sys
import os

# Ensure the careerpilot package root is on the path when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------
_PROMPT_TEMPLATE = """You are a career counselor for college students.
Analyze the student profile below and produce a concise markdown report.

## Student Profile
- Degree / Branch : {degree}
- Current Year    : {year}
- Technical Skills: {tech_skills}
- Soft Skills     : {soft_skills}
- Interests       : {interests}
- Projects        : {projects}
- Target Role     : {target_role}

## Instructions
Write EXACTLY three markdown sections (use these headings verbatim):
### Current Skills
- Bullet each skill the student already has (max 5 bullets).

### Required Skills
- Bullet the key skills needed for {target_role} (max 5 bullets).

### Skill Gaps
- Bullet each missing skill with a one-line reason why it matters (max 5 bullets).

Be brief. 2-3 bullets per section minimum. No filler text."""


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------
def run_skill_analyzer(profile: dict) -> str:
    """
    Run Agent 1 — Skill Analyzer.

    Parameters
    ----------
    profile : dict with keys:
              degree, year, tech_skills, soft_skills,
              interests, projects, target_role

    Returns
    -------
    str : Markdown-formatted skill analysis report.
    """
    prompt = _PROMPT_TEMPLATE.format(
        degree      = profile.get("degree",      "Not specified"),
        year        = profile.get("year",        "Not specified"),
        tech_skills = profile.get("tech_skills", "Not specified"),
        soft_skills = profile.get("soft_skills", "Not specified"),
        interests   = profile.get("interests",   "Not specified"),
        projects    = profile.get("projects",    "Not specified"),
        target_role = profile.get("target_role", "Not specified"),
    )
    return call_llm(prompt)
