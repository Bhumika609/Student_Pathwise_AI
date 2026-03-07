import boto3

translate = boto3.client('translate', region_name='ap-south-1')

text = "నాకు కంప్యూటర్ సైన్స్ ఇష్టం"

response = translate.translate_text(
    Text=text,
    SourceLanguageCode='auto',
    TargetLanguageCode='en'
)

print("Original:", text)
print("Translated:", response['TranslatedText'])
