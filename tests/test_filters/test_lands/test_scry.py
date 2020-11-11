"""Test scry lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.scry import ScryLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = ScryLandFilter()

    data = {
        "name": "Temple of Enlightenment",
        "oracle_text": (
            "Temple of Enlightenment enters the battlefield tapped.\n"
            "When Temple of Enlightenment enters the battlefield, scry 1. "
            "(Look at the top card of your library. You may put that card "
            "on the bottom of your library.)\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Temple of Enlightenment",
        "oracle_text": (
            "Temple of Enlightenment enters the battlefield tapped.\n"
            "When Temple of Enlightenment enters the battlefield, scry 1. "
            "(Look at the top card of your library. You may put that card "
            "on the bottom of your library.)\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
