import os
import json
import google.generativeai as genai

# --------------------------------------------------
# Configuration
# --------------------------------------------------

# IMPORTANT:
# Set this as an environment variable, DO NOT hardcode in production
# Windows (PowerShell):
#   setx GEMINI_API_KEY "your_api_key_here"
#
# macOS / Linux:
#   export GEMINI_API_KEY="your_api_key_here"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENABLED = bool(GEMINI_API_KEY)

if GEMINI_ENABLED:
    import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-1.5-flash"


# --------------------------------------------------
# Core intent interpretation function
# --------------------------------------------------

def interpret_intent(message: str) -> dict:
    if not GEMINI_ENABLED:
        return {
            "topics": [],
            "confidence": 0.0,
            "explanation": ""
        }

    """
    Uses Gemini to extract research/technical topics from a user idea.

    Always returns a dictionary with keys:
    - topics (list)
    - confidence (float)
    - explanation (str)
    """

    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are an intent classifier for a technology research discovery app.

Your task:
Given a user's idea, identify the TECHNICAL and RESEARCH domains involved.

These may include (but are not limited to):
- Machine Learning
- Artificial Intelligence
- Data Science
- Time Series Forecasting
- Computer Vision
- Natural Language Processing
- Systems
- Software Engineering
- Domain-specific sciences (e.g. meteorology, healthcare, finance)

Rules:
- If the idea involves building an app, system, or model, ALWAYS return at least 1–3 relevant topics.
- Be generous, not conservative.
- Do NOT return an empty list unless the message is clearly non-technical.

Respond ONLY in valid JSON in this format:
{{
  "topics": ["Machine Learning", "Data Science"],
  "confidence": 0.8,
  "explanation": "Short explanation of why these topics apply."
}}

User idea:
{message}
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        print("GEMINI RAW RESPONSE:\n", raw_text)

        # ---- Robust JSON extraction ----
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON object found in Gemini response")

        json_text = raw_text[start:end]
        parsed = json.loads(json_text)

        # ---- Final validation ----
        return {
            "topics": parsed.get("topics", []),
            "confidence": float(parsed.get("confidence", 0.0)),
            "explanation": parsed.get("explanation", "")
        }

    except Exception as e:
        print("Gemini intent parsing failed:", str(e))

        # Absolute-safe fallback (never crashes the app)
        return {
            "topics": [],
            "confidence": 0.0,
            "explanation": ""
        }
