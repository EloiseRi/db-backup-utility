from google.cloud import storage as gcs
import os

from ..logger import setup_logger

logger = setup_logger(__name__)

def upload_to_gcs(config, file_path, bucket_name):
    try:
        service_account_key = config['cloud']['gcs']['service_account_key']
        gcs_project = config['cloud']['gcs']['project_id']
        bucket_name = config['cloud']['gcs']['bucket_name']
        if not bucket_name:
            raise ValueError("Bucket name is required for GCS upload.")

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key

        client = gcs.Client(project=gcs_project)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(os.path.basename(file_path))

        blob.upload_from_filename(file_path)

        logger.info(f"File {file_path} uploaded to GCS bucket {bucket_name} successfully.")
    except Exception as e:
        logger.error(f"An error occurred while uploading to GCS: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Local file {file_path} removed after upload.")