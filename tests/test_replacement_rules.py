import pytest
from hamberder.replacement_rules import define_replaceable, replacement_rules
import spacy


def test_raises_error():
    with pytest.raises(TypeError):
        define_replaceable("hi, mom!")


def test_replaces_stupid_catchphrase():
    nlp = spacy.load('en_core_web_sm')
    no_ampersand = nlp("Build the wall and Crime will fall!")
    sent = list(no_ampersand.sents)[0]
    assert "MORE BERDERS, LESS MURDERS!" == replacement_rules(sent)

    yes_ampersand = nlp("Build the wall & Crime will fall!")
    sent = list(yes_ampersand.sents)[0]
    assert "MORE BERDERS, LESS MURDERS!" == replacement_rules(sent)
