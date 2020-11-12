"""Test banners filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.rocks.banner import BannerFilter


def test_filter(make_card):
    filter_ = BannerFilter()

    data = {
        "name": "Abzan Banner",
        "oracle_text": (
            "{T}: Add {W}, {B}, or {G}.\n"
            "{W}{B}{G}, {T}, Sacrifice Abzan Banner: Draw a card."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is not None

    data = {
        "name": "Abzan Banner",
        "oracle_text": (
            "{T}: Add {W}, {B}, or {G}.\n"
            "{W}{B}{G}, {T}, Sacrifice Abzan Banner: Draw a card."
            "Some text"
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card).accepted_by is None
