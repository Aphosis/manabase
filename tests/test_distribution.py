# pylint: disable=missing-module-docstring, missing-function-docstring
from typing import Callable

import pytest

from manabase.cards import Card
from manabase.filler.distribution import WeightedDistribution


def test_weighted_distribution_wrong_number(make_card: Callable[..., Card]):
    distribution = WeightedDistribution(weights=[1, 2, 3, 4])

    cards = [
        make_card(name="Plains"),
        make_card(name="Island"),
        make_card(name="Swamp"),
    ]

    with pytest.raises(ValueError, match=r"^.*should be computed on 4 cards\.$"):
        distribution.compute(1, cards)
