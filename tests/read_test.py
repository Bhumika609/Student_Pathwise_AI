import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('career_advisory')

response = table.get_item(
    Key={
        'user_id': '1',
        'timestamp': '001'
    }
)

print(response['Item'])
