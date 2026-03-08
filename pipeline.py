from services.ai_advisor_service import generate_advice

def run_pipeline(user_id, text):

    advice = generate_advice(text)

    return {
        "user_id": user_id,
        "input_text": text,
        "advice": advice
    }
