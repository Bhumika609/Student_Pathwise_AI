import boto3

translate = boto3.client("translate", region_name="ap-south-1")

def translate_to_english(text):

    result = translate.translate_text(
        Text=text,
        SourceLanguageCode="auto",
        TargetLanguageCode="en"
    )

    return result["TranslatedText"]
