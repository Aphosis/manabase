# pylint: disable=missing-module-docstring, missing-function-docstring
from typing import Callable

from manabase.cards import Card


def test_card_hashable(make_card: Callable[..., Card]):
    card = make_card(name="Swamp")
    hash(card)


def test_card_str(make_card: Callable[..., Card]):
    card = make_card(name="Swamp")
    assert str(card) == "Swamp"


def test_card_eq(make_card: Callable[..., Card]):
    card1 = make_card(name="Plains")
    card2 = make_card(name="Swamp")

    assert card1 != card2

    card2 = make_card(name="Plains")

    assert card1 == card2


def test_card_lt(make_card: Callable[..., Card]):
    card1 = make_card(name="Plains")
    card2 = make_card(name="Swamp")

    assert card1 < card2
