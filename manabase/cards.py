"""Cards data structure.

Cards data are fetched from scryfall API, and reduced to a minimal set of data
as the original scryfall response contains a lot of information, such as artist
and artwork related data, price data, etc...
"""
from __future__ import annotations

from functools import total_ordering
from typing import Dict, List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


@total_ordering
class Card(BaseModel):
    """A single card data.

    Only relevant data is shown here, and is parsed from a scryfall API response.
    """

    name: str
    oracle_text: str
    colors: List[str]
    color_identity: List[str]
    produced_mana: List[str]
    legalities: Dict[str, str]
    textless: bool
    scryfall_uri: str

    def __hash__(self) -> int:
        return hash(self.json())

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Card) -> bool:
        return self.json() == other.json()

    def __lt__(self, other: Card) -> bool:
        return self.name < other.name


class MaximumSizeExceeded(Exception):
    """Raised when the maximum number of occurrences has been exceeded."""


class CardEntry(Card):
    """Card occurrences in a list."""

    occurrences: int


class CardList(BaseModel):
    """List of cards, including metadata such as remaining slots."""

    entries: List[CardEntry]
    maximum: int
    available: int

    entries_by_name: Dict[str, CardEntry]

    def __init__(self, maximum: int):
        super().__init__(
            entries=[],
            maximum=maximum,
            available=maximum,
            entries_by_name={},
        )

    def add_card(self, card: Card, occurrences: int):
        """Add a new card to this card list.

        Raises:
            MaximumSizeExceeded: When you exceed the `CardList.maximum` size
                fixed.
        """
        existing = self.by_name(card.name)

        if not existing:
            entry = CardEntry(occurrences=0, **card.dict())
            self.entries_by_name[entry.name] = entry
            self.entries.append(entry)
            existing = entry

        existing.occurrences += occurrences

        # PyLance seems to dislike `self.available -= occurrences`
        self.available = self.available - occurrences

        if self.available < 0:
            raise MaximumSizeExceeded(
                f"This card list is limited to {self.maximum} cards."
            )

    def by_name(self, name: str) -> Optional[CardEntry]:
        """Return a entry by name."""
        return self.entries_by_name.get(name)
