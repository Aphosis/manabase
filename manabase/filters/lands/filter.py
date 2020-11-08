"""Filters filter lands."""
from manabase.filters.lands.base import LandFilter


class FilterLandFilter(LandFilter):
    """Filters filter lands."""

    def __init__(self):
        pattern = r"^\{1\}, %(tap)s: Add %(symbols)s%(symbols)s\.$"
        super().__init__(pattern)
