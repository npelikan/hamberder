import pytest
from hamberder.replacement_rules import define_replaceable, replacement_rules
import spacy

nlp = spacy.load('en_core_web_sm')


def test_raises_error():
    with pytest.raises(TypeError):
        define_replaceable("hi, mom!")


def test_replaces_stupid_catchphrase():
    no_ampersand = nlp("Build the wall and Crime will fall!")
    sent = list(no_ampersand.sents)[0]
    assert "MORE HAMBERDERS, LESS MURDERS!" == replacement_rules(sent)

    yes_ampersand = nlp("Build the wall & Crime will fall!")
    sent = list(yes_ampersand.sents)[0]
    assert "MORE HAMBERDERS, LESS MURDERS!" == replacement_rules(sent)


def test_wall_replacement():
    doc = nlp("Build the wall")
    sent = list(doc.sents)[0]
    assert "Grill the hamberders" == replacement_rules(sent)

    doc = nlp("I love walls")
    sent = list(doc.sents)[0]
    assert "I love hamberders" == replacement_rules(sent)


def test_replaces_noun_piles():
    sigh = nlp("JOBS, JOBS, JOBS!")
    sent = list(sigh.sents)[0]
    assert "HAMBERDERS, HAMBERDERS, HAMBERDERS!" == replacement_rules(sent)