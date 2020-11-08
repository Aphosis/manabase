"""Test battle lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.battle import BattleLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = BattleLandFilter()

    data = {
        "name": "Prairie Stream",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Prairie Stream enters the battlefield tapped unless you control "
            "two or more basic lands."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "name": "Prairie Stream",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Prairie Stream enters the battlefield tapped unless you control "
            "two or more basic lands."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
