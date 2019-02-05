from .config import bad_tweet
from .twitter_api import api
from .replacement_rules import replacement_rules
from .utils import remove_escapes

import tweepy
import re
import spacy

hyperlink_regexp = re.compile(
    r"\b(?:https?|telnet|gopher|file|wais|ftp):[\w/#~:.?+=&%@!\-.:?\\-]+?(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))"
)


class TrumpTweet:
    """
    Inits with a tweepy.Status object
    """
    def __init__(self, status):
        if type(status) is not tweepy.models.Status:
            raise TypeError("`status` argument must be an object of class tweepy.models.Status")
        self.orig_tweet = status
        self.tweet_text = None
        self.tweet_url = None
        self.substituted_text = None

    def strip_urls(self):
        """
        Strips URLs so they don't mess with NLP
        :return:
        """
        raw_text = remove_escapes(self.orig_tweet.full_text)
        link_match = re.search(hyperlink_regexp, raw_text)
        if link_match:
            self.tweet_url = link_match.group(0)
            self.tweet_text = raw_text[:link_match.start(0)] + raw_text[link_match.end(0):]
        else:
            self.tweet_text = raw_text

    def insert_hamberders(self):
        """
        Substitutes hamberders in good places.
        """
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.tweet_text)
        with_subs = []
        for sent in doc.sents:
            with_subs.append(replacement_rules(sent))
        # trims if > 280
        self.substituted_text = " ".join(with_subs)[:280]

    def post_tweet(self):
        to_post = self.substituted_text

        if self.tweet_url:
            to_post = " ".join([to_post, self.tweet_url])

        api.update_status(to_post)

    def serve_hamberders(self):
        """
        Posts the tweet! Likely most useful from a stream
        """
        self.strip_urls()
        if not bad_tweet(self.tweet_text):
            self.insert_hamberders()
            self.post_tweet()
