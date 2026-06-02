"""
AI Startup Advisor Chatbot View
Context-aware conversational interface that uses the user's startup idea
and all generated analyses to provide tailored strategic advice.
"""

import streamlit as st
from utils.ai_helper import query_advisor_chatbot, is_api_available


# Suggested starter questions
SUGGESTIONS = [
    ("💸", "How should I monetize this startup?"),
    ("🔍", "Who are my main competitors?"),
    ("🛠️", "What features should I build first?"),
    ("⚠️", "What are the biggest risks?"),
]


def _build_analysis_context():
    """Aggregates all generated analyses into a single context string for the chatbot."""
    parts = []

    strategic = st.session_state.get("strategic_result")
    if strategic:
        parts.append(f"=== Strategic Analysis ===\n{strategic[:1500]}")

    risk_swot = st.session_state.get("risk_swot_result")
    if risk_swot:
        parts.append(f"=== Risk & SWOT Analysis ===\n{risk_swot[:1500]}")

    if not parts:
        return "No analyses have been generated yet. Provide general startup advice based on the idea description."

    return "\n\n".join(parts)


def render_chatbot():
    """Renders the AI Startup Advisor chat interface."""

    st.markdown("## 🤖 AI Startup Advisor")
    st.caption(
        "Ask questions about your startup — monetization, competitors, features, risks, and more. "
        "The advisor uses your idea and all generated analyses as context."
    )
    st.divider()

    title = st.session_state.get("startup_title")
    desc = st.session_state.get("startup_desc")

    if not title or not desc:
        st.warning("⬅️ Please save a startup idea in the **Idea Center** first.")
        return

    if not is_api_available():
        st.info("📡 **Offline Mode** — No API key detected. Showing simulated responses.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # ── Suggestion Chips ──
    st.markdown("##### 💡 Quick Questions")
    cols = st.columns(len(SUGGESTIONS))
    suggested_q = None

    for idx, (icon, question) in enumerate(SUGGESTIONS):
        with cols[idx]:
            if st.button(f"{icon} {question.split('?')[0]}?", width='stretch'):
                suggested_q = question

    st.markdown("")

    # ── Chat History Display ──
    # Welcome message
    with st.chat_message("assistant"):
        st.markdown(
            f"Hi! I'm your **FounderGPT Advisor**. I've reviewed **{title}** and I'm ready "
            f"to help you with strategy, positioning, and growth. What would you like to explore?"
        )

    # Render previous messages
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Handle Input ──
    user_input = st.chat_input("Ask your advisor anything…")
    question = user_input or suggested_q

    if question:
        # Show user message
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state["chat_history"].append({"role": "user", "content": question})

        # Build context from all generated analyses
        analysis_context = _build_analysis_context()

        # Query advisor
        with st.spinner("Thinking…"):
            response = query_advisor_chatbot(
                title=title,
                desc=desc,
                analysis_context=analysis_context,
                history_list=st.session_state["chat_history"][:-1],
                question=question,
            )

        # Show response
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        st.rerun()

    # ── Clear History ──
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state["chat_history"] = []
        st.rerun()
