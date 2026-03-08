import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "career-audio-bucket-asmitha"

def upload_audio(file):

    file_name = file.filename

    s3.upload_fileobj(
        file.file,
        BUCKET_NAME,
        file_name
    )

    return f"s3://{BUCKET_NAME}/{file_name}"
