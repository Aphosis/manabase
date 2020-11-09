"""Filter our cards based on their color identity."""
import re
from typing import List

from ..cards import Card
from ..colors import Color
from .composite import CompositeFilter


class ProducedManaFilter(CompositeFilter):
    """A filter checking for colors in the card produced mana.

    Args:
        colors (List[Color]): A list of `Color`s to match.
        exclusive (bool): If ``True``, exclude all cards containing a color
            outside ``colors``.
        minimum_count (int): Minimum amount of colors matched from ``colors`` in
            the card produced mana.

    Example::

    ```python
    >>> from manabase.filters.colors import ProducedManaFilter
    >>> from manabase.colors import Color
    >>> from manabase.cards import Card
    >>> colors = [Color.white, Color.blue, Color.black]
    >>> filter_ = ProducedManaFilter(colors)
    >>> card = Card(
    ...     name="",
    ...     oracle_text="",
    ...     colors=[],
    ...     color_identity=[],
    ...     produced_mana=["W", "U"],
    ...     legalities={},
    ...     textless=False,
    ...     scryfall_uri="",
    ... )
    >>> filter_.filter_value(card)
    True
    >>> card.produced_mana = ["W", "U", "G"]
    >>> filter_.filter_value(card)
    False
    >>> filter_.exclusive = False
    >>> filter_.filter_value(card)
    True
    >>> card.produced_mana = ["W"]
    >>> filter_.filter_value(card)
    False
    >>> filter_.minimum_count = 1
    >>> filter_.filter_value(card)
    True

    ```
    """

    def __init__(self, colors: List[Color], exclusive=True, minimum_count=2):
        self.colors = set(colors)
        self.exclusive = exclusive
        self.minimum_count = minimum_count

    def filter_value(self, value: Card) -> bool:
        produced_mana = [Color(mana) for mana in value.produced_mana if mana != "C"]
        if self.exclusive and not set(produced_mana).issubset(self.colors):
            return False
        if len(self.colors.intersection(produced_mana)) < self.minimum_count:
            return False
        return True


class BasicLandReferencedFilter(CompositeFilter):
    """A filter checking if the card text referenced some basic land names.

    Args:
        colors (List[Color]): A list of `Color`s to match their basic land names.
        exclusive (bool): If ``True``, exclude all cards containing a land name
            outside ``colors``.
        minimum_count (int): Minimum amount of land name matched from ``colors`` in
            the card text.

    Example::

    ```python
    >>> from manabase.filters.colors import BasicLandReferencedFilter
    >>> from manabase.colors import Color
    >>> from manabase.cards import Card
    >>> colors = [Color.white, Color.blue, Color.black]
    >>> filter_ = BasicLandReferencedFilter(colors)
    >>> card = Card(
    ...     name="",
    ...     oracle_text="a Plains or Island",
    ...     colors=[],
    ...     color_identity=[],
    ...     produced_mana=[],
    ...     legalities={},
    ...     textless=False,
    ...     scryfall_uri="",
    ... )
    >>> filter_.filter_value(card)
    True
    >>> card.oracle_text = "a Plains, Island or Forest"
    >>> filter_.filter_value(card)
    False
    >>> filter_.exclusive = False
    >>> filter_.filter_value(card)
    True
    >>> card.oracle_text = "a Plains"
    >>> filter_.filter_value(card)
    False
    >>> filter_.minimum_count = 1
    >>> filter_.filter_value(card)
    True

    ```
    """

    def __init__(self, colors: List[Color], exclusive=True, minimum_count=2):
        self.colors = set(colors)
        self.exclusive = exclusive
        self.minimum_count = minimum_count
        self.names = set(color.to_basic_land_name() for color in colors)
        self._regex = re.compile("(Plains|Island|Swamp|Mountain|Forest)")

    def filter_value(self, value: Card) -> bool:
        names = set(self._extract_basic_land_names(value))
        if self.exclusive and not names.issubset(self.names):
            return False
        if len(self.names.intersection(names)) < self.minimum_count:
            return False
        return True

    def _extract_basic_land_names(self, card: Card) -> List[str]:
        """Extract basic land names from a card text.

        Example::

        ```python
        >>> from manabase.filters.colors import BasicLandReferencedFilter
        >>> filter_ = BasicLandReferencedFilter([])
        >>> card = Card(
        ...     name="",
        ...     oracle_text="a Plains or Island",
        ...     colors=[],
        ...     color_identity=[],
        ...     produced_mana=[],
        ...     legalities={},
        ...     textless=False,
        ...     scryfall_uri="",
        ... )
        >>> filter_._extract_basic_land_names(card)
        ['Plains', 'Island']
        >>> card.oracle_text = "a Plains, Island, Swamp, Mountain of Forest"
        >>> filter_._extract_basic_land_names(card)
        ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']

        ```
        """
        names = filter(None, self._regex.findall(card.oracle_text))
        return list(names)
