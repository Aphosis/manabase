"""Filter management."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from ..cards import Card
from ..colors import Color
from ..filters.base import FilterResult
from ..filters.colors import BasicLandReferencedFilter, ProducedManaFilter
from ..filters.composite import CompositeFilter
from ..filters.lands.battle import BattleLandFilter
from ..filters.lands.check import CheckLandFilter
from ..filters.lands.fetch import FetchLandFilter
from ..filters.lands.original import OriginalDualLandFilter
from ..filters.lands.reveal import RevealLandFilter
from ..filters.lands.shock import ShockLandFilter
from .parser import parse_filter_string


class FilterManager(BaseModel):
    """Filter lists of cards."""

    colors: List[Color]
    filters: CompositeFilter

    @classmethod
    def default(cls, colors: List[Color]) -> FilterManager:
        """Create a default filter tree."""
        return cls(
            colors=colors,
            filters=(
                ProducedManaFilter(colors=colors)
                & (
                    OriginalDualLandFilter()
                    | ShockLandFilter()
                    | BattleLandFilter()
                    | CheckLandFilter()
                    | RevealLandFilter()
                )
            )
            | (
                BasicLandReferencedFilter(
                    colors=colors,
                    exclusive=False,
                    minimum_count=1,
                )
                & FetchLandFilter()
            ),
        )

    @classmethod
    def from_string(cls, filter_string: str, colors: List[Color]) -> FilterManager:
        """Create a filter tree from a filter string."""
        filters = parse_filter_string(filter_string, colors)
        return cls(colors=colors, filters=filters)

    def filter_cards(self, cards: List[Card]) -> List[FilterResult]:
        """Filter a list of cards."""
        results = []

        for card in cards:

            res = self.filters.filter_card(card)

            if res.accepted_by is not None:
                results.append(res)

        return results
