from services.s3_service import upload_audio
from services.transcribe_service import start_transcription
from services.translation_service import translate_text
from services.profile_service import extract_profile
from services.eligibility_service import check_eligibility
from services.career_service import get_career_recommendations, generate_summary
from services.ai_advisor_service import generate_ai_advice
from services.dynamodb_service import save_result


def run_pipeline(user_id, audio_file):

    # upload audio
    s3_url = upload_audio(audio_file)

    # start transcription
    job_name = start_transcription(s3_url)

    # NOTE: in real system we would poll transcription result
    transcript = "Transcription processing..."

    english_text = translate_text(transcript)

    profile_result = extract_profile(english_text)
    profile = profile_result["profile"]

    eligibility = check_eligibility(profile)

    careers = get_career_recommendations(profile, english_text)

    summary = generate_summary(profile, careers)

    advice = generate_ai_advice(profile, careers)

    result = {
        "user_id": user_id,
        "transcript": transcript,
        "translated_text": english_text,
        "profile": profile,
        "eligibility": eligibility,
        "career_matches": careers,
        "ai_summary": summary,
        "ai_advice": advice
    }

    save_result(profile, eligibility, careers, summary)

    return result
