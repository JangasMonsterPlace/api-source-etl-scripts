import os

from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET_NAME = "altair-janga"

GCS_PRIMARY_FOLDER_NAME = "data"

GCS_BACKUP_FOLDER_NAME = "backup"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

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
