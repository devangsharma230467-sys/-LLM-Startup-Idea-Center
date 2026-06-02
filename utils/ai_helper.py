"""
FounderGPT AI Helper
Handles all Gemini API interactions and offline simulation fallbacks.
Provides three focused generation functions: Strategic Analysis, Risk & SWOT, and Advisor Chat.
"""

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"


def get_api_key():
    """Retrieves Gemini API key from session state or environment."""
    session_key = st.session_state.get("gemini_api_key", "")
    if session_key and len(session_key.strip()) > 5:
        st.sidebar.info("🔑 API key found in session state.")
        return session_key.strip()

    env_key = os.getenv("GEMINI_API_KEY", "")
    if env_key and len(env_key.strip()) > 5:
        st.sidebar.info("🔑 API key loaded from .env file.")
        return env_key.strip()

    st.sidebar.warning("⚠️ No Gemini API key detected.")
    return None


def is_api_available():
    """Returns True if a valid API key is configured and logs status."""
    available = get_api_key() is not None
    if not available:
        st.sidebar.error("⚠️ API connection not available: Key missing.")
    return available


def _call_gemini(prompt, system_instruction=None):
    """
    Internal helper to query Gemini API.
    Returns generated text on success, None on failure (triggers fallback).
    """
    key = get_api_key()
    if not key:
        st.sidebar.warning("⚠️ Gemini API key missing, cannot call API.")
        return None

    # Log start of request
    st.sidebar.info("🚀 Gemini request started…")
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
            ),
            system_instruction=system_instruction,
        )
        response = model.generate_content(prompt)
        # Log successful response
        st.sidebar.success("✅ Gemini response received.")
        return response.text
    except Exception as e:
        st.sidebar.warning(f"API error: {str(e)[:80]}… Using offline mode.")
        return None


# ─────────────────────────────────────────────
# 1. STRATEGIC ANALYSIS  (Market · Competitor · Revenue · Growth)
# ─────────────────────────────────────────────

STRATEGIC_SYSTEM = (
    "You are an elite startup strategist and market analyst. "
    "Write concise, realistic, and actionable business insights. "
    "Use markdown formatting with bullet points for readability."
)

STRATEGIC_PROMPT = """
Analyze the following startup idea and generate a comprehensive strategic profile.

**Startup Name:** {title}
**Description:** {desc}

Respond using EXACTLY these markdown headers and sub-sections:

### 🎯 Market Analysis
#### Target Audience
[Identify 3 specific customer personas with demographics and pain points.]
#### Market Demand
[Describe the current market need, industry trends, and demand drivers.]
#### Customer Segments
[Define 3 distinct customer segments with willingness-to-pay estimates.]

### 🔍 Competitor Analysis
#### Major Competitors
[List 3-4 direct or indirect competitors with brief descriptions.]
#### Competitor Strengths
[Identify what competitors do well and their market advantages.]
#### Market Positioning
[Explain how this startup should differentiate and position itself.]

### 💰 Revenue Model
#### Monetization Strategies
[Propose 2-3 realistic monetization approaches for this business.]
#### Pricing Suggestions
[Suggest specific pricing tiers with dollar amounts and justification.]
#### Revenue Streams
[Detail primary and secondary revenue streams with projected mix.]

### 🚀 Growth Strategy
#### Customer Acquisition
[Outline 3 specific acquisition channels with estimated CAC.]
#### Marketing Channels
[Recommend the most effective marketing channels for this business.]
#### Scaling Recommendations
[Provide a phased scaling roadmap: Month 1-3, Month 4-6, Month 7-12.]

Be specific to this startup. Avoid generic advice.
"""


def _simulate_strategic(title, desc):
    """High-quality offline fallback for strategic analysis."""
    return f"""### 🎯 Market Analysis
#### Target Audience
- **Primary Persona – The Busy Professional:** Ages 25-45, digitally native, time-constrained decision makers who need efficient solutions for {title.lower()}-related workflows. They value speed and simplicity over feature bloat.
- **Secondary Persona – The Growing SMB:** Small-to-medium businesses with 10-50 employees looking to streamline operations without enterprise-level pricing or complexity.
- **Tertiary Persona – The Tech-Savvy Freelancer:** Independent contractors and consultants seeking affordable, professional-grade tools to serve their own clients.

#### Market Demand
- The market for solutions addressing {title} is experiencing strong tailwinds driven by digital transformation and remote-work adoption.
- Industry research indicates a 15-20% year-over-year growth rate in adjacent software segments.
- Existing solutions are either overpriced enterprise suites or fragmented free tools, creating a clear gap for a mid-market product.

#### Customer Segments
- **Segment 1 – Solo Operators:** Willingness to pay $15-29/month for core features. Represent 60% of early adopters.
- **Segment 2 – Small Teams (2-10 people):** Willingness to pay $49-99/month for collaboration features. Key expansion revenue driver.
- **Segment 3 – Mid-Market Companies:** Willingness to pay $200-500/month for advanced integrations, compliance, and dedicated support.

### 🔍 Competitor Analysis
#### Major Competitors
- **Legacy Enterprise Players:** Large, established software vendors offering bloated solutions at $500+/month with complex onboarding processes.
- **Niche Point Solutions:** Small startups solving only one slice of the problem, forcing users to stitch together multiple tools.
- **DIY/Spreadsheet Approach:** Many potential customers currently use manual spreadsheets and email, representing untapped demand.

#### Competitor Strengths
- Legacy players benefit from brand recognition, existing customer lock-in, and large sales teams.
- Niche solutions are often free or very cheap, creating price-sensitive switching barriers.
- The DIY approach has zero cost, making the value proposition critical to articulate clearly.

#### Market Positioning
- Position {title} as the "professional-grade yet effortless" middle ground between expensive enterprise tools and fragmented free alternatives.
- Lead with **time-to-value**: users should experience core benefits within 5 minutes of sign-up.
- Emphasize simplicity, modern design, and transparent pricing as brand differentiators.

### 💰 Revenue Model
#### Monetization Strategies
- **Freemium SaaS Model:** Offer a generous free tier to drive adoption, with paid upgrades for advanced features and higher usage limits.
- **Usage-Based Pricing:** Charge based on consumption metrics (API calls, projects, team members) so pricing scales naturally with value delivered.

#### Pricing Suggestions
- **Free Tier:** Limited to 2 projects, 1 user. Serves as the acquisition funnel.
- **Pro Plan – $29/month:** Unlimited projects, priority support, export capabilities. Target conversion rate: 5-8% of free users.
- **Team Plan – $79/month:** Multi-user collaboration, admin controls, integrations. Target: growing teams ready to invest.

#### Revenue Streams
- **Primary (85%):** Monthly/annual SaaS subscriptions forming predictable recurring revenue.
- **Secondary (10%):** One-time professional setup or onboarding services for team accounts.
- **Tertiary (5%):** Affiliate partnerships or marketplace commissions from complementary tools.

### 🚀 Growth Strategy
#### Customer Acquisition
- **Content Marketing & SEO:** Publish high-value guides and templates related to {title.lower()}, targeting long-tail search queries. Estimated CAC: $8-15.
- **Product-Led Growth (PLG):** Free tier drives organic sign-ups; in-app prompts encourage upgrades. Estimated CAC: $3-8 for converted users.
- **Community Building:** Engage in relevant Reddit, Discord, and LinkedIn communities as a helpful expert, not a promoter. Estimated CAC: $5-10.

#### Marketing Channels
- **SEO & Blog Content:** Long-term compounding traffic engine; 6-12 month investment horizon.
- **Twitter/LinkedIn Thought Leadership:** Build founder brand and attract early adopters through authentic industry commentary.
- **Product Hunt & Indie Hackers Launch:** One-time spikes for initial traction and social proof.

#### Scaling Recommendations
- **Month 1-3 (Validate):** Launch MVP to 50-100 beta users. Focus on retention metrics and feature feedback. Target: 80%+ weekly active rate.
- **Month 4-6 (Optimize):** Refine onboarding flow, implement self-serve billing, and begin content marketing. Target: $2,000 MRR.
- **Month 7-12 (Scale):** Activate paid acquisition channels (LinkedIn ads, retargeting). Launch team plan. Target: $10,000 MRR and 500+ active users.
"""


def get_strategic_analysis(title, desc):
    """Generates strategic analysis via Gemini or offline fallback."""
    prompt = STRATEGIC_PROMPT.format(title=title, desc=desc)
    result = _call_gemini(prompt, STRATEGIC_SYSTEM)
    return result if result else _simulate_strategic(title, desc)


# ─────────────────────────────────────────────
# 2. RISK & SWOT ANALYSIS
# ─────────────────────────────────────────────

RISK_SWOT_SYSTEM = (
    "You are a seasoned business risk analyst and strategic consultant. "
    "Provide realistic, specific, and actionable SWOT and risk assessments. "
    "Use markdown formatting with bullet points."
)

RISK_SWOT_PROMPT = """
Perform a complete SWOT and Risk analysis for the following startup:

**Startup Name:** {title}
**Description:** {desc}

Respond using EXACTLY these markdown headers:

### 🟢 Strengths
[4 specific internal strengths of this startup concept. Be concrete, not generic.]

### 🔴 Weaknesses
[4 specific internal weaknesses, resource gaps, or operational challenges.]

### 🔵 Opportunities
[4 external market opportunities, trends, or partnership possibilities.]

### 🟡 Threats
[4 external threats including competitors, regulation, and market shifts.]

### ⚠️ Risk Assessment

#### Market Risks
[2-3 specific market-level risks such as demand uncertainty, timing, or adoption barriers.]

#### Technical Risks
[2-3 technical risks such as scalability challenges, dependency risks, or implementation complexity.]

#### Financial Risks
[2-3 financial risks such as runway constraints, unit economics, or pricing pressure.]

#### Competitive Risks
[2-3 competitive risks such as incumbent responses, new entrants, or substitute products.]

Tailor every point to this specific startup idea. Avoid generic statements.
"""


def _simulate_risk_swot(title, desc):
    """High-quality offline fallback for SWOT and risk analysis."""
    return f"""### 🟢 Strengths
- **Clear Problem-Solution Fit:** {title} addresses a well-defined pain point that existing solutions handle poorly or expensively.
- **Modern Technical Architecture:** Built with current technologies, enabling rapid iteration and lower maintenance overhead compared to legacy alternatives.
- **Low Initial Capital Requirements:** Can launch an MVP with a lean team of 2-3 people, minimizing burn rate during the validation phase.
- **Strong Value Proposition:** Delivers measurable time or cost savings that can be clearly communicated in marketing and sales conversations.

### 🔴 Weaknesses
- **Zero Brand Recognition:** Starting from scratch with no established reputation, customer base, or social proof to accelerate trust-building.
- **Limited Team Bandwidth:** A small founding team must juggle product development, customer support, marketing, and sales simultaneously.
- **Unproven Unit Economics:** Customer acquisition costs and lifetime value ratios are theoretical until validated with real paying customers.
- **Feature Gaps vs. Incumbents:** The MVP will necessarily lack advanced features that enterprise competitors offer, limiting appeal to larger accounts initially.

### 🔵 Opportunities
- **Remote Work Acceleration:** The shift toward distributed teams has dramatically increased demand for cloud-based productivity and workflow tools.
- **API Ecosystem Growth:** Integration partnerships with established platforms (Slack, Zapier, HubSpot) can provide built-in distribution channels.
- **Underserved Mid-Market:** Most solutions target either individual users or large enterprises, leaving small-to-medium teams poorly served.
- **AI-Powered Differentiation:** Incorporating intelligent automation features can create meaningful differentiation that is difficult for legacy players to replicate quickly.

### 🟡 Threats
- **Fast-Follower Risk:** If the concept gains traction, well-funded competitors could replicate core features within 3-6 months.
- **Platform Dependency:** Heavy reliance on third-party APIs or distribution channels creates vulnerability to pricing or policy changes.
- **Economic Downturn Sensitivity:** In tight budget environments, SMBs cut software spending first, increasing churn risk.
- **Regulatory Uncertainty:** Evolving data privacy regulations (GDPR, CCPA) may require costly compliance investments as the platform scales.

### ⚠️ Risk Assessment

#### Market Risks
- **Adoption Timing:** The market may not be ready for this specific approach, requiring more education and longer sales cycles than projected.
- **Demand Validation:** Initial interest from beta users does not guarantee willingness to pay at the proposed price points.

#### Technical Risks
- **Scalability Bottlenecks:** Architecture decisions made for MVP speed may create performance issues at 10x-100x user growth.
- **Integration Complexity:** Building reliable integrations with third-party platforms introduces ongoing maintenance burden and breaking-change risk.

#### Financial Risks
- **Runway Pressure:** Without external funding, the founding team has approximately 6-12 months to achieve product-market fit before capital constraints force difficult decisions.
- **Pricing Sensitivity:** Setting prices too high slows adoption; too low erodes margins and sets difficult-to-change anchoring expectations.

#### Competitive Risks
- **Incumbent Defensive Moves:** Established players may slash pricing or bundle competing features in response to emerging threats.
- **Talent Competition:** Recruiting skilled engineers and designers is challenging when competing against well-funded startups and tech giants offering higher compensation.
"""


def get_risk_swot_analysis(title, desc):
    """Generates SWOT + Risk analysis via Gemini or offline fallback."""
    prompt = RISK_SWOT_PROMPT.format(title=title, desc=desc)
    result = _call_gemini(prompt, RISK_SWOT_SYSTEM)
    return result if result else _simulate_risk_swot(title, desc)


# ─────────────────────────────────────────────
# 3. ADVISOR CHATBOT
# ─────────────────────────────────────────────




def query_advisor_chatbot(title, desc, analysis_context, history_list, question):
    """
    Queries the AI Startup Advisor chatbot.
    """
    headings = _extract_headings(analysis_context)
    system_instruction = f"""You are 'FounderGPT Advisor', an expert startup consultant, business analyst, product strategist, and investor advisor.
    You are advising a founder building: "{title}"
    
    Startup Description: {desc}
    
    Use the strategic analysis, risk analysis, and SWOT analysis (provided below) as context.
    
    When answering a business question, ALWAYS:
    1️⃣ Provide a **Direct Answer** that addresses the user’s question first.
    2️⃣ Follow with a **Reasoning** section explaining why this answer makes sense given the context.
    3️⃣ End with **Recommendations** that give concrete, actionable next steps.
    
    Include detailed business‑focused content for any of the following topics when relevant:
    - Target Audience
    - Competitors
    - Revenue Model
    - Pricing Strategy
    - Growth Strategy
    - Customer Acquisition
    - Risks
    - SWOT Analysis
    - Market Positioning
    - Investor Readiness
    
    Use markdown headings exactly as shown (### Direct Answer, ### Reasoning, ### Recommendations).
    Avoid generic advice like "talk to customers" or "validate demand" unless explicitly asked.
    Keep the response concise (<200 words) but rich in specifics.
    
    Strategic Analysis (Key areas: {', '.join(headings)}):
    {analysis_context}
    """

    # Format history
    history_text = ""
    for msg in history_list:
        role = "Founder" if msg["role"] == "user" else "Advisor"
        history_text += f"{role}: {msg['content']}\n\n"

    prompt = f"""Previous conversation:
{history_text}

Founder's new question: "{question}"

Respond as the startup advisor:"""

    result = _call_gemini(prompt, system_instruction)
    if result is not None:
        return result
    else:
        return "**Error:** Gemini API request failed. Please check the API key and network connection. Details are shown in the sidebar."

def _extract_headings(text):
    """Extract markdown headings from a block of text.
    Returns a list of heading titles without the leading '#'.
    """
    import re
    headings = []
    for line in text.splitlines():
        m = re.match(r'^(#{1,6})\s*(.+)', line)
        if m:
            headings.append(m.group(2).strip())
    return headings

