from google.cloud import storage
from dotenv import load_dotenv

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

    return blob.download_as_string()

def upload_file(file_name, file_data):

    blob = bucket.blob(file_name)

    blob.upload_from_string(file_data)

    return blob

if __name__ == "__main__":

    list_contents()