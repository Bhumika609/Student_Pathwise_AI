import boto3
import requests
import json

transcribe = boto3.client('transcribe', region_name='ap-south-1')

job_name = "career-test-job"

# get job info
response = transcribe.get_transcription_job(
    TranscriptionJobName=job_name
)

status = response['TranscriptionJob']['TranscriptionJobStatus']

print("Job Status:", status)

if status == "COMPLETED":

    transcript_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']

    result = requests.get(transcript_url).json()

    text = result['results']['transcripts'][0]['transcript']

    print("Transcript Text:", text)

else:
    print("Job not finished yet")
