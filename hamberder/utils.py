import re


def remove_escapes(value):
    value = value.encode('utf-8').decode('unicode_escape')
    value = re.sub(r"\&amp;", "&", value)
    return value
