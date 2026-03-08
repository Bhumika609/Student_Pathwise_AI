import boto3
import json

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "amazon.nova-lite-v1:0"

prompt = "Reply with only the word SUCCESS."

body = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 50,
    "temperature": 0
}

try:
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())
    print("Model Response:")
    print(response_body["output"]["message"]["content"][0]["text"])

except Exception as e:
    print("ERROR:", e)
