import logging
import tweepy
from typing import Generator
from common import settings, ORM
from common.domain_types import TransformedTextData
from tweepy.models import Status

logger = logging.getLogger(__name__)


class _TwitterRunner:
    def __init__(self):
        auth = tweepy.OAuthHandler(**settings.TWITTER["oauth_handler"])
        auth.set_access_token(**settings.TWITTER["access_token"])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    @staticmethod
    def _tweet_is_valid(tweet: Status) -> bool:
        if tweet.full_text.startswith("RT"):
            # Replace tweet with original
            # tweet.full_text = tweet.retweeted_status.full_text

            # continue - no retweets wanted
            return False
        if len(tweet.entities["hashtags"]) > 5:
            return False
        return True

    def extract_tweets(self, hashtag: str) -> Generator[Status, None, None]:
        for tweet in self.api.search_tweets(q=f"#{hashtag}", tweet_mode="extended", count=100):
            if not self._tweet_is_valid(tweet):
                continue
            yield tweet

    def extract_and_transform_tweets(self, hashtag: str) -> Generator[TransformedTextData, None, None]:
        for tweet in self.extract_tweets(hashtag):
            yield TransformedTextData(
                id=tweet.id,
                source="twitter",
                text=tweet.full_text,
                user=tweet.author.screen_name.lower(),
                written_by_user_at=tweet.created_at,
                use_case=f"#{hashtag}"
            )

    def etl(self, hashtag: str):
        data = [
            tuple(tweet.__dict__.values())
            for tweet in self.extract_and_transform_tweets(hashtag)
        ]
        ORM.insert_transformed_review_data(data)


def runner():
    twitter_runner = _TwitterRunner()
    twitter_runner.etl("python")
