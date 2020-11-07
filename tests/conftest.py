"""Test utilities."""
import pytest


@pytest.fixture(scope="session")
def make_card():
    """Create a card with default values.

    Specify any field to override by keyword argument.
    """

    from manabase.cards import Card  # pylint: disable=import-outside-toplevel

    def inner(**data):
        default = {
            "name": "",
            "oracle_text": "",
            "colors": [],
            "color_identity": [],
            "produced_mana": [],
            "legalities": {},
            "textless": False,
            "scryfall_uri": "",
        }
        default.update(data)
        return Card(**default)

    return inner
