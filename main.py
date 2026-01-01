import streamlit as st
from google import genai
from fpdf import FPDF
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Solar Expert Germany 2026", page_icon="☀️")

# Initialize Session State
for key in ["chat_history", "balloons_shown", "tech_score", "fin_score", "intent_score"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "history" in key else 0 if "score" in key else False

# NEW 2026 API Client Setup
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("Missing GEMINI_API_KEY in Secrets!")

# --- 2. SIDEBAR ---
st.sidebar.header("Lead Qualifizierung")
st.sidebar.progress(st.session_state.tech_score * 10, text=f"Technik: {st.session_state.tech_score}/10")
st.sidebar.progress(st.session_state.fin_score * 10, text=f"Budget: {st.session_state.fin_score}/10")
st.sidebar.progress(st.session_state.intent_score * 10, text=f"Interesse: {st.session_state.intent_score}/10")

# --- 3. MAIN UI ---
st.title("☀️ Ihr Solar-Experte")
st.info("Willkommen! Ich helfe Ihnen bei der Planung Ihrer PV-Anlage.")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT INPUT & NEW 2026 AI LOGIC ---
if prompt := st.chat_input("Schreiben Sie hier..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Scoring Logic
    p_lower = prompt.lower()
    if any(k in p_lower for k in ["hauseigentümer", "besitzer", "eigentum", "haus"]):
        st.session_state.tech_score = 10
    if any(k in p_lower for k in ["euro", "€", "budget", "sparen", "kosten"]):
        st.session_state.fin_score = 10
    if any(k in p_lower for k in ["tesla", "laden", "wallbox", "batterie"]):
        st.session_state.intent_score = 10

    # AI Response using Gemini 3 Flash (Fastest & Most Reliable in 2026)
    with st.chat_message("assistant"):
        try:
            # We target 'gemini-3-flash' as it is the current workhorse
            response = client.models.generate_content(
                model="gemini-3-flash",
                contents=f"Du bist ein Solar-Experte in Deutschland. Antworte hilfreich auf Deutsch: {prompt}"
            )
            full_response = response.text
        except Exception as e:
            # Fallback to 2.5 if 3 is not yet in your region
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                full_response = response.text
            except:
                full_response = f"⚠️ Verbindungsfehler: {str(e)}"

        st.markdown(full_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    st.rerun()

# --- 5. QUALIFICATION & PDF ---
if st.session_state.tech_score >= 10 and st.session_state.fin_score >= 10:
    if not st.session_state.balloons_shown:
        st.balloons()
        st.success("🎉 Glückwunsch! Sie sind als Premium-Kunde qualifiziert.")
        st.session_state.balloons_shown = True


    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Solar-Qualifizierungsbericht", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Erstellt am: {datetime.date.today()}", ln=True)
        pdf.multi_cell(0, 10, "Basierend auf unserem Gespräch sind Sie ein idealer Kandidat für eine Solaranlage.")
        return pdf.output(dest='S').encode('latin-1')


    st.download_button(
        label="📥 PDF-Bericht herunterladen",
        data=create_pdf(),
        file_name="Solar_Expert_Report.pdf",
        mime="application/pdf"
    )