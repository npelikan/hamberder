from .TrumpTweet import TrumpTweet
from .twitter_api import api
from .config import TRUMP_TWITTER_ID

import tweepy


class TrumpStreamListener(tweepy.StreamListener):
    """
    An override of the tweepy StreamListener.on_status argument to instead repost Trump tweets
    """
    def on_status(self, status):
        new_tweet = TrumpTweet(status)
        new_tweet.grill_hamberders()


def trump_stream():
    streamObj = tweepy.Stream(auth=api.auth, listener=TrumpStreamListener, tweet_mode='extended')
    streamObj.filter(follow=[TRUMP_TWITTER_ID])