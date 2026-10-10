# agents/learning_agent.py
# ---------------------------------------------------------------------------
# Agent 3 — Learning Roadmap & Interview Prep
#
# Makes TWO separate LLM calls to stay within free-tier token limits.
#
#   Call 1 — Learning Plan
#     • 6-month roadmap
#     • Top 5 free resources
#     • 3 project ideas
#     • 2 certifications
#
#   Call 2 — Interview Preparation
#     • Technical topics to study
#     • DSA plan
#     • Behavioral tips
#     • Resume tips
#     • 30-day action plan
#
# Input: student profile + ONLY the ## Skill Gaps section (≤ 400 chars)
#        — NOT the full Agent 1 / Agent 2 outputs.
#
# Output: both call results merged into one combined markdown string.
# ---------------------------------------------------------------------------

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

_PLAN_PROMPT = """You are a learning coach for college students.
Use the student profile and skill gaps to create a focused study plan.

## Student Profile
- Degree / Branch : {degree}
- Current Year    : {year}
- Target Role     : {target_role}

## Skill Gaps
{skill_gaps}

## Instructions — Learning Plan
Write EXACTLY four markdown sections (use these headings verbatim):
### 6-Month Roadmap
- Month-by-month plan as bullets (6 bullets, one per month).

### Top 5 Free Resources
- List 5 free online resources (course/site name + one-line description).

### Project Ideas
- 3 project ideas that fill the skill gaps (title + one-line description each).

### Certifications
- 2 relevant certifications with provider and estimated cost.

Be brief. No filler text."""


_INTERVIEW_PROMPT = """You are an interview coach for college students.
Use the student profile and skill gaps to create an interview prep plan.

## Student Profile
- Target Role : {target_role}
- Current Year: {year}

## Skill Gaps
{skill_gaps}

## Instructions — Interview Prep
Write EXACTLY five markdown sections (use these headings verbatim):
### Technical Topics
- 4-5 key technical topics to study for {target_role} interviews.

### DSA Plan
- 3-4 data structures / algorithms to focus on with practice tips.

### Behavioral Tips
- 3 tips for HR / behavioral rounds (STAR method, etc.).

### Resume Tips
- 3 actionable resume tips for a fresher applying to {target_role}.

### 30-Day Action Plan
- Week-by-week tasks as bullets (4 bullets, one per week).

Be brief. No filler text."""


# ---------------------------------------------------------------------------
# Helper — extract Skill Gaps section from Agent 1 output
# ---------------------------------------------------------------------------
def _extract_skill_gaps(skill_analysis: str, max_chars: int = 400) -> str:
    """
    Pull out the '### Skill Gaps' section from Agent 1's markdown output.
    Falls back to a truncated slice of the full text if the section isn't found.
    """
    # Try to find content under the Skill Gaps heading
    match = re.search(
        r"###\s*Skill Gaps\s*\n(.*?)(?=\n###|\Z)",
        skill_analysis,
        re.DOTALL | re.IGNORECASE,
    )
    if match:
        gaps_text = match.group(1).strip()
    else:
        # Fallback: just use whatever text we have
        gaps_text = skill_analysis.strip()

    # Enforce the 400-char cap to keep the prompt small
    return gaps_text[:max_chars]


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------
def run_learning_agent(profile: dict, skill_analysis: str) -> str:
    """
    Run Agent 3 — Learning Roadmap & Interview Prep (two LLM calls).

    Parameters
    ----------
    profile        : Same profile dict used by Agents 1 & 2.
    skill_analysis : Full markdown output from Agent 1.
                     Only the Skill Gaps section (≤ 400 chars) is extracted
                     and passed to the LLM — never the full text.

    Returns
    -------
    str : Combined markdown string with both Learning Plan and Interview Prep.
    """
    # Extract only the skill gaps — keeps prompts small and focused
    skill_gaps = _extract_skill_gaps(skill_analysis)

    degree      = profile.get("degree",      "Not specified")
    year        = profile.get("year",        "Not specified")
    target_role = profile.get("target_role", "Not specified")

    # ── Call 1 : Learning Plan ────────────────────────────────────────────
    plan_prompt = _PLAN_PROMPT.format(
        degree      = degree,
        year        = year,
        target_role = target_role,
        skill_gaps  = skill_gaps,
    )
    learning_plan = call_llm(plan_prompt)

    # ── Call 2 : Interview Prep ───────────────────────────────────────────
    interview_prompt = _INTERVIEW_PROMPT.format(
        year        = year,
        target_role = target_role,
        skill_gaps  = skill_gaps,
    )
    interview_prep = call_llm(interview_prompt)

    # ── Merge both outputs ────────────────────────────────────────────────
    combined = (
        "## 📚 Learning Roadmap\n\n"
        + learning_plan
        + "\n\n---\n\n"
        + "## 🎯 Interview Preparation\n\n"
        + interview_prep
    )
    return combined
