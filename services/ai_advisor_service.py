import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_ai_advice(profile, career_matches):

    if not career_matches:
        return "No career advice available."

    top_career = career_matches[0]["career"]

    prompt = f"""
Student Profile:
{profile}

Recommended Career:
{top_career}

Give short practical career advice.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return "AI advisor temporarily unavailable."
