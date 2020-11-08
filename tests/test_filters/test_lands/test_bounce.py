"""Test bounce lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.bounce import BounceLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = BounceLandFilter()

    data = {
        "name": "Dimir Aqueduct",
        "oracle_text": (
            "Dimir Aqueduct enters the battlefield tapped.\n"
            "When Dimir Aqueduct enters the battlefield, return a land "
            "you control to its owner's hand.\n"
            "{T}: Add {U}{B}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "name": "Dimir Aqueduct",
        "oracle_text": (
            "Dimir Aqueduct enters the battlefield tapped.\n"
            "When Dimir Aqueduct enters the battlefield, return a land "
            "you control to its owner's hand.\n"
            "{T}: Add {U}{B}.\nSome text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
