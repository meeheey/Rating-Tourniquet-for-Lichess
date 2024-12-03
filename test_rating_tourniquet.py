import pytest

import lichess.api
from lichess.format import PYCHESS

from project import validate_username, get_color, timestamp_to_datetime


def test_validate_username():
    with pytest.raises(ValueError):
        validate_username("%p", "blitz")

def test_get_color():
    game = lichess.api.game('iaMVD4iR')
    assert get_color(game, "thibault") == "white"

def test_timestamp_to_datetime():
    assert timestamp_to_datetime(1727342725066) == 11
