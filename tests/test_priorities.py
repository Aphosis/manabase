# pylint: disable=missing-module-docstring, missing-function-docstring
from typing import Callable

from manabase.cards import Card
from manabase.filter.data import FilterAlias
from manabase.filters.base import FilterResult
from manabase.filters.lands.original import OriginalDualLandFilter
from manabase.filters.lands.shock import ShockLandFilter
from manabase.priorities import PriorityManager


def test_build_list(make_card: Callable[..., Card]):
    priorities = [FilterAlias.original, FilterAlias.shock]
    manager = PriorityManager(priorities=priorities)

    original = OriginalDualLandFilter()
    shock = ShockLandFilter()

    results = [
        FilterResult(card=make_card(name="unfiltered"), accepted_by=None),
        FilterResult(card=make_card(name="original 1"), accepted_by=original),
        FilterResult(card=make_card(name="shock"), accepted_by=shock),
        FilterResult(card=make_card(name="original 2"), accepted_by=original),
    ]

    card_list = manager.build_list(results)

    assert [card.name for card in card_list.entries] == [
        "original 1",
        "original 2",
        "shock",
        "unfiltered",
    ]
