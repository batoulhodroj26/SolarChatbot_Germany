☀️ SolarExpert Deutschland: Intelligent Sales & Qualification Bot
🚀 Business Context
This project provides a Conversational AI Filter for a German residential solar provider. It is designed to act as the first technical and commercial touchpoint for homeowners, ensuring that only high-quality, feasible leads reach the expensive sales engineering team.

🧠 Key Features & Scope (Assignment Alignment)
Scope 1: Dynamic Conversational Intelligence Uses a non-scripted, history-aware logic to adapt follow-up questions based on homeowner knowledge.

Scope 2 & 5: Technical Feasibility & Risk Detection Automatically identifies building types and roof characteristics while flagging risks like Renters (Mieter) or unsuitable structural properties.

Scope 3: Financial Qualification Distinguishes curiosity from genuine intent by analyzing budget expectations and urgency drivers (e.g., EV/Tesla adoption).

Scope 4: Trust & Compliance Operates in professional German, correcting misinformation without making unauthorized financial guarantees or subsidy promises.

Scope 6: Automated Sales Handoff Generates a structured PDF Lead Report including Technical, Financial, and Intent scores (0-10) for qualified leads.

🛠️ Technical Architecture
To meet the constraint of a "budget-conscious design," this bot utilizes the Google Gemini 3 Flash (Free Tier).

Resilience Engine: Dual-Account Failover
Due to strict identity-linked API quotas in 2026, I implemented a Hierarchical Failover Router:

Primary Account: Attempts to process requests through a model pool (Flash 1.5, Flash 8B, 2.0 Exp).

Backup Account: Automatically switches to a secondary API key if the primary account hits rate limits.

Graceful Throttling: If both instances are exhausted, the system informs the user via a managed cooldown message to prevent data loss.

🔧 Installation & Setup
Clone the Repo:

Bash

git clone https://github.com/your-username/SolarChatbot_Germany.git
Install Dependencies:

Bash

pip install -r requirements.txt
Configure Secrets: Create a folder .streamlit and a file secrets.toml:

Ini, TOML

GEMINI_API_KEY = "your_key_1"
BACKUP_API_KEY = "your_key_2"
Run Application:

Bash

streamlit run main.py
⚖️ Compliance & Ethics
GDPR: No PII is stored; data is processed in-memory during the session.

Ethics: Disclaimer included to ensure users understand the AI provides estimates, not binding offers.
Deliverable 3: Example Conversations (German)
The following transcripts demonstrate the chatbot's ability to assess technical feasibility, financial readiness, and risk factors in the German residential solar market.

Case A: The "Golden" Lead (Qualified Homeowner)
This example shows a high-intent, technically feasible homeowner in Berlin.

Bot: Willkommen bei SolarExpert Deutschland. Sind Sie der Eigentümer der Immobilie?

User: Ja, ich habe ein Einfamilienhaus in Berlin-Pankow.

Bot: Das klingt gut! Wie ist die Ausrichtung Ihres Dachs und haben Sie viel Schatten durch Bäume?

User: Mein Dach zeigt direkt nach Süden, keine Verschattung. Ich fahre auch einen Tesla und möchte eine Wallbox.

Bot: Perfekt. Für ein System mit Speicher und Wallbox liegt die Investition meist ab 20.000€. Passt das in Ihre Planung?

User: Ja, das Budget ist vorhanden. Wir wollen so schnell wie möglich starten.

Result: QUALIFIED. (Technical: 10/10, Financial: 10/10, Intent: 10/10). Sales Handoff Triggered.

Case B: The "Risk" Lead (Disqualified Renter)
This example shows the bot's risk detection (Scope 5) identifying a non-owner.

Bot: Willkommen bei SolarExpert Deutschland. Sind Sie der Eigentümer der Immobilie?

User: Nein, ich wohne zur Miete, aber ich möchte Solar auf meinem Balkon installieren.

Bot: Ich verstehe Ihr Interesse an grüner Energie! Da wir uns auf fest installierte Aufdachanlagen für Hauseigentümer spezialisieren, können wir Ihnen leider kein Angebot erstellen. Mieter benötigen für solche Anlagen meist die Zustimmung des Vermieters.

Result: DISQUALIFIED. (Risk Flag: True). Handoff Blocked.

Case C: The "Borderline" Case (Uncertain Feasibility)
This example shows the bot handling technical uncertainty and correcting misinformation (Scope 4).

Bot: Wie ist die Beschaffenheit Ihres Dachs?

User: Es ist ein altes Schieferdach mit einer Gaube nach Norden. Ich habe gehört, der Staat zahlt die Anlage komplett durch Subventionen.

Bot: Ein Schieferdach erfordert eine spezielle Prüfung durch unsere Techniker. Zur Info: Es gibt zwar Förderungen und Steuererleichterungen, aber eine "kostenlose" Anlage durch Subventionen gibt es aktuell nicht. Wäre ein Investment von ca. 15.000€ trotzdem denkbar?

User: Das müsste ich erst mit meiner Bank besprechen.

Result: IN PRÜFUNG. (Technical: 4/10, Intent: 5/10). Escalated for human technical review.
