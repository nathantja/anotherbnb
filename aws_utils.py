import boto3

BUCKET_NAME = "r33anotherbnb"
AWS_REGION = "us-west-1"






s3 = boto3.resource('s3')

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id = ,
#     aws_secret_access_key
# )

# Upload a new file
with open('test.jpg', 'rb') as data:
    s3.Bucket(f"{BUCKET_NAME}").put_object(Key='test.jpg', Body=data)

