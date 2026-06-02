"""
Risk & SWOT Analysis View
Displays SWOT quadrants in a color-coded 2x2 grid and structured risk assessment cards.
"""

import re
import streamlit as st
from utils.ai_helper import get_risk_swot_analysis, is_api_available


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


# SWOT quadrant styling configuration
SWOT_CONFIG = {
    "strength": {"bg": "#ECFDF5", "border": "#059669", "text": "#065F46", "label": "🟢 Strengths"},
    "weakness": {"bg": "#FEF2F2", "border": "#DC2626", "text": "#991B1B", "label": "🔴 Weaknesses"},
    "opportunit": {"bg": "#EFF6FF", "border": "#2563EB", "text": "#1E40AF", "label": "🔵 Opportunities"},
    "threat": {"bg": "#FFF7ED", "border": "#EA580C", "text": "#9A3412", "label": "🟡 Threats"},
}


def render_risk_swot():
    """Renders the SWOT matrix and risk assessment view."""

    st.markdown("## ⚖️ Risk & SWOT Analysis")
    st.caption(
        "Strategic assessment of internal strengths and weaknesses, external opportunities and threats, "
        "plus detailed risk evaluation across market, technical, financial, and competitive dimensions."
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
    result = st.session_state.get("risk_swot_result")

    if not result:
        if st.button("⚡ Generate Risk & SWOT Analysis", type="primary", width='stretch'):
            with st.spinner("Evaluating strengths, weaknesses, opportunities, threats, and risk vectors…"):
                result = get_risk_swot_analysis(title, desc)
                st.session_state["risk_swot_result"] = result
                st.rerun()
        return

    # Re-generate button
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown(f"**Analyzing:** {title}")
    with col_btn:
        if st.button("🔄 Regenerate", width='stretch'):
            with st.spinner("Regenerating…"):
                st.session_state["risk_swot_result"] = get_risk_swot_analysis(title, desc)
                st.rerun()

    sections = _parse_sections(result)

    # ── SWOT Matrix ──
    st.markdown("### SWOT Matrix")

    # Classify sections
    swot_data = {}
    risk_content = None

    for header, content in sections:
        header_lower = header.lower()
        if "risk" in header_lower:
            risk_content = content
        else:
            for key in SWOT_CONFIG:
                if key in header_lower:
                    swot_data[key] = content
                    break

    # Render 2x2 grid
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2 = st.columns(2)

    grid_positions = [
        (row1_c1, "strength"),
        (row1_c2, "weakness"),
        (row2_c1, "opportunit"),
        (row2_c2, "threat"),
    ]

    for col, key in grid_positions:
        cfg = SWOT_CONFIG[key]
        content = swot_data.get(key, "Not yet analyzed.")
        with col:
            st.markdown(
                f"""<div style='background:{cfg["bg"]}; padding:16px; border-radius:10px;
                            border-left:5px solid {cfg["border"]}; min-height:200px; margin-bottom:12px;'>
                    <h4 style='color:{cfg["text"]}; margin-top:0;'>{cfg["label"]}</h4>
                </div>""",
                unsafe_allow_html=True,
            )
            st.markdown(content)

    # ── Risk Assessment ──
    if risk_content:
        st.markdown("---")
        st.markdown("### ⚠️ Risk Assessment")

        risk_subsections = _parse_subsections(risk_content)

        risk_icons = {
            "market": "📉",
            "technical": "⚙️",
            "financial": "💸",
            "competitive": "🏁",
        }

        for sub_title, sub_content in risk_subsections:
            icon = "⚠️"
            for key, ico in risk_icons.items():
                if key in sub_title.lower():
                    icon = ico
                    break

            with st.container(border=True):
                st.markdown(f"#### {icon} {sub_title}")
                st.markdown(sub_content)
