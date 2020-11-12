"""Test obelisks filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.obelisk import ObeliskFilter


def test_filter(make_card):
    filter_ = ObeliskFilter()

    data = {
        "name": "Obelisk of Bant",
        "oracle_text": "{T}: Add {G}, {W}, or {U}.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Obelisk of Bant",
        "oracle_text": "{T}: Add {G}, {W}, or {U}.Some text.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
