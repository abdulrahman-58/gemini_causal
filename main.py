import streamlit as st
import os
import time
from dotenv import load_dotenv
from google import genai

# ---------------- ENV ----------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Gemini 3 – Causal Analyzer",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.analysis-card {
    background-color: #ffffff;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-top: 20px;
}
.small-muted {
    color: #555;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🔥 Gemini 3 Causal Analyzer")
st.markdown(
    "<span class='small-muted'>Abdul Rahman Azam• Analyze root causes , assumptions & counterfactuals</span>",
    unsafe_allow_html=True
)
st.divider()

# ---------------- SESSION STATE ----------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "auto_run" not in st.session_state:
    st.session_state.auto_run = False

# ---------------- DEMO ----------------
st.subheader("⚡ Quick Demo (1-Click)")

example_1 = """Month 1: Strong signups after launch
Month 2: Low conversion to paid plans
Month 4: Added multiple new features
Month 8: Burn rate exceeded revenue, startup shut down"""

example_2 = """After increasing delivery fees, user retention dropped.
Marketing spend increased to compensate, but margins worsened.
Team responded by adding loyalty features."""

col1, col2 = st.columns(2)

if col1.button("🚀 Startup Failure"):
    st.session_state.input_text = example_1
    st.session_state.auto_run = True

if col2.button("📉 Business Decision"):
    st.session_state.input_text = example_2
    st.session_state.auto_run = True

# ---------------- INPUT ----------------
with st.form("analyze_form"):
    st.subheader("📝 Scenario Input")

    user_input = st.text_area(
        "Type your scenario (Ctrl + Enter to analyze):",
        height=170,
        placeholder="Describe events, decisions, KPIs, or timeline..."
    )

    submitted = st.form_submit_button(
        "🔍 Analyze with Gemini 3",
        use_container_width=True
    )

# ---------------- INPUT SELECTION (CRITICAL FIX) ----------------
input_to_analyze = ""

if st.session_state.auto_run and st.session_state.input_text.strip():
    input_to_analyze = st.session_state.input_text
elif submitted and user_input.strip():
    input_to_analyze = user_input

# ---------------- ANALYSIS ----------------
if input_to_analyze:
    st.session_state.auto_run = False

    with st.spinner("Gemini 3 is reasoning step-by-step..."):

        prompt = f"""
You are a senior product strategist and causal reasoning expert.

Analyze the scenario and produce a HIGH-SIGNAL report.

Rules:
- Bullet points only
- Max 5 bullets per section
- Clear cause → effect language

Return EXACTLY in this format:

## 📅 Timeline
- ...

## 🎯 Root Causes
- ...

## 🔗 Causal Chain
- A → B → C

## 🧠 Hidden Assumptions
- ...

## 🔄 Counterfactuals
- ...

## ✅ Key Takeaways
- ...

Scenario:
{input_to_analyze}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

    st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
    st.subheader("📊 Gemini 3 Analysis Report")

    with st.expander("📊 View Analysis (Click to Expand)", expanded=True):
        output_box = st.empty()

    rendered = ""
    for line in response.text.split("\n"):
        rendered += line + "\n"
        output_box.markdown(rendered)
        time.sleep(0.02)

    st.markdown("</div>", unsafe_allow_html=True)

    # ✅ CLEAR INPUT AFTER RESPONSE
    st.session_state.input_text = ""

# ---------------- FOOTER ----------------
st.divider()
st.caption("Built by Abdul Rahman Azam • Powered by Gemini 3")
