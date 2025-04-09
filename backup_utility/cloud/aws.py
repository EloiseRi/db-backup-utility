import boto3
import os

from ..logger import setup_logger

logger = setup_logger(__name__)

def upload_to_s3(config, file_path):
    try:
        aws_access_key = config['cloud']['aws']['access_key']
        aws_secret_key = config['cloud']['aws']['secret_key']
        region_name = config['cloud']['aws']['region']
        bucket_name = config['cloud']['aws']['bucket_name']
        if not bucket_name:
            raise ValueError("Bucket name is required for S3 upload.")

        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        s3_client = session.client('s3')
        s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))

        logger.info(f"File {file_path} uploaded to S3 bucket {bucket_name} successfully.")
    except Exception as e:
        logger.error(f"An error occurred while uploading to S3: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Local file {file_path} removed after upload.")