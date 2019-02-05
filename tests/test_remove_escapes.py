from hamberder.utils import remove_escapes


def test_ampersand_escapes():
    assert "Ben & Jerry's" == remove_escapes("Ben &amp; Jerry's")
