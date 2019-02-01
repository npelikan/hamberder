from .config import bad_tweet
from .twitter_api import api
from .replacement_rules import replacement_rules

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

    def _strip_urls(self):
        """
        Strips URLs so they don't mess with NLP
        :return:
        """
        raw_text = self.orig_tweet.text
        link_match = re.search(hyperlink_regexp, raw_text)
        if link_match:
            self.tweet_url = link_match.group(0)
            self.tweet_text = raw_text[:link_match.start(0)] + raw_text[link_match.end(0):]
        else:
            self.tweet_text = raw_text

    def _insert_hamberders(self):
        """
        Substitutes hamberders in good places.
        """
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.tweet_text)
        with_subs = []
        for sent in doc.sents:
            with_subs.append(replacement_rules(sent))
        self.substituted_text = " ".join(with_subs)

    def grill_hamberders(self):
        """
        Posts the tweet!
        """
        self._strip_urls()
        if not bad_tweet(self.tweet_text):
            self._insert_hamberders()

            to_post = self.substituted_text

            if self.tweet_url:
                to_post = " ".join([to_post, self.tweet_url])

            api.update_status(to_post)
