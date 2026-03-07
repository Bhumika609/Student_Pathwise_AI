import boto3
import time
import requests
transcribe = boto3.client(
    "transcribe",
    region_name="ap-south-1"
)


def start_transcription(file_uri):

    job_name = f"job-{int(time.time())}"

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        IdentifyLanguage=True,
        LanguageOptions=[
           "te-IN",
           "hi-IN",
           "ta-IN",
           "kn-IN",
           "en-IN",
           "ml-IN"
        ]
    )
    return job_name


def get_transcription(job_name):

    while True:

        status = transcribe.get_transcription_job(
            TranscriptionJobName=job_name
        )

        job_status = status["TranscriptionJob"]["TranscriptionJobStatus"]

        print("TRANSCRIBE STATUS:", job_status)

        if job_status in ["COMPLETED", "FAILED"]:
            break

        time.sleep(3)

    if job_status == "COMPLETED":

        transcript_url = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

        response = requests.get(transcript_url)
        data = response.json()

        return data["results"]["transcripts"][0]["transcript"]

    else:

        print(status)

        raise Exception("Transcription failed")
