"""Test lockets filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.locket import LocketFilter


def test_filter(make_card):
    filter_ = LocketFilter()

    data = {
        "name": "Orzhov Locket",
        "oracle_text": (
            "{T}: Add {W} or {B}.\n"
            "{W/B}{W/B}{W/B}{W/B}, {T}, Sacrifice Orzhov Locket: Draw two cards."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Orzhov Locket",
        "oracle_text": (
            "{T}: Add {W} or {B}.\n"
            "{W/B}{W/B}{W/B}{W/B}, {T}, Sacrifice Orzhov Locket: Draw two cards."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
