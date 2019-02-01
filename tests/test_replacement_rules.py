import pytest
from hamberder.replacement_rules import define_replaceable


def test_raises_error():
    with pytest.raises(TypeError):
        define_replaceable("hi, mom!")
