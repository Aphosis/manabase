"""Test signets filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.signet import SignetFilter


def test_filter(make_card):
    filter_ = SignetFilter()

    data = {
        "name": "Orzhov Signet",
        "oracle_text": "{1}, {T}: Add {W}{B}.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Orzhov Signet",
        "oracle_text": "{1}, {T}: Add {W}{B}.Some text.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
