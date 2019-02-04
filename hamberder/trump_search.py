from .TrumpTweet import TrumpTweet
from .twitter_api import api
from .config import TRUMP_TWITTER_ID

import sched
import time
import tweepy


def trump_search():
    """
    Searches for trump tweets every 60 seconds. Makes jokes.
    """
    s = sched.scheduler(time.time, time.sleep)
    