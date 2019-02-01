import re


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