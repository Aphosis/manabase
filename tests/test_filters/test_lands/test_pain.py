"""Test pain lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.pain import PainLandFilter


def test_pain_land_filter(make_card):
    filter_ = PainLandFilter()

    data = {
        "name": "Adarkar Wastes",
        "oracle_text": (
            "{T}: Add {C}.\n{T}: Add {W} or {U}. "
            "Adarkar Wastes deals 1 damage to you."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "oracle_text": (
            "{T}: Add {C}.\n{T}: Add {W} or {U}. "
            "Adarkar Wastes deals 1 damage to you."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
