"""Test cluestones filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.cluestone import CluestoneFilter


def test_filter(make_card):
    filter_ = CluestoneFilter()

    data = {
        "name": "Orzhov Cluestone",
        "oracle_text": (
            "{T}: Add {W} or {B}.\n"
            "{W}{B}, {T}, Sacrifice Orzhov Cluestone: Draw a card."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Orzhov Cluestone",
        "oracle_text": (
            "{T}: Add {W} or {B}.\n"
            "{W}{B}, {T}, Sacrifice Orzhov Cluestone: Draw a card."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
