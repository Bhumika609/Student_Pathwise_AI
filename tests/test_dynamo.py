import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")

tables = list(dynamodb.tables.all())

print("DynamoDB connected successfully")
