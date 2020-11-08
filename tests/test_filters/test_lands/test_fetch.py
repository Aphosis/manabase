"""Test fetch lands filtering."""
# pylint: disable=missing-function-docstring
from manabase.filters.lands.fetch import FetchLandFilter


def test_original_dual_land_filter(make_card):
    filter_ = FetchLandFilter()

    data = {
        "name": "Flooded Strand",
        "oracle_text": (
            "{T}, Pay 1 life, Sacrifice Flooded Strand: "
            "Search your library for a Plains or Island card, put it "
            "onto the battlefield, then shuffle your library."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_value(card)

    data = {
        "name": "Flooded Strand",
        "oracle_text": (
            "{T}, Pay 1 life, Sacrifice Flooded Strand: "
            "Search your library for a Plains or Island card, put it "
            "onto the battlefield, then shuffle your library."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_value(card)
