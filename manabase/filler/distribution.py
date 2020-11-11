"""Compute cards distributions."""
from abc import ABCMeta, abstractmethod
from math import ceil
from typing import List

from pydantic import BaseModel, validator

from ..cards import Card, CardList


class Distribution(BaseModel, metaclass=ABCMeta):
    """Computes a distribution of cards."""

    maximum: int
    cards: List[Card]

    @abstractmethod
    def compute(self) -> CardList:
        """Compute a card list filled with `Distribution.cards`.

        Occurrences of each card are based on `Distribution.weights`.

        Example::

        ```python
        >>> from manabase.filler.distribution import Distribution
        >>> from manabase.cards import CardList
        >>> class SimpleDistribution(Distribution):
        ...     def compute(self):
        ...         card_list = CardList(self.maximum)
        ...         for card in self.cards:
        ...             card_list.add_card(card, 1)
        ...         return card_list
        >>> cards = [Card.named('card 1')]
        >>> distribution = SimpleDistribution(maximum=1, cards=cards)
        >>> distribution.compute()
        CardList(entries=[CardEntry(name='card 1'...)], ...)

        ```
        """


class WeightedDistribution(Distribution):
    """Perform a weighted distribution of cards.

    Example::

    ```python
    >>> from manabase.filler.distribution import WeightedDistribution
    >>> cards = [Card.named("Plains"), Card.named("Island"), Card.named("Swamp")]
    >>> weights = [3, 1, 3]
    >>> distribution = WeightedDistribution(cards=cards, maximum=21, weights=weights)
    >>> distribution.compute()
    CardList(entries=[CardEntry(name='Plains'...occurrences=9), CardEntry(name='Island'\
...occurrences=3), CardEntry(name='Swamp'...occurrences=9)]...)

    ```
    """

    weights: List[int]

    def compute(self) -> CardList:
        """Compute a card list filled with `Distribution.cards`.

        Occurrences of each card are based on `Distribution.weights`.
        """
        card_list = CardList(self.maximum)
        total_weight = sum(self.weights)
        for card, weight in zip(self.cards, self.weights):
            occurrences = ceil(weight * self.maximum / total_weight)
            card_list.add_card(card, occurrences)
        return card_list

    @validator("weights")
    @classmethod
    def validate_weights(cls, weights, values):
        """Ensure each card has a weight."""
        if len(weights) != len(values["cards"]):
            raise ValueError(
                "Weighted distribution should have the "
                "same number of weights and cards."
            )
        return weights
