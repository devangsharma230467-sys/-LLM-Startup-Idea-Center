"""
Startup Idea Input View
Provides a clean form for entering startup details with quick-load demo profiles.
"""

import streamlit as st


# Pre-configured demo profiles for instant demonstration
DEMO_PROFILES = {
    "🌱 SolarGrid (CleanTech)": {
        "title": "SolarGrid",
        "desc": (
            "A decentralized smart microgrid platform enabling neighborhood residents "
            "to store excess residential solar energy and trade it peer-to-peer over "
            "secure digital ledgers, cutting energy bills by 30%."
        ),
    },
    "🩺 ClinicaScribe (HealthTech)": {
        "title": "ClinicaScribe",
        "desc": (
            "An AI medical scribe that runs on clinicians' tablets, listens to "
            "patient-doctor conversations, filters ambient noise, and outputs "
            "structured electronic health records in real-time."
        ),
    },
    "👗 FitMesh (E-commerce)": {
        "title": "FitMesh",
        "desc": (
            "A virtual 3D garment fitting API for online fashion brands, using "
            "smartphone camera body-scanning to match customers with precise sizes, "
            "reducing product return rates by 45%."
        ),
    },
}


def render_idea_input():
    """Renders the startup idea input form."""

    st.markdown("## 🚀 Startup Idea Center")
    st.caption(
        "Enter your startup concept below, or load a demo profile to explore the platform instantly."
    )

    st.divider()

    # ── Quick-Load Demo Profiles ──
    st.markdown("#### 💡 Quick-Load Demo Profiles")
    cols = st.columns(3)

    for idx, (label, profile) in enumerate(DEMO_PROFILES.items()):
        with cols[idx]:
            if st.button(label, width='stretch'):
                st.session_state["startup_title"] = profile["title"]
                st.session_state["startup_desc"] = profile["desc"]
                _clear_analysis_cache()
                st.rerun()

    st.markdown("")

    # ── Input Form ──
    with st.container(border=True):
        st.markdown("#### Enter Startup Details")

        title_val = st.text_input(
            "Startup Name",
            value=st.session_state.get("startup_title", ""),
            placeholder="e.g. SolarGrid, ClinicaScribe, FitMesh",
        )

        desc_val = st.text_area(
            "Describe your startup idea",
            value=st.session_state.get("startup_desc", ""),
            placeholder=(
                "What problem does it solve? Who is the customer? "
                "How does the product work? What makes it unique?"
            ),
            height=150,
        )

        if st.button("💾 Save & Begin Analysis", type="primary", width='stretch'):
            if not title_val.strip() or not desc_val.strip():
                st.error("Please provide both a name and description.")
            else:
                st.session_state["startup_title"] = title_val.strip()
                st.session_state["startup_desc"] = desc_val.strip()
                _clear_analysis_cache()
                st.success(f"✅ '{title_val.strip()}' saved! Navigate to other tabs to generate analysis.")
                st.rerun()

    # ── Active Venture Banner ──
    title = st.session_state.get("startup_title")
    desc = st.session_state.get("startup_desc")

    if title and desc:
        st.markdown(
            f"""
            <div style='background:#F0FDF4; padding:16px; border-radius:10px;
                        border-left:4px solid #059669; margin-top:16px;'>
                <strong style='color:#059669;'>Active Startup:</strong>
                <strong style='color:#1E293B;'> {title}</strong><br/>
                <span style='color:#64748B; font-size:0.9rem;'>{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _clear_analysis_cache():
    """Clears all previously generated analysis when the idea changes."""
    for key in ["strategic_result", "risk_swot_result", "chat_history"]:
        st.session_state.pop(key, None)
