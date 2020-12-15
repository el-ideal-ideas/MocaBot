# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Tuple, Callable, Union
)
from pathlib import Path
from tweepy import Cursor
from tweepy.cursor import ItemIterator
from tweepy import OAuthHandler, API
from ..moca_core import NEW_LINE, ENCODING

# -------------------------------------------------------------------------- Imports --

# -- MocaTwitter --------------------------------------------------------------------------


class MocaTwitter:
    """
    This class can get data from twitter use twitter API.

    Attributes
    ----------
    self._api
        a instance of twitter API class.
    """

    def __init__(
            self,
            consumer_key: str,
            consumer_secret: str,
            access_token: str,
            access_token_secret: str,
    ):
        """
        :param consumer_key: consumer key for twitter API.
        :param consumer_secret: consumer_secret for twitter API.
        :param access_token: access_token for twitter API.
        :param access_token_secret: access_token_secret for twitter API.
        """
        twitter_auth = OAuthHandler(consumer_key, consumer_secret)
        twitter_auth.set_access_token(access_token, access_token_secret)
        self._api = API(twitter_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def get_timeline(
            self,
            screen_name: str,
            since_id: Optional[int] = None,
            max_id: Optional[int] = None,
            count: Optional[int] = None,
            include_rts: bool = False,
            trim_user: bool = False,
            include_entities: bool = False,
            exclude_replies: bool = True
    ) -> ItemIterator:
        return Cursor(self._api.user_timeline,
                      screen_name=screen_name,
                      since_id=since_id,
                      max_id=max_id,
                      count=count,
                      include_rts=include_rts,
                      trim_user=trim_user,
                      include_entities=include_entities,
                      exclude_replies=exclude_replies).items()

    def get_user_icon_url(self, screen_name: str) -> Tuple[str, str, str, str]:
        url: str = self._api.get_user(screen_name).profile_image_url_https
        return url, url.replace('_normal', '_mini'), url.replace('_normal', '_bigger'), url.replace('_normal', '')

    def get_user_description(self, screen_name: str) -> str:
        return self._api.get_user(screen_name).description

    def get_user_info(self, screen_name: str) -> dict:
        return self._api.get_user(screen_name)._json

    def save_all_tweets_to_file(
            self,
            screen_name: str,
            filename: Union[Path, str],
            include_rts: bool = False,
            trim_user: bool = False,
            include_entities: bool = False,
            exclude_replies: bool = True,
            print_get_count: bool = True,
            get_per_once: int = 200,
            filter_func: Callable = lambda tweet: tweet
    ) -> int:
        get_count = 0
        with open(str(filename), mode='w', encoding=ENCODING) as file:
            tweets = self.get_timeline(
                screen_name, None, None, get_per_once, include_rts, trim_user, include_entities, exclude_replies
            )
            for tweet in tweets:
                get_count += 1
                file.write(filter_func(tweet.text))
                file.write(NEW_LINE)
            if print_get_count:
                print(f'Saved {get_count} tweets to {filename}.')
            return get_count

# -------------------------------------------------------------------------- MocaTwitter --
