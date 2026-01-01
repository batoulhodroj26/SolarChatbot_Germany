import os
from datetime import datetime  # Added for time-stamping leads
from dotenv import load_dotenv
from openai import OpenAI
from engine.scoring import LeadScoreCard

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_feedback(user_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a German solar expert. Give a 1-sentence professional reply."},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Vielen Dank für die Details."


def save_lead_report(scores, roof_details):
    """Saves the lead data to a text file for the sales team."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- NEW LEAD CAPTURED: {timestamp} ---\n")
        f.write(f"Technical Score: {scores['Technical']}/10\n")
        f.write(f"Financial Score: {scores['Financial']}/10\n")
        f.write(f"Roof Description: {roof_details}\n")
        f.write("Status: HIGH PRIORITY - Ready for Handoff\n")
        f.write("-" * 40 + "\n")
    print("\n[System]: Lead data has been saved to leads.txt")


def run_solar_bot():
    score_card = LeadScoreCard()
    print("--- Solar Chatbot Germany ---")
    print("Disclaimer: Schätzungen sind unverbindlich.\n")

    owner = input("Bot: Sind Sie der Eigentümer der Immobilie? (Ja/Nein): ").lower()
    if "ja" not in owner:
        print("Bot: Wir fokussieren uns auf Eigentümer. Danke!")
        return

    house = input("Bot: Ist es ein Einfamilienhaus? (Ja/Nein): ").lower()
    b_type = "einfamilienhaus" if "ja" in house else "other"
    score_card.evaluate_technical("owner", b_type)

    roof = input("Bot: Beschreiben Sie kurz Ihr Dach: ")
    print(f"Bot: {get_ai_feedback(roof)}")

    print("\nBot: Eine Anlage kostet meist 18.000€ - 25.000€.")
    budget = input("Bot: Passt das in Ihre Vorstellung? (Ja/Nein): ").lower()
    score_card.evaluate_financial("ja" in budget)

    # OUTPUT AND SAVING
    print("\n--- QUALIFICATION SUMMARY ---")
    for category, score in score_card.scores.items():
        print(f"{category} Score: {score}/10")

    if score_card.scores["Technical"] >= 5 and score_card.scores["Financial"] >= 10:
        print("Result: HIGH QUALITY LEAD - Transfer to Sales Team.")
        # Trigger the save function
        save_lead_report(score_card.scores, roof)
    else:
        print("Result: LOW PRIORITY - Send info material.")


if __name__ == "__main__":
    run_solar_bot()