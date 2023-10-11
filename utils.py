import boto3


BUCKET_NAME = "r33anotherbnb"
AWS_REGION = "us-west-1"
BUCKET_IMG_BASE_URL = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"


s3 = boto3.resource('s3')



def uploadToS3(file, filename):
    """Upload file to AWS S3 bucket."""

    s3.Bucket(BUCKET_NAME).upload_fileobj(file, filename)








# s3_client = boto3.client(
#     's3',
#     aws_access_key_id = ,
#     aws_secret_access_key
# )

# Upload a new file
# with open('temp_testimage.jpg', 'rb') as data:
#     s3.Bucket(f"{BUCKET_NAME}").put_object(Key='temp_testimage', Body=data)

