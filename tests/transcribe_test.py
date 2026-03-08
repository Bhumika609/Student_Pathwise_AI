import boto3

transcribe = boto3.client('transcribe', region_name='ap-south-1')

job_name = "career-test-job"

job_uri = "s3://career-audio-bucket-asmitha/test_audio.mp3"

response = transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='te-IN'
)

print("Transcription job started")
