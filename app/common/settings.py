import os
import uuid

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

GCP_STORAGE = {
    "credentials_file_path": os.path.join(BASE_DIR, ".google-service-account-file.json"),
    "primary_folder_name": os.getenv("PRIMARY_FOLDER_NAME"),
    "backup_folder_name": os.getenv("BACKUP_FOLDER_NAME"),
    "bucket_name": os.getenv("BUCKET_NAME")
}

TWITTER = {
    "oauth_handler": {
        "consumer_key": os.getenv("TWITTER_API_KEY"),
        "consumer_secret": os.getenv("TWITTER_API_KEY_SECRET")
    },
    "access_token": {
        "key": os.getenv("TWITTER_ACCESS_TOKEN"),
        "secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    }
}

POSTGRES = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME")
}


CONFLUENT_KAFKA = {
    "bootstrap.servers": os.getenv("KAFKA_CLUSTER_SERVER"),
    "group.id": f"ngrams-{uuid.uuid4().hex[:6]}",
    'auto.offset.reset': 'latest',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_CLUSTER_API_KEY"),
    'sasl.password': os.getenv("KAFKA_CLUSTER_API_SECRET")
}