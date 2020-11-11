"""Test bond lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.bond import BondLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = BondLandFilter()

    data = {
        "name": "Sea of Clouds",
        "oracle_text": (
            "Sea of Clouds enters the battlefield tapped unless you have "
            "two or more opponents.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Sea of Clouds",
        "oracle_text": (
            "Sea of Clouds enters the battlefield tapped unless you have "
            "two or more opponents.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
