"""Filter a scryfall query string and results.

Filters provide a mean to optimize the scryfall query, and to filter
its results.
"""
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Type

from .cards import Card
from .colors import Color
from .cycles import (
    UNSUPPORTED,
    BattleLandFilter,
    BondLandFilter,
    BounceLandFilter,
    CheckLandFilter,
    Cycle,
    CyclingLandFilter,
    FastLandFilter,
    FetchLandFilter,
    FilterLandFilter,
    HorizonLandFilter,
    LandCycleFilter,
    OriginalDualLandFilter,
    PainLandFilter,
    RevealLandFilter,
    ScryLandFilter,
    ShockLandFilter,
)


class BaseFilter(metaclass=ABCMeta):
    """Base class for filters.

    To implement a new filter, subclass `BaseFilter` and implement
    `BaseFilter.contributes_to_query`, `BaseFilter.filter_cards`, and optionally
    `BaseFilter.query` if `BaseFilter.contributes_to_query` returns ``True``.
    """

    def query(self) -> Optional[str]:  # pylint: disable=no-self-use
        """Return a query parameter to add to the scryfall query.

        Examples::

        ```python
        class MyFilter(BaseFilter):
            def query(self) -> str:
                return "provides:wu"
        ```

        If the query is not meant to be modified by this filter, return ``None``.

        This is the default behavior.

        For a reference of the query syntax, you can refer to the official
        [scryfall documentation](https://scryfall.com/docs/syntax).
        """
        return None

    @abstractmethod
    def filter_cards(self, cards: List[Card]) -> List[Card]:
        """Filter a list of cards."""


class ProvideColorFilter(BaseFilter):
    """Filter cards based on the color they provide."""

    def __init__(self, *colors: Color, minimum_colors: int = 2):
        self.colors = colors
        self.minimum_colors = minimum_colors

    def query(self) -> Optional[str]:
        return f"provides:{Color.to_string(*self.colors)}"

    def filter_cards(self, cards: List[Card]) -> List[Card]:
        """Filter cards based on their ``provides`` attribute."""
        subset = set(Color.to_string(*self.colors))
        filtered_cards = []
        for card in cards:

            if not card.produced_mana:
                # This could be a fetch land, let it through.
                filtered_cards.append(card)
                continue

            color_match = subset.intersection(set(card.produced_mana))
            if not len(color_match) >= self.minimum_colors:
                # This land does not match our colors, or not enough colors.
                continue

            filtered_cards.append(card)
        return filtered_cards


class CycleFilter(BaseFilter):
    """Filter cards based on their land cycle."""

    CYCLE_TO_FILTER = {
        Cycle.original: OriginalDualLandFilter,
        Cycle.pain: PainLandFilter,
        Cycle.fetch: FetchLandFilter,
        Cycle.filter: FilterLandFilter,
        Cycle.bounce: BounceLandFilter,
        Cycle.shock: ShockLandFilter,
        Cycle.horizon: HorizonLandFilter,
        Cycle.scry: ScryLandFilter,
        Cycle.battle: BattleLandFilter,
        Cycle.check: CheckLandFilter,
        Cycle.fast: FastLandFilter,
        Cycle.reveal: RevealLandFilter,
        Cycle.cycling: CyclingLandFilter,
        Cycle.bond: BondLandFilter,
    }

    def __init__(
        self,
        colors: List[Color],
        cycles: List[Cycle],
        ignore_colors: Optional[List[Cycle]] = None,
    ):
        ignore_colors = ignore_colors or []
        land_filter_types = [CycleFilter.filter_for_cycle(cycle) for cycle in cycles]
        self.land_filters = [
            filter_type(colors, cycle in ignore_colors)
            for cycle, filter_type in zip(cycles, land_filter_types)
            if filter_type
        ]

    def filter_cards(self, cards: List[Card]) -> List[Card]:
        """Filter cards based on their ``provides`` attribute."""
        filtered_cards = []
        for card in cards:
            for land_filter in self.land_filters:
                if not land_filter.filter_card(card):
                    continue
                filtered_cards.append(card)
                break
        return filtered_cards

    @staticmethod
    def filter_for_cycle(cycle: Cycle) -> Optional[Type[LandCycleFilter]]:
        """Return a filter for a specific land cycle."""
        if cycle in UNSUPPORTED:
            return None
        return CycleFilter.CYCLE_TO_FILTER.get(cycle, None)
