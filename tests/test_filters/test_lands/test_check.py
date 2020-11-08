"""Test check lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.check import CheckLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = CheckLandFilter()

    data = {
        "name": "Glacial Fortress",
        "oracle_text": (
            "Glacial Fortress enters the battlefield tapped unless you control "
            "a Plains or an Island.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "name": "Glacial Fortress",
        "oracle_text": (
            "Glacial Fortress enters the battlefield tapped unless you control "
            "a Plains or an Island.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
