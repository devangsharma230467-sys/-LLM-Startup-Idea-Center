"""
FounderGPT — AI Startup Validation Platform
Main application entrypoint.
Handles page config, custom theming, sidebar navigation, and view routing.
"""

import streamlit as st

# ── Page Config (must be first Streamlit command) ──
st.set_page_config(
    page_title="FounderGPT – Startup Validation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

import os
from dotenv import load_dotenv

from views.idea_input import render_idea_input
from views.strategic_analysis import render_strategic_analysis
from views.risk_swot import render_risk_swot
from views.chatbot import render_chatbot

from utils.ai_helper import is_api_available

# Startup API detection log
if is_api_available():
    st.sidebar.success("🔑 Gemini API key detected successfully.")
else:
    st.sidebar.error("⚠️ Gemini API key not found. Please set GEMINI_API_KEY in .env.")

# ── Session State Initialization ──
DEFAULTS = {
    "startup_title": "",
    "startup_desc": "",
    "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
    "active_view": "🚀 Idea Center",
    "strategic_result": None,
    "risk_swot_result": None,
    "chat_history": [],
}

for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Custom CSS Theme ──
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Clean background */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    }

    /* Card containers */
    div[data-testid="stVerticalBlockBorderContainer"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }

    /* Sidebar */
    div[data-testid="stSidebar"] {
        background: #0F172A !important;
    }

    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3,
    div[data-testid="stSidebar"] h4,
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] span,
    div[data-testid="stSidebar"] label {
        color: #F1F5F9 !important;
    }

    div[data-testid="stSidebar"] button {
        background: #1E293B !important;
        color: #F1F5F9 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stSidebar"] button:hover {
        background: #0F766E !important;
        border-color: #0F766E !important;
    }

    /* Headings */
    h1, h2, h3, h4 { color: #1E293B; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ──
with st.sidebar:
    # Logo & Title
    st.markdown(
        """
        <div style='text-align:center; padding:20px 0 10px;'>
            <h1 style='font-size:1.6rem; margin:0; color:#F8FAFC;'>🚀 FounderGPT</h1>
            <p style='color:#64748B; font-size:0.8rem; margin-top:4px;'>AI Startup Validator</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # API Key Input
    # Gemini API key is loaded from the environment via .env file.
    if not st.session_state["gemini_api_key"]:
        st.error(
            "⚠️ Gemini API key is not configured. Please set `GEMINI_API_KEY` in a `.env` file at the project root."
        )
        # Optionally, you could stop execution of features that require the key.
        # st.stop()


    st.divider()

    # Navigation
    st.markdown("##### 🧭 Navigation")
    nav_options = [
        "🚀 Idea Center",
        "📋 Strategic Analysis",
        "⚖️ Risk & SWOT",
        "🤖 AI Advisor",
    ]

    selected = st.radio("Go to", nav_options, label_visibility="collapsed")
    st.session_state["active_view"] = selected

    # Active Venture Card
    title = st.session_state.get("startup_title")
    desc = st.session_state.get("startup_desc")

    st.markdown("<br/>", unsafe_allow_html=True)

    if title:
        st.markdown(
            f"""
            <div style='background:#1E293B; padding:14px; border-radius:10px;
                        border-left:4px solid #0F766E;'>
                <span style='color:#0F766E; font-weight:600; font-size:0.75rem;
                             text-transform:uppercase;'>Active Startup</span>
                <h4 style='color:#F8FAFC; margin:4px 0 2px; font-size:1rem;'>{title}</h4>
                <p style='color:#94A3B8; font-size:0.78rem; margin:0;
                          line-height:1.3;'>{desc[:90]}…</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style='background:#1E293B; padding:14px; border-radius:10px;
                        border-left:4px solid #475569; text-align:center;'>
                <p style='color:#94A3B8; font-size:0.8rem; margin:0;'>
                    No startup loaded yet
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown(
        """
        <div style='text-align:center; margin-top:40px; color:#475569; font-size:0.7rem;'>
            FounderGPT v2.0 · Simplified Edition
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Main Content Router ──
view = st.session_state["active_view"]

if view == "🚀 Idea Center":
    render_idea_input()
elif view == "📋 Strategic Analysis":
    render_strategic_analysis()
elif view == "⚖️ Risk & SWOT":
    render_risk_swot()
elif view == "🤖 AI Advisor":
    render_chatbot()
