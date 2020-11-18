"""Default values of the application.

Here you can find the default filters and priority lists for both lands and rocks.
"""
from typing import List

from .colors import Color
from .filter.data import FilterAlias
from .filters.colors import BasicLandReferencedFilter, ProducedManaFilter
from .filters.composite import CompositeFilter
from .filters.lands.battle import BattleLandFilter
from .filters.lands.check import CheckLandFilter
from .filters.lands.fetch import FetchLandFilter
from .filters.lands.original import OriginalDualLandFilter
from .filters.lands.reveal import RevealLandFilter
from .filters.lands.shock import ShockLandFilter
from .filters.rocks.crystal import CrystalFilter
from .filters.rocks.obelisk import ObeliskFilter
from .filters.rocks.signet import SignetFilter
from .filters.rocks.talisman import TalismanFilter


def default_land_filters(colors: List[Color]) -> CompositeFilter:
    """Build and return default land filters."""
    return (
        ProducedManaFilter(colors=colors)
        & (
            OriginalDualLandFilter()
            | ShockLandFilter()
            | BattleLandFilter()
            | CheckLandFilter()
            | RevealLandFilter()
        )
    ) | (
        BasicLandReferencedFilter(
            colors=colors,
            exclusive=False,
            minimum_count=1,
        )
        & FetchLandFilter()
    )


def default_land_priorities() -> List[FilterAlias]:
    """Return default land priorities."""
    return [
        FilterAlias.fetch,
        FilterAlias.original,
        FilterAlias.shock,
        FilterAlias.battle,
        FilterAlias.check,
        FilterAlias.reveal,
    ]


def default_rock_filters(colors: List[Color]) -> CompositeFilter:
    """Build and return default rock filters."""
    return ProducedManaFilter(colors=colors) & (
        SignetFilter() | TalismanFilter() | CrystalFilter() | ObeliskFilter()
    )


def default_rock_priorities() -> List[FilterAlias]:
    """Return default rock priorities."""
    return [
        FilterAlias.signet,
        FilterAlias.talisman,
        FilterAlias.crystal,
        FilterAlias.obelisk,
    ]
