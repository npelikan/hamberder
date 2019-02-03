from spacy.tokens import Token
from spacy.tokens import Span
import re
from .config import keep_string


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
    # excludes replacing people
    elif token.ent_type_ in ["PERSON", "NORP"]:
        return False
    elif keep_string(token.text):
        return False
    # otherwise, it's replaceable!
    else:
        return True


def wall_replacements(token):
    """
    Replaces build that wall with something far more delicious
    :param token: a spacy.tokens.Token
    :return: a replaced word
    """
    if type(token) is not Token:
        raise TypeError("input to define_replaceable must be an object of class spacy.tokens.Token")

    if token.lemma_ == "wall":
        replacement = "hamberders" + token.whitespace_

    elif token.lemma_ == "build":
        # handles tense
        if re.search(r"build", token.string, re.IGNORECASE):
            replacement = "grill" + token.whitespace_
        if re.search(r"built", token.string, re.IGNORECASE):
            replacement = "grilled" + token.whitespace_

    else:
        return token.string

    if token.is_upper:
        return replacement.upper()
    elif token.is_title:
        return replacement.title()
    else:
        return replacement


def replacement_rules(sentence):
    """
    Applies typical and bespoke replacement rules over sentences
    :param sentence: a spacy.tokens.Span
    :return: The string representation of sentence, with inserted replacements
    """
    if type(sentence) is not Span:
        raise TypeError("input to replacement_rules must be an object of class spacy.tokens.Span")

    # tests if stupid catchphrase and returns equally stupid thing if true
    # TODO: continue replacements if this is a final phrase, rather than a separate sentence
    bad_catchphrase = re.compile(r"build the wall (and|&) crime will fall", re.IGNORECASE)
    if re.search(bad_catchphrase, sentence.text):
        return re.sub(
            bad_catchphrase,
            "MORE HAMBERDERS, LESS MURDERS",
            sentence.text
        )

    # Fires if any mention of "wall". Let's grill up some hamberders!
    elif any([token.lemma_ == "wall" for token in sentence]):
        new_sentence = []
        for token in sentence:
            new_sentence.append(wall_replacements(token))
        return "".join(new_sentence)

    # if it's a stupid repetition, just replace every word with hamberders
    elif len(set([token.lemma_ for token in sentence if token.pos_ != "PUNCT"])) == 1:
        new_sentence = []
        for token in sentence:
            if token.pos_ == "PUNCT":
                new_sentence.append(token.string)
            else:
                new_sentence.append("HAMBERDERS" + token.whitespace_)
        return "".join(new_sentence)

    # nothing else worked, let's do some NLP replacements
    else:
        replaceable_tokens = [x for x in sentence if define_replaceable(x)]
        to_replace = replaceable_tokens[0]

        replacement = "hamberders" + to_replace.whitespace_
        if to_replace.is_upper:
            replacement = replacement.upper()
        elif to_replace.is_title:
            replacement = replacement.title()

        new_sentence = []
        for token in sentence:
            if token == to_replace:
                new_sentence.append(replacement)
            else:
                new_sentence.append(token.string)

        return "".join(new_sentence)