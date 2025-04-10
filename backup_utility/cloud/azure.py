from azure.storage.blob import BlobServiceClient
import os

from ..logger import setup_logger

logger = setup_logger(__name__)

def upload_to_azure(config, file_path):
    try:
        azure_connection_string = config['cloud']['azure']['connection_string']
        container_name = config['cloud']['azure']['container_name']
        if not container_name:
            raise ValueError("Container name is required for Azure upload.")

        blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

        logger.info(f"File {file_path} uploaded to Azure container {container_name} successfully.")
    except Exception as e:
        logger.error(f"An error occurred while uploading to Azure: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Local file {file_path} removed after upload.")