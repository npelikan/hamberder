from spacy.tokens.token import Token


def define_replaceable(token):
    """
    Determines if a token should be considered replaceable.
    :param token: a spacy.tokens.Token
    :return: a boolean True or False
    """
    if type(token) is not Token:
        raise TypeError("input to define_replaceable must be an object of class spacy.tokens.token.Token")

    # only replace nouns. This also excludes pronoun replacements.
    if token.pos_ not in ["NOUN", "PROPN"]:
        return False
    # check for only subject/object
    elif token.dep_ not in ["pobj", "dobj", "nsubj"]:
        return False
    # excludes replacing people or organizations
    elif token.ent_type_ in ["GPE", "ORG", "PERSON"]:
        return False
    # otherwise, it's replaceable!
    else:
        return True
