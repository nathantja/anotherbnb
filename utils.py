import boto3


BUCKET_NAME = "r33anotherbnb"
AWS_REGION = "us-west-1"
BUCKET_IMG_BASE_URL = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

s3 = boto3.resource('s3')



def upload_to_S3(file, filename):
    """Upload file to AWS S3 bucket."""

    s3.Bucket(BUCKET_NAME).upload_fileobj(file, filename)


def validate_image_extensions(images):
    """Given a list of image files, return True if extensions are in the allowed
    set. Otherwise return False."""

    for image in images:
        extension = image.filename.rsplit(".", 1)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            return False

    return True
