"""
Strategic Analysis View
Displays Market Analysis, Competitor Analysis, Revenue Model, and Growth Strategy
in a clean tabbed layout with card-based rendering.
"""

import re
import streamlit as st
from utils.ai_helper import get_strategic_analysis, is_api_available


def _parse_sections(text):
    """Splits markdown text by ### headers into (title, content) pairs."""
    pattern = r"###\s+(.*?)\n(.*?)(?=\n###\s+|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        return [("Analysis", text)]
    return [(m[0].strip(), m[1].strip()) for m in matches]


def _parse_subsections(text):
    """Splits markdown text by #### sub-headers into (title, content) pairs."""
    pattern = r"####\s+(.*?)\n(.*?)(?=\n####\s+|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        return [("Details", text)]
    return [(m[0].strip(), m[1].strip()) for m in matches]


def render_strategic_analysis():
    """Renders the full strategic analysis view."""

    st.markdown("## 📋 Strategic Analysis")
    st.caption(
        "AI-generated market intelligence, competitive positioning, revenue models, and growth roadmap."
    )
    st.divider()

    title = st.session_state.get("startup_title")
    desc = st.session_state.get("startup_desc")

    if not title or not desc:
        st.warning("⬅️ Please save a startup idea in the **Idea Center** first.")
        return

    if not is_api_available():
        st.info("📡 **Offline Mode** — No API key detected. Showing simulated analysis.")

    # Generate or retrieve cached result
    result = st.session_state.get("strategic_result")

    if not result:
        if st.button("🔍 Generate Strategic Analysis", type="primary", width='stretch'):
            with st.spinner("Analyzing market, competitors, revenue, and growth strategies…"):
                result = get_strategic_analysis(title, desc)
                st.session_state["strategic_result"] = result
                st.rerun()
        return

    # Re-generate button
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown(f"**Analyzing:** {title}")
    with col_btn:
        if st.button("🔄 Regenerate", width='stretch'):
            with st.spinner("Regenerating…"):
                st.session_state["strategic_result"] = get_strategic_analysis(title, desc)
                st.rerun()

    # Parse into the 4 major sections
    sections = _parse_sections(result)

    # Map section keywords to tab labels
    tab_map = [
        ("market", "🎯 Market"),
        ("competitor", "🔍 Competitors"),
        ("revenue", "💰 Revenue"),
        ("growth", "🚀 Growth"),
    ]

    # Create tabs
    tab_labels = [label for _, label in tab_map]
    tabs = st.tabs(tab_labels)

    for tab_idx, (keyword, _) in enumerate(tab_map):
        with tabs[tab_idx]:
            # Find matching section
            matched = False
            for header, content in sections:
                if keyword in header.lower():
                    # Parse subsections within this section
                    subsections = _parse_subsections(content)
                    for sub_title, sub_content in subsections:
                        with st.container(border=True):
                            st.markdown(f"**{sub_title}**")
                            st.markdown(sub_content)
                    matched = True
                    break

            if not matched:
                st.info("This section was not generated. Try regenerating the analysis.")
