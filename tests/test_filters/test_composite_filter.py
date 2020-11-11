"""Test `CompositeFilter`."""
# pylint: disable=no-self-use, missing-function-docstring
from manabase.cards import Card
from manabase.colors import Color
from manabase.filters.base import FilterResult
from manabase.filters.composite import CompositeFilter


class WhiteColorFilter(CompositeFilter):
    """Filters integer values strictly under ``maximum``."""

    def filter_card(self, card: Card) -> FilterResult:
        if Color.white.value in card.colors:
            return FilterResult(card=card, accepted_by=self)
        return FilterResult(card=card)


class BlueColorFilter(CompositeFilter):
    """Filters integer values strictly under ``maximum``."""

    def filter_card(self, card: Card) -> FilterResult:
        if Color.blue.value in card.colors:
            return FilterResult(card=card, accepted_by=self)
        return FilterResult(card=card)


def test_composite_filter_and(make_card):
    left = WhiteColorFilter()
    right = BlueColorFilter()
    filter_ = left & right

    card = make_card()
    assert filter_.filter_card(card).accepted_by is None

    card.colors = ["W"]
    assert filter_.filter_card(card).accepted_by is None

    card.colors = ["U"]
    assert filter_.filter_card(card).accepted_by is None

    card.colors = ["W", "U"]
    assert filter_.filter_card(card).accepted_by == right


def test_composite_filter_or(make_card):
    left = WhiteColorFilter()
    right = BlueColorFilter()
    filter_ = left | right

    card = make_card()
    assert filter_.filter_card(card).accepted_by is None

    card.colors = ["W"]
    assert filter_.filter_card(card).accepted_by == left

    card.colors = ["U"]
    assert filter_.filter_card(card).accepted_by == right

    card.colors = ["W", "U"]
    assert filter_.filter_card(card).accepted_by == right


def test_composite_filter_xor(make_card):
    left = WhiteColorFilter()
    right = BlueColorFilter()
    filter_ = left ^ right

    card = make_card()
    assert filter_.filter_card(card).accepted_by is None

    card.colors = ["W"]
    assert filter_.filter_card(card).accepted_by == left

    card.colors = ["U"]
    assert filter_.filter_card(card).accepted_by == right

    card.colors = ["W", "U"]
    assert filter_.filter_card(card).accepted_by is None


def test_composite_filter_invert(make_card):
    leaf = WhiteColorFilter()
    filter_ = ~leaf

    card = make_card()
    assert filter_.filter_card(card).accepted_by == leaf

    card.colors = ["W"]
    assert filter_.filter_card(card).accepted_by is None
