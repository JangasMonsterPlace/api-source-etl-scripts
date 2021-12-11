from google.cloud import storage
from dotenv import load_dotenv

import json

load_dotenv()

storage_client = storage.Client()

BUCKET_NAME = "altair-janga"

bucket = storage_client.get_bucket(BUCKET_NAME)

def list_contents():

    blobs = list(bucket.list_blobs())

    for blob in blobs:

        print(blob.name)

    return blobs

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

def download_blob(bucket_name, source_blob_name, destination_file_name):
    
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    return blob

if __name__ == "__main__":

    list_contents()