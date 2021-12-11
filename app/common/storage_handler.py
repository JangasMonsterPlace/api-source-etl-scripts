from google.cloud import storage
from dotenv import load_dotenv
from .settings import GCS_BUCKET_NAME as BUCKET_NAME

import json

load_dotenv()

storage_client = storage.Client()

bucket = storage_client.get_bucket(BUCKET_NAME)

def list_contents(prefix = ""):

    blob_name_list = []

    blobs = list(bucket.list_blobs(prefix=prefix))

    for blob in blobs:

        blob_name_list.append(blob.name)

    return blob_name_list

def read_file(file_name):

    blob = bucket.blob(file_name)

    return blob.download_as_string() # Returns a byte encoded string

def upload_file(file_name, file_data):

    blob = bucket.blob(file_name)

    blob.upload_from_string(file_data)

    return blob

def create_bucket(bucket_name):

    bucket = storage_client.create_bucket(bucket_name)

    return bucket

def delete_bucket(bucket_name):
    
    bucket = storage_client.get_bucket(bucket_name)

    bucket.delete()

    return bucket

def download_blob(source_blob_name, destination_file_name):
    
    bucket = storage_client.get_bucket(BUCKET_NAME)

    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    return blob

if __name__ == "__main__":

    list_contents()