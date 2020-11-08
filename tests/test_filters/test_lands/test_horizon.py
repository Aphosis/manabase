"""Test horizon lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.horizon import HorizonLandFilter


def test_horizon_land_filter(make_card):
    filter_ = HorizonLandFilter()

    data = {
        "name": "Silent Clearing",
        "oracle_text": (
            "{T}, Pay 1 life: Add {W} or {B}.\n"
            "{1}, {T}, Sacrifice Silent Clearing: Draw a card."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "name": "Silent Clearing",
        "oracle_text": (
            "{T}, Pay 1 life: Add {W} or {B}.\n"
            "{1}, {T}, Sacrifice Silent Clearing: Draw a card."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
