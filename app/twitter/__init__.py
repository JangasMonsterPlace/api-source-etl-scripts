import logging
import tweepy
from typing import Generator, Optional
from common import settings, ORM
from common.domain_types import TransformedTextData
from tweepy.models import Status

logger = logging.getLogger(__name__)


class _TwitterRunner:
    def __init__(
            self,
            hashtag: Optional[str] = None,
            *,
            until: Optional[str] = None,
            since: Optional[str] = None,
            replies: bool = False
    ):
        auth = tweepy.OAuthHandler(**settings.TWITTER["oauth_handler"])
        auth.set_access_token(**settings.TWITTER["access_token"])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        self.from_date = since
        self.to_date = until
        self.hashtag = hashtag
        self.replies = replies

    @staticmethod
    def _tweet_is_valid(tweet: Status) -> bool:
        if len(tweet.entities["hashtags"]) > 5:
            return False
        return True

    def _get_query(self) -> str:
        query = f"#{self.hashtag} -filter:retweets lang:en"
        if self.from_date and self.to_date:
            query += f" since:{self.from_date} until:{self.to_date}"
        if self.replies:
            query += " -filter:replies"
        return query

    def extract_tweets(self) -> Generator[Status, None, None]:
        for tweet in self.api.search_tweets(q=self._get_query(), tweet_mode="extended", count=100):
            if not self._tweet_is_valid(tweet):
                continue
            yield tweet

    def extract_and_transform_tweets(self) -> Generator[TransformedTextData, None, None]:
        for tweet in self.extract_tweets():
            yield TransformedTextData(
                source_id=tweet.id,
                source="twitter",
                text=tweet.full_text,
                author=tweet.author.screen_name.lower(),
                written_by_user_at=tweet.created_at,
                use_case=f"#{self.hashtag}"
            )

    def etl(self):
        data = [
            tuple(tweet.__dict__.values())
            for tweet in self.extract_and_transform_tweets()
        ]
        ORM.insert_transformed_review_data(data)


def runner() -> None:
    # Example for Values:
    # https://github.com/JangasMonsterPlace/api-source-etl-scripts/blob/9bb29776d8c114b6009a0e1c1e5176d1b11470d2/app/twitter/__init__.py#L49
    twitter_runner = _TwitterRunner(hashtag="python")
    twitter_runner.etl()

