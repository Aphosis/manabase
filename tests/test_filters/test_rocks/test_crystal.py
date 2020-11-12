"""Test crystals filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.crystal import CrystalFilter


def test_filter(make_card):
    filter_ = CrystalFilter()

    data = {
        "name": "Indatha Crystal",
        "oracle_text": (
            "{T}: Add {W}, {B}, or {G}.\n"
            "Cycling {2} ({2}, Discard this card: Draw a card.)"
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Indatha Crystal",
        "oracle_text": (
            "{T}: Add {W}, {B}, or {G}.\n"
            "Cycling {2} ({2}, Discard this card: Draw a card.)"
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
