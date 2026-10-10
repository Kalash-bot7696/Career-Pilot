# -*- coding: utf-8 -*-
# app.py
# ---------------------------------------------------------------------------
# CareerPilot – AI Career Mentor
# Streamlit entry point — orchestrates all three agents in sequence.
# ---------------------------------------------------------------------------

import sys
import os

# Make sure Python can find the agents/ and utils/ packages regardless of
# the working directory from which `streamlit run app.py` is invoked.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import streamlit as st
from agents.skill_analyzer import run_skill_analyzer
from agents.career_agent    import run_career_agent
from agents.learning_agent  import run_learning_agent

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title = "CareerPilot – AI Career Mentor",
    page_icon  = "🧭",
    layout     = "centered",
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🧭 CareerPilot – AI Career Mentor")
st.markdown(
    "Get your **personalised career roadmap** powered by three AI agents "
    "running in sequence.  Fill in your profile below and click **Generate Roadmap**."
)
st.divider()

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
with st.form("profile_form"):
    st.subheader("📋 Your Student Profile")

    col1, col2 = st.columns(2)

    with col1:
        degree = st.text_input(
            "Degree / Branch",
            placeholder="e.g. B.Tech Computer Science",
        )
        year = st.selectbox(
            "Current Year",
            ["1st Year", "2nd Year", "3rd Year", "4th Year", "Recent Graduate"],
        )
        target_role = st.text_input(
            "Target Job Role",
            placeholder="e.g. Data Scientist, Full-Stack Developer",
        )

    with col2:
        tech_skills = st.text_area(
            "Technical Skills",
            placeholder="e.g. Python, SQL, Machine Learning basics",
            height=100,
        )
        soft_skills = st.text_area(
            "Soft Skills",
            placeholder="e.g. Communication, Teamwork, Problem Solving",
            height=100,
        )

    interests = st.text_area(
        "Interests",
        placeholder="e.g. AI/ML, Web development, Open Source",
        height=80,
    )
    projects = st.text_area(
        "Projects / Experience",
        placeholder="e.g. Built a sentiment analysis tool using NLTK; internship at XYZ as a web developer",
        height=100,
    )

    submitted = st.form_submit_button("🚀 Generate Roadmap", use_container_width=True)

# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------
def _validate(degree, tech_skills, target_role):
    """Return an error message string, or None if everything looks good."""
    if not degree.strip():
        return "Please enter your Degree / Branch."
    if not tech_skills.strip():
        return "Please list at least one Technical Skill."
    if not target_role.strip():
        return "Please enter a Target Job Role."
    return None

# ---------------------------------------------------------------------------
# Agent pipeline
# ---------------------------------------------------------------------------
if submitted:
    # ── Basic input validation ────────────────────────────────────────────
    error_msg = _validate(degree, tech_skills, target_role)
    if error_msg:
        st.error(f"⚠️ {error_msg}")
        st.stop()

    # Build the shared profile dict passed to every agent
    profile = {
        "degree"     : degree,
        "year"       : year,
        "tech_skills": tech_skills,
        "soft_skills": soft_skills,
        "interests"  : interests,
        "projects"   : projects,
        "target_role": target_role,
    }

    st.divider()
    st.subheader("🤖 AI Agents at Work…")

    # ── Agent 1 — Skill Analyzer ──────────────────────────────────────────
    with st.spinner("Agent 1 / 3 — Analysing your skills…"):
        skill_analysis = run_skill_analyzer(profile)

    if skill_analysis.startswith("⚠️ LLM Error:"):
        st.error(skill_analysis)
        st.stop()

    with st.expander("🔍 Agent 1 — Skill Analysis & Gaps", expanded=True):
        st.markdown(skill_analysis)

    # ── Agent 2 — Career Advisor ──────────────────────────────────────────
    with st.spinner("Agent 2 / 3 — Building your career recommendations…"):
        career_report = run_career_agent(profile, skill_analysis)

    if career_report.startswith("⚠️ LLM Error:"):
        st.error(career_report)
        st.stop()

    with st.expander("💼 Agent 2 — Career Recommendations", expanded=True):
        st.markdown(career_report)

    # ── Agent 3 — Learning Roadmap & Interview Prep ───────────────────────
    with st.spinner("Agent 3 / 3 — Crafting your learning roadmap & interview prep…"):
        learning_report = run_learning_agent(profile, skill_analysis)

    if learning_report.startswith("⚠️ LLM Error:"):
        st.error(learning_report)
        st.stop()

    with st.expander("📚 Agent 3 — Learning Roadmap & Interview Preparation", expanded=True):
        st.markdown(learning_report)

    # ── Success banner ────────────────────────────────────────────────────
    st.divider()
    st.success(
        "✅ Your personalised career roadmap is ready!  "
        "Scroll through each section above, or copy the content to save it."
    )

    # Download button — combine all reports into one text file
    combined_report = (
        f"# CareerPilot Report\n\n"
        f"**Name / Profile:** {degree} | {year} | {target_role}\n\n"
        f"---\n\n"
        f"## Agent 1 — Skill Analysis\n\n{skill_analysis}\n\n"
        f"---\n\n"
        f"## Agent 2 — Career Recommendations\n\n{career_report}\n\n"
        f"---\n\n"
        f"## Agent 3 — Learning Roadmap & Interview Prep\n\n{learning_report}\n"
    )
    st.download_button(
        label     = "⬇️ Download Full Report (.md)",
        data      = combined_report.encode("utf-8"),
        file_name = "careerpilot_report.md",
        mime      = "text/markdown",
        use_container_width = True,
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
    "CareerPilot · Powered by Groq &amp; Qwen · Built with Streamlit"
    "</p>",
    unsafe_allow_html=True,
)
