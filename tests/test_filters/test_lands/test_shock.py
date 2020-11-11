"""Test shock lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.shock import ShockLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = ShockLandFilter()

    data = {
        "name": "Hallowed Fountain",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "As Hallowed Fountain enters the battlefield, you may pay 2 life. "
            "If you don't, it enters the battlefield tapped."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Hallowed Fountain",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "As Hallowed Fountain enters the battlefield, you may pay 2 life. "
            "If you don't, it enters the battlefield tapped.\nSome text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
