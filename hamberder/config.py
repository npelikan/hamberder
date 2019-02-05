import re

TRUMP_TWITTER_ID = "25073877"
ACCT_TWITTER_ID = "1092174040247107584"


# defines hard non-replacement string rules
def keep_string(string):
    """
    Defines if strings should be kept
    :param string:
    :return: a boolean. True if string should be excluded from replacement
    """
    return any([
        re.search(r"(republican|democrat)s*", string, re.IGNORECASE) is not None,
    ])


# determines if replacement on a tweet would be in bad taste
def bad_tweet(string):
    """
    determines if replacement on a tweet would be in bad taste
    :param string:
    :return: a boolean. True if tweet should not be botted
    """
    return any([
        # leaving out racist stuff
        re.search(r"(african(-| )american|mexican|hispanic)", string, re.IGNORECASE) is not None
    ])
