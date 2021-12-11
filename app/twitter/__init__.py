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
        print(data)
        # ORM.insert_transformed_review_data(data)


def runner(until: str = "0-0-0", since: str = "0-0-0", hashtag: str = "python", date_range: bool = False, replies: bool = True ) -> None:
    twitter_runner = _TwitterRunner()
    query = f"{hashtag} -filter:retweets lang:en"
    if date_range:
        query += f" since:{since} until:{until}"
    if replies:
        query += " -filter:replies"
    print(query)
    twitter_runner.etl(query)
    # twitter_runner.etl(f"{hashtag}  -filter:replies until:{until} since:{since} -filter:retweets lang:en")

