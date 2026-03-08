import boto3

# connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

table = dynamodb.Table('career_advisory')

# insert test data
response = table.put_item(
    Item={
        'user_id': '1',
        'timestamp': '001',
        'text': 'Hello World'
    }
)

print("Data inserted successfully")
