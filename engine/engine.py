import streamlit as st
import google.generativeai as genai


def get_chat_response(prompt):
    try:
        # 1. Setup
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)

        # 2. Model Scanner (This prevents the 404 error)
        # It finds exactly which model name your library supports
        working_model_name = "gemini-pro"  # Default
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    working_model_name = m.name
                    break
        except Exception as list_error:
            print(f"ListModels Error: {list_error}")

        # 3. Initialize the found model
        model = genai.GenerativeModel(working_model_name)

        # 4. Generate the response
        # We add a personality so it sounds like a professional consultant
        response = model.generate_content(
            f"Du bist ein Solar-Experte. Antworte auf Deutsch: {prompt}"
        )

        return response.text

    except Exception as e:
        # This will only show if your internet is down or the API key is blocked
        print(f"TERMINAL ERROR: {e}")
        return "Die KI-Verbindung wird stabilisiert. Bitte nennen Sie mir Ihr Budget."