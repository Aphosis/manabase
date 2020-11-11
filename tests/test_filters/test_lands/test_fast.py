"""Test fast lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.fast import FastLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = FastLandFilter()

    data = {
        "name": "Seachrome Coast",
        "oracle_text": (
            "Seachrome Coast enters the battlefield tapped unless you control "
            "two or fewer other lands.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Seachrome Coast",
        "oracle_text": (
            "Seachrome Coast enters the battlefield tapped unless you control "
            "two or fewer other lands.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
