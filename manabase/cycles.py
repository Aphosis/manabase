"""A description of every relevant land cycle you might want to play.

Land cycles are archetypes of lands, as defined by the following MTG gamepedia pages:
https://mtg.gamepedia.com/Dual_land
https://mtg.gamepedia.com/Triple_land

By default a competitive-ish set of cycles are active, but users can add
disable, or provide their own set of cycles.
"""
from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List

from .cards import Card
from .colors import Color


class Cycle(Enum):
    """Archetypes of lands."""

    original = "original"
    pain = "pain"
    fetch = "fetch"
    filter = "filter"
    bounce = "bounce"
    shock = "shock"
    horizon = "horizon"
    scry = "scry"
    battle = "battle"
    check = "check"
    fast = "fast"
    reveal = "reveal"
    cycling = "cycling"
    bond = "bond"
    nimbus = "nimbus"
    changing = "changing"
    opponent_boon = "opponent_boon"
    man = "man"
    pathway = "pathway"
    shard = "shard"
    wedge = "wedge"

    @classmethod
    def default(cls) -> List[Cycle]:
        """Return a default list of cycles."""
        return [
            cls.original,
            cls.fetch,
            cls.shock,
            cls.battle,
            cls.check,
            cls.reveal,
            cls.pathway,
        ]


UNSUPPORTED = [
    Cycle.nimbus,
    Cycle.changing,
    Cycle.opponent_boon,
    Cycle.man,
    Cycle.pathway,
    Cycle.shard,
    Cycle.wedge,
]

# TODO: Convert land filters to regular filters.
# TODO: Add and and or methods to filters.
# TODO: Move land filters to `manabase.filters` package.
# TODO: Actually make a ``filters`` package.
# TODO: Change land filters constructor to accept combinations directly.
# TODO: Filter land cycles by extension first.
# TODO: Support cycle pattern by extension (bounce lands texts are different
# for Ravnica and Visions for example).


class LandCycleFilter(metaclass=ABCMeta):  # pylint: disable=too-few-public-methods
    """Filters a single card by matching its color, and specific text data.

    For example, implementing a pain land filter:

    Example::

    ```python
    class PainLandFilter(LandCycleFilter):
        def filter_card(self, card: Card) -> bool:
            color_identity = set(Color.to_string(*self.colors).split())
            if color_identity != set(card.color_identity):
                return False

            color_identity.add("C")
            if color_identity != card.produced_mana:
                return False

            if "deals 1 damage to you" not in card.oracle_text:
                return False

            return True
    ```
    """

    def __init__(self, colors: List[Color], ignore_colors: bool = False):
        self.colors = colors
        self.ignore_colors = ignore_colors
        dual_colors = list(colors) if not ignore_colors else Color.all()
        self.combinations = Color.dual_combinations(dual_colors)

    @abstractmethod
    def filter_card(self, card: Card) -> bool:
        """Return ``True`` if ``card`` matches this filter."""


class OriginalDualLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters original dual lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\(\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.\)$"
                % {
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class PainLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters pain lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"\{T\}: Add \{C\}.\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}. %(name)s deals 1 damage to you."
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class FetchLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters fetch lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\{T\}, Pay 1 life, Sacrifice %(name)s: "
                r"Search your library for (a|an) "
                r"(%(first)s|%(second)s) or "
                r"(%(first)s|%(second)s) card, "
                r"put it onto the battlefield, then shuffle your library.$"
                % {
                    "name": card.name,
                    "first": combination[0].to_basic_land_name(),
                    "second": combination[1].to_basic_land_name(),
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class FilterLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters filter lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\{1\}, \{T\}: Add \{(%(first)s|%(second)s)\}"
                r"\{(%(first)s|%(second)s)\}.$"
                % {
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class BounceLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters bounce lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^%(name)s enters the battlefield tapped.\n"
                r"When %(name)s enters the battlefield, return a land "
                r"you control to its owner's hand.\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\}\{(%(first)s|%(second)s)\}.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class ShockLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters shock lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\(\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.\)\n"
                r"As %(name)s enters the battlefield, you may pay 2 life. "
                "If you don't, it enters the battlefield tapped.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class HorizonLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters horizon lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\{T\}, Pay 1 life: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.\n"
                r"\{1\}, \{T\}, Sacrifice %(name)s: Draw a card.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class ScryLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters scry lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^%(name)s enters the battlefield tapped.\n"
                r"When %(name)s enters the battlefield, scry 1. "
                r"\(Look at the top card of your library. You may put that card "
                r"on the bottom of your library.\)\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\} or \{(%(first)s|%(second)s)\}.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class BattleLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters battle lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\(\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.\)\n"
                r"%(name)s enters the battlefield tapped unless you control "
                r"two or more basic lands.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class CheckLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters check lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^%(name)s enters the battlefield tapped unless you control "
                r"(a|an) (%(first_name)s|%(second_name)s) or (a|an) "
                r"(%(first_name)s|%(second_name)s).\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                    "first_name": combination[0].to_basic_land_name(),
                    "second_name": combination[1].to_basic_land_name(),
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class FastLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters fast lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^%(name)s enters the battlefield tapped unless you control "
                r"two or fewer other lands.\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class RevealLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters reveal lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^As %(name)s enters the battlefield, you may reveal (a|an) "
                r"(%(first_name)s|%(second_name)s) or (%(first_name)s|%(second_name)s) "
                r"card from your hand. If you don't, %(name)s enters "
                "the battlefield tapped.\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                    "first_name": combination[0].to_basic_land_name(),
                    "second_name": combination[1].to_basic_land_name(),
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class CyclingLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters cycling lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^\(\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.\)\n"
                r"%(name)s enters the battlefield tapped.\n"
                r"Cycling \{2\} \(\{2\}, Discard this card: Draw a card.\)$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True


class BondLandFilter(LandCycleFilter):  # pylint: disable=too-few-public-methods
    """Filters bond lands."""

    def filter_card(self, card: Card) -> bool:
        for combination in self.combinations:
            pattern = (
                r"^%(name)s enters the battlefield tapped unless you have "
                r"two or more opponents.\n"
                r"\{T\}: Add \{(%(first)s|%(second)s)\} or "
                r"\{(%(first)s|%(second)s)\}.$"
                % {
                    "name": card.name,
                    "first": combination[0].value,
                    "second": combination[1].value,
                }
            )
            if re.match(pattern, card.oracle_text):
                break
        else:
            return False

        return True
