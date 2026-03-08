from dotenv import load_dotenv
import os
import logging
import uuid

from typing import List, Dict, Optional
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

# Services
from services.profile_service import extract_profile
from services.eligibility_service import check_eligibility
from services.career_service import get_career_recommendations, generate_summary
from services.ai_advisor_service import generate_ai_advice

from services.translation_service import translate_to_english
from services.s3_service import upload_audio
from services.transcribe_service import start_transcription, get_transcription
from services.dynamodb_service import save_result


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PathWise AI Backend")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Models
# -------------------------

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5)


class SaveRequest(BaseModel):
    user_id: str
    summary: str
    profile: Dict
    eligibility: List[str]
    career_matches: List[Dict]


# -------------------------
# Basic Endpoints
# -------------------------

@app.get("/")
def home():
    return {"message": "PathWise backend running on AWS 🚀"}


@app.get("/health")
def health():
    return {"status": "API healthy"}


# -------------------------
# TEXT ANALYSIS
# -------------------------

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    text = request.text

    # translate to english
    translated_text = translate_to_english(text)

    profile_result = extract_profile(translated_text)
    profile = profile_result["profile"]
    warnings = profile_result.get("warnings", [])

    eligibility = check_eligibility(profile)

    career_matches = get_career_recommendations(profile, translated_text)

    summary = generate_summary(profile, career_matches)

    try:
        ai_advice = generate_ai_advice(profile, career_matches)
    except Exception as e:
        logger.warning(f"AI advisor unavailable: {e}")
        ai_advice = "AI advisor currently unavailable."
    return {
        "input_text": text,
        "translated_text": translated_text,
        "profile": profile,
        "warnings": warnings,
        "eligibility":eligibility,
        "career_matches": career_matches,
        "ai_summary": summary,
        "ai_advice": ai_advice
    }


# -------------------------
# VOICE ANALYSIS
# -------------------------

@app.post("/voice-analyze")
async def voice_analyze(audio: UploadFile = File(...)):

    # upload to S3
    s3_uri = upload_audio(audio)

    # start transcription
    job_name = start_transcription(s3_uri)

    transcript = get_transcription(job_name)

    translated_text = translate_to_english(transcript)

    profile_result = extract_profile(translated_text)
    profile = profile_result["profile"]

    eligibility = check_eligibility(profile)

    career_matches = get_career_recommendations(profile, translated_text)

    summary = generate_summary(profile, career_matches)

    try:
        ai_advice = generate_ai_advice(profile, career_matches)
    except Exception as e:
        logger.warning(f"AI advisor unavailable: {e}")
        ai_advice = "AI advisor currently unavailable."
    return {
        "transcript": transcript,
        "translated_text": translated_text,
        "profile": profile,
        "eligibility":eligibility,
        "career_matches": career_matches,
        "ai_summary": summary,
        "ai_advice": ai_advice
    }


# -------------------------
# SMART ENDPOINT
# -------------------------

@app.post("/advisor")
async def advisor(
    text: Optional[str] = None,
    audio: Optional[UploadFile] = File(None)
):

    if not text and not audio:
        return {"error": "Provide either text or audio"}

    if audio:
        s3_uri = upload_audio(audio)
        job_name = start_transcription(s3_uri)
        text = get_transcription(job_name)

    translated_text = translate_to_english(text)

    profile_result = extract_profile(translated_text)
    profile = profile_result["profile"]

    eligibility = check_eligibility(profile)

    career_matches = get_career_recommendations(profile, translated_text)

    summary = generate_summary(profile, career_matches)

    try:
        ai_advice = generate_ai_advice(profile, career_matches)
    except Exception as e:
        logger.warning(f"AI advisor unavailable: {e}")
        ai_advice = "AI advisor currently unavailable."
    return {
        "input": text,
        "translated_text": translated_text,
        "profile": profile,
        "eligibility":eligibility,
        "career_matches": career_matches,
        "ai_summary": summary,
        "ai_advice": ai_advice
    }


# -------------------------
# SAVE RESULTS
# -------------------------

@app.post("/save")
def save_data(data: SaveRequest):

    result = save_result(
        profile=data.profile,
        eligibility=data.eligibility,
        careers=data.career_matches,
        summary=data.summary
    )

    return {
        "message": "Saved successfully",
        "data": result
    }
