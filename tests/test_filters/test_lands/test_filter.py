"""Test filter lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.filter import FilterLandFilter


def test_filter_land_filter(make_card):
    filter_ = FilterLandFilter()

    data = {
        "oracle_text": "{1}, {T}: Add {W}{U}.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "oracle_text": "{1}, {T}: Add {W}{U}.\nSome text.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
