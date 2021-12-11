import os

from dotenv import load_dotenv

load_dotenv()


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
