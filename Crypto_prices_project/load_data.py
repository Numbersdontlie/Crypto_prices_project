import boto3 
import os
from dotenv import load_dotenv
import glob

# Point to .env file
load_dotenv('../.env')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key_id = os.getenv('AWS_SECRET_KEY_ID')

# Creating session with boto3 
session = boto3.Session(
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_key_id=aws_secret_key_id
                    )

# Creating S3 resource from the Session
s3 = session.resource('s3')

# Upload files to crypto-price-project bucket 
path = "../raw_data/*.csv"
for file in glob.glob(path):
    s3.Bucket('crypto-price-project'.upload_file(file))
