from spacy.tokens import Token
from spacy.tokens import Span
import re


def define_replaceable(token):
    """
    Determines if a token should be considered replaceable.
    :param token: a spacy.tokens.Token
    :return: a boolean True or False
    """
    if type(token) is not Token:
        raise TypeError("input to define_replaceable must be an object of class spacy.tokens.Token")

    # only replace nouns. This also excludes pronoun replacements.
    if token.pos_ not in ["NOUN", "PROPN"]:
        return False
    # check for only subject/object
    elif token.dep_ not in ["pobj", "dobj", "nsubj", "iobj"]:
        return False
    # excludes replacing people or organizations
    elif token.ent_type_ in ["ORG", "PERSON"]:
        return False
    # otherwise, it's replaceable!
    else:
        return True


def replacement_rules(sentence):
    """
    Applies typical and bespoke replacement rules over sentences
    :param sentence: a spacy.tokens.Span
    :return: The string representation of sentence, with inserted replacements
    """
    if type(sentence) is not Span:
        raise TypeError("input to replacement_rules must be an object of class spacy.tokens.Span")

    # tests if stupid catchphrase and returns equally stupid thing if true
    bad_catchphrase = re.compile(r"build the wall (and|&) crime will fall", re.IGNORECASE)

    if re.search(bad_catchphrase, sentence.text):
        return re.sub(
            bad_catchphrase,
            "MORE BERDERS, LESS MURDERS",
            sentence.text
        )

    