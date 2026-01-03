import streamlit as st
import json
import time
from google import genai
from fpdf import FPDF


# --- 1. SALES HANDOFF & PDF GENERATION (Scope 6) ---
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(255, 140, 0)  # Corporate Solar Orange
    pdf.cell(200, 15, "SOLAR-SALES HANDOVER PROTOCOL", ln=True, align='C')
    pdf.ln(10)

    # Lead Status
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    status = "QUALIFIED" if data['qualified'] else "REJECTED/PENDING"
    pdf.cell(200, 10, f"Lead Handoff Status: {status}", ln=True)
    pdf.ln(5)

    # Scoring Metrics (Scope 2 & 3)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(80, 10, "Qualification Metric", 1, 0, 'L', True)
    pdf.cell(40, 10, "Score (0-10)", 1, 1, 'C', True)

    pdf.set_font("Arial", size=11)
    pdf.cell(80, 10, "Technical Feasibility", 1)
    pdf.cell(40, 10, f"{data['technical_score']}/10", 1, 1, 'C')
    pdf.cell(80, 10, "Financial Readiness", 1)
    pdf.cell(40, 10, f"{data['financial_score']}/10", 1, 1, 'C')
    pdf.cell(80, 10, "Purchase Intent", 1)
    pdf.cell(40, 10, f"{data['intent_score']}/10", 1, 1, 'C')

    # Structured Summary (Scope 6)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Executive Sales Summary:", ln=True)
    pdf.set_font("Arial", size=11)
    summary_text = data.get('summary', 'No summary provided.').encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, summary_text)

    # Recommended Next Step
    pdf.ln(5)
    next_step = "Next Step: Schedule Sales Consultation" if data[
        'qualified'] else "Next Step: Automated Rejection / Lead Nurture"
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 10, next_step, ln=True)

    return pdf.output(dest='S').encode('latin-1')


# --- 2. MULTI-KEY & MULTI-MODEL ARCHITECTURE (Constraints) ---
st.set_page_config(page_title="SolarExpert Germany | Sales Filter", layout="wide")

# Setup Dual Clients for high availability
client_primary = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
client_backup = genai.Client(api_key=st.secrets["BACKUP_API_KEY"])

# Model hierarchy for failover
MODEL_POOL = ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-2.0-flash-exp"]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                  "content": "Willkommen bei SolarExpert Deutschland. Sind Sie der Eigentümer der Immobilie?"}]
if "scores" not in st.session_state:
    st.session_state.scores = {"technical_score": 0, "financial_score": 0, "intent_score": 0, "summary": "",
                               "qualified": False, "risk_flag": False}

# --- 3. SIDEBAR: THE SALES COCKPIT (Deliverable 1) ---
with st.sidebar:
    st.title("📊 Lead Dashboard")
    s = st.session_state.scores

    st.write(f"**Technik:** {s['technical_score']}/10")
    st.progress(s['technical_score'] / 10)
    st.write(f"**Finanzen:** {s['financial_score']}/10")
    st.progress(s['financial_score'] / 10)
    st.write(f"**Absicht:** {s['intent_score']}/10")
    st.progress(s['intent_score'] / 10)

    st.divider()

    # Risk Detection Alerts (Scope 5)
    if s.get("risk_flag"):
        st.error("❌ LEAD DISQUALIFIED: Risk detected (e.g. Renter or Unsuitable Building)")
    elif s.get("qualified"):
        st.success("✅ LEAD QUALIFIED: Escalating to Sales")
        pdf_bytes = create_pdf(s)
        st.download_button("📄 Download Sales Report (PDF)", data=pdf_bytes, file_name="Solar_Lead_Handoff.pdf")
    else:
        st.info("🕒 Qualification in Progress...")

# --- 4. CORE CHATBOT ENGINE (Scope 1 & 4) ---
st.title("Intelligent Solar Filter ☀️")
st.caption("Residential Rooftop Solar Qualification Bot - German Market Only")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ihre Antwort..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

        # This Master Instruction ensures we follow Scope 2, 3, 5, and 7
        master_instruction = f"""
        Identity: Solar Sales Bot for Germany.
        Language: Speak German (Tone: Trustworthy, professional).
        Rules: 
        1. DO NOT promise exact savings or subsidies (Compliance).
        2. Detect if user is a 'Mieter' (renter). If so, set risk_flag: true.
        3. Assess technical (roof, orientation) and financial (budget, Tesla/EV).
        4. Distinguish price-shoppers from genuine buyers.

        OUTPUT FORMAT:
        Reply: [German Response]
        JSON: {{"technical_score": int, "financial_score": int, "intent_score": int, "qualified": bool, "risk_flag": bool, "summary": "Detailed English summary for sales"}}

        CONTEXT:
        {history_str}
        """

        # HIERARCHICAL FAILOVER LOGIC
        final_response = None

        # Strategy: Loop through Primary Account first, then Backup Account
        clients = [client_primary, client_backup]
        for client in clients:
            if final_response: break
            for model in MODEL_POOL:
                try:
                    time.sleep(0.5)  # Prevent Rate-Limit Bursting
                    res = client.models.generate_content(model=model, contents=master_instruction)
                    if res.text:
                        final_response = res.text
                        break
                except Exception:
                    continue

        if final_response:
            try:
                if "JSON:" in final_response:
                    parts = final_response.split("JSON:")
                    chat_text = parts[0].replace("Reply:", "").strip()
                    json_data = json.loads(parts[1].strip())

                    st.session_state.scores.update(json_data)
                    st.session_state.messages.append({"role": "assistant", "content": chat_text})
                    st.markdown(chat_text)
                    st.rerun()
                else:
                    st.markdown(final_response)
            except Exception:
                st.markdown(final_res)
        else:
            st.error("⚠️ All API instances exhausted. Please wait 60 seconds.")