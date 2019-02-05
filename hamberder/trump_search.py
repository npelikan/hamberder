from .TrumpTweet import TrumpTweet
from .twitter_api import api
from .config import TRUMP_TWITTER_ID, ACCT_TWITTER_ID, bad_tweet
from .utils import remove_escapes

import time
import tweepy


class TrumpSearch:
    def __init__(self):
        # gets recent tweets
        all_recents = api.user_timeline(user_id=TRUMP_TWITTER_ID, tweet_mode='extended')
        all_recents.reverse()
        # gets
        recent_posts = [remove_escapes(x.full_text) for x in api.user_timeline(user_id=ACCT_TWITTER_ID,
                                                                               tweet_mode='extended')]
        for status in all_recents:
            trumptweet = TrumpTweet(status)
            trumptweet.strip_urls()
            if not bad_tweet(trumptweet.tweet_text):
                trumptweet.insert_hamberders()
                if trumptweet.substituted_text not in recent_posts:
                    trumptweet.post_tweet()
        self.maxtweetid = max(status.id for status in all_recents)

    def search_tweets(self):
        new_posts = api.user_timeline(
            user_id=TRUMP_TWITTER_ID,
            tweet_mode='extended',
            since_id=self.maxtweetid
        )
        for status in new_posts:
            trumptweet = TrumpTweet(status)
            trumptweet.serve_hamberders()
        if len(new_posts) > 0:
            self.maxtweetid = max(status.id for status in new_posts)


def trump_search():
    """
    Searches for trump tweets every 60 seconds. Makes jokes.
    """
    tweetsearch = TrumpSearch()
    try:
        while True:
            tweetsearch.search_tweets()
            time.sleep(60)
    except KeyboardInterrupt:
        print("manual break by user")
