"""Test cycling lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.cycling import CyclingLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = CyclingLandFilter()

    data = {
        "name": "Irrigated Farmland",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Irrigated Farmland enters the battlefield tapped.\n"
            "Cycling {2} ({2}, Discard this card: Draw a card.)"
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Irrigated Farmland",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Irrigated Farmland enters the battlefield tapped.\n"
            "Cycling {2} ({2}, Discard this card: Draw a card.)"
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
