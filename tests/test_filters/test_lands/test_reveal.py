"""Test reveal lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.reveal import RevealLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = RevealLandFilter()

    data = {
        "name": "Port Town",
        "oracle_text": (
            "As Port Town enters the battlefield, you may reveal a "
            "Plains or Island card from your hand. If you don't, "
            "Port Town enters the battlefield tapped.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "name": "Silent Clearing",
        "oracle_text": (
            "{T}, Pay 1 life: Add {W} or {B}.\n"
            "{1}, {T}, Sacrifice Silent Clearing: Draw a card."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
