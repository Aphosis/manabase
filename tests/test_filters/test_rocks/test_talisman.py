"""Test talismans filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.talisman import TalismanFilter


def test_filter(make_card):
    filter_ = TalismanFilter()

    data = {
        "name": "Talisman of Hierarchy",
        "oracle_text": (
            "{T}: Add {C}.\n"
            "{T}: Add {W} or {B}. Talisman of Hierarchy deals 1 damage to you."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Talisman of Hierarchy",
        "oracle_text": (
            "{T}: Add {C}.\n"
            "{T}: Add {W} or {B}. Talisman of Hierarchy deals 1 damage to you."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
