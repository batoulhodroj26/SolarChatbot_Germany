import streamlit as st
from datetime import datetime
from engine.engine import get_chat_response
from engine.scoring import LeadScoreCard

st.set_page_config(page_title="Solar Lead Pro", layout="wide")

# --- SESSION STATE (The Bot's Memory) ---
if "tracker" not in st.session_state:
    st.session_state.tracker = LeadScoreCard()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_saved" not in st.session_state:
    st.session_state.lead_saved = False


def save_lead_to_file(scores):
    """Saves the lead data locally for Omar to see"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- NEW LEAD: {timestamp} ---\n")
        f.write(f"Tech: {scores['Technical']}/10 | Finance: {scores['Financial']}/10 | Intent: {scores['Intent']}/10\n")
        f.write("-" * 40 + "\n")


# --- SIDEBAR (The Progress Bars) ---
st.sidebar.title("Lead Qualifizierung")
for cat, score in st.session_state.tracker.scores.items():
    st.sidebar.write(f"**{cat}**")
    st.sidebar.progress(score * 10)
    st.sidebar.caption(f"Status: {score}/10")

# --- CHAT INTERFACE ---
st.title("☀️ Solar KI-Assistent")

# NEW: Welcome Logic - If no messages, the bot starts
if not st.session_state.messages:
    welcome = "Hallo! Ich bin Ihr Solar-Experte. Gehört Ihnen die Immobilie, für die Sie Solar planen?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Check if user reached 30/30 score
total_score = sum(st.session_state.tracker.scores.values())

if total_score >= 30:
    st.balloons()
    st.success("🎉 Glückwunsch! Sie sind voll qualifiziert. Wir haben Ihre Daten gespeichert.")
    if not st.session_state.lead_saved:
        save_lead_to_file(st.session_state.tracker.scores)
        st.session_state.lead_saved = True
    st.button("PDF Angebot herunterladen")
else:
    # User Input Field
    if prompt := st.chat_input("Ihre Antwort..."):
        # 1. Update the scoring bars
        st.session_state.tracker.evaluate_all(prompt)

        # 2. Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 3. Get AI Response
        with st.chat_message("assistant"):
            answer = get_chat_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        # Refresh to show new messages and updated bars
        st.rerun()