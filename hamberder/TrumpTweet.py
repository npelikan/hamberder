import tweepy


class TrumpTweet:
    """
    Inits with a tweepy.Status object
    """
    def __init__(self, status):
        if type(status) is not tweepy.models.Status:
            raise TypeError("`status` argument must be an object of class tweepy.models.Status")

        self.orig_tweet = status

