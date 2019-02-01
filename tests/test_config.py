from hamberder.config import keep_string


def keep_string_positive_test():
    assert keep_string("Democrats")


def keep_string_negative_test():
    assert not keep_string("Germans")