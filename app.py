import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from engine.scoring import LeadScoreCard

# 1. SETUP & COMPLIANCE (Module 7)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="Solar Sales AI - Germany", layout="wide")

# Mandatory Legal Disclaimer
st.info("⚖️ **Compliance-Hinweis:** Schätzungen sind unverbindlich. Wir bieten keine Rechts- oder Steuerberatung.")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "score_card" not in st.session_state:
    st.session_state.score_card = LeadScoreCard()
if "step" not in st.session_state:
    st.session_state.step = 0

# 2. SIDEBAR DASHBOARD (Module 6: Sales Handoff)
with st.sidebar:
    st.title("👨‍💼 Sales Dashboard")
    scores = st.session_state.score_card.scores

    st.subheader("Live Lead Scores")

    # FIX: Using min/max to ensure value is always between 0.0 and 1.0 for Streamlit
    tech_val = min(scores['Technical'] / 10, 1.0)
    fin_val = min(scores['Financial'] / 20, 1.0)  # Divided by 20 to handle your higher scores
    int_val = min(scores['Intent'] / 10, 1.0)

    st.progress(tech_val, text=f"Technical: {scores['Technical']}/10")
    st.progress(fin_val, text=f"Financial: {scores['Financial']}/20")
    st.progress(int_val, text=f"Intent: {scores['Intent']}/10")

    # Qualification Logic for the Green Badge
    if scores['Technical'] >= 5 and scores['Financial'] >= 10:
        st.success("🎯 STATUS: HIGH QUALITY LEAD")
        # Module 6: Structured Summary for Sales Handoff
        summary = (f"SOLAR LEAD REPORT\n"
                   f"------------------\n"
                   f"Technical Score: {scores['Technical']}/10\n"
                   f"Financial Score: {scores['Financial']}/20\n"
                   f"Intent Score: {scores['Intent']}/10\n"
                   f"Recommended Next Step: Schedule Site Visit")
        st.download_button("📥 Download Sales Handoff", data=summary, file_name="solar_lead_summary.txt")
    elif st.session_state.step > 0:
        st.warning("⚠️ STATUS: Qualifying...")


# 3. CONVERSATIONAL LOGIC (Modules 1-5)
def get_bot_response(user_input):
    ui = user_input.lower()

    # Step 0: Ownership (Risk Detection - Module 5)
    if st.session_state.step == 0:
        if any(word in ui for word in ["ja", "yes", "owner", "eigentümer"]):
            st.session_state.score_card.evaluate_technical("owner", "einfamilienhaus")
            return "Wunderbar. Handelt es sich um ein Einfamilienhaus? (Is it a single-family home?)"
        else:
            return "Leider können wir nur Eigentümern helfen. (Unfortunately we only help homeowners.)"

    # Step 1: Building Type (Technical Feasibility - Module 2)
    if st.session_state.step == 1:
        return "Eine PV-Anlage kostet meist 18.000€ - 25.000€. Ist das finanziell vorstellbar? (Budget fits?)"

    # Step 2: Financial Anchor (Financial Qualification - Module 3)
    if st.session_state.step == 2:
        if any(word in ui for word in ["ja", "yes", "passt"]):
            st.session_state.score_card.evaluate_financial(True)
        return "Planen Sie ein E-Auto oder eine Wärmepumpe? (Are you planning an EV or Heat Pump?)"

    # Step 3: Intent Detection (Upselling - Module 4)
    if st.session_state.step == 3:
        if any(word in ui for word in ["ja", "yes", "auto", "ev"]):
            # Boost intent score
            st.session_state.score_card.scores['Intent'] += 10
        return "Vielen Dank! Ein Experte wird Ihre Angaben prüfen. (An expert will review your data.)"

    return "Chat abgeschlossen. (Chat complete.)"


# 4. CHAT INTERFACE
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Trigger initial greeting
if not st.session_state.messages:
    greeting = "Willkommen! Gehört Ihnen die Immobilie, für die Sie planen? (Welcome! Do you own the property?)"
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.rerun()

# User Input Handling
if prompt := st.chat_input("Ihre Antwort..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and update
    response = get_bot_response(prompt)
    st.session_state.step += 1

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()