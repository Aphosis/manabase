"""Test original dual lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.original import OriginalDualLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = OriginalDualLandFilter()

    data = {
        "oracle_text": "({T}: Add {W} or {U}.)",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "oracle_text": "({T}: Add {W} or {U}.)\nSome text.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
