"""Filter management."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from ..cards import Card
from ..colors import Color
from ..filters.base import FilterResult
from ..filters.composite import CompositeFilter
from .parser import parse_filter_string


class FilterManager(BaseModel):
    """Filter lists of cards."""

    colors: List[Color]
    filters: CompositeFilter

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
