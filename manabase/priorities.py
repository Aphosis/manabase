"""Manage a list of priorities.

When the targetted number if lands is reached, priorities can be set to
decide whichever land is returned first, and whichever is discarded.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .cards import Card
from .filter.data import FilterAlias
from .filters.base import FilterResult


class CardEntry(Card):
    """Card occurrences in a list."""

    occurrences: int


class PriorityManager(BaseModel):
    """Build prioritized lists of cards."""

    lands: int = 23
    occurrences: int = 1
    priorities: List[FilterAlias]

    @classmethod
    def default(cls, lands: int = 23, occurrences: int = 4) -> PriorityManager:
        """Build a default priority manager."""
        priorities = [
            FilterAlias.fetch,
            FilterAlias.original,
            FilterAlias.shock,
            FilterAlias.battle,
            FilterAlias.check,
            FilterAlias.reveal,
        ]
        return cls(lands=lands, occurrences=occurrences, priorities=priorities)

    @classmethod
    def from_string(
        cls,
        priorities: str,
        lands: int = 23,
        occurrences: int = 4,
    ) -> PriorityManager:
        """Build a priority manager from a string of space separated aliases.

        Example::
        ```python
        >>> from manabase.priorities import PriorityManager
        >>> string = "original fetch"
        >>> PriorityManager.from_string(string)
        PriorityManager(lands=23, occurrences=4, priorities=[<FilterAlias.original: \
'original'>, <FilterAlias.fetch: 'fetch'>])

        ```
        """
        priorities_list = [FilterAlias(alias) for alias in priorities.split()]
        return cls(lands=lands, occurrences=occurrences, priorities=priorities_list)

    def truncate_results(self, results: List[FilterResult]) -> List[CardEntry]:
        """Build a new list of cards by truncating the specified one."""
        card_entries = []

        if self.priorities:
            results.sort(key=self._result_key, reverse=True)

        remaining_slots = self.lands

        for result in results:
            if remaining_slots >= self.occurrences:
                occurrences = self.occurrences
            else:
                occurrences = remaining_slots

            entry = CardEntry(occurrences=occurrences, **result.card.dict())
            card_entries.append(entry)

            remaining_slots -= occurrences
            if remaining_slots == 0:
                break

        return card_entries

    def _result_key(self, result: FilterResult) -> int:
        """Return a priority key for ``result``.

        Raises:
            KeyError: If accepting filter has no alias.
        """
        if not result.accepted_by:
            return -1

        alias = FilterAlias.alias(result.accepted_by)

        try:
            return len(self.priorities) - self.priorities.index(alias)
        except ValueError:
            return -1
