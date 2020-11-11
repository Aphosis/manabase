"""Test filter parsing."""
from manabase.colors import Color
from manabase.filter.parser import parse_filter_string
from manabase.filters.colors import (
    BasicLandReferencedFilter,
    ProducedManaFilter,
)
from manabase.filters.lands.battle import BattleLandFilter
from manabase.filters.lands.check import CheckLandFilter
from manabase.filters.lands.fetch import FetchLandFilter
from manabase.filters.lands.original import OriginalDualLandFilter
from manabase.filters.lands.reveal import RevealLandFilter
from manabase.filters.lands.shock import ShockLandFilter


def test_filter_parsing_simple():
    """Parse a single filter."""
    colors = [Color.white]
    string = "original"
    expected = OriginalDualLandFilter()

    assert parse_filter_string(string, colors) == expected


def test_filter_parsing_and():
    """Parse ANDed filters."""
    colors = [Color.white]
    string = "producer & original"
    expected = ProducedManaFilter(colors=colors) & OriginalDualLandFilter()

    assert parse_filter_string(string, colors) == expected


def test_filter_parsing_arguments():
    """Parse filters with arguments."""
    colors = [Color.white]
    string = "reference{0, 1}"
    expected = BasicLandReferencedFilter(
        colors=colors,
        exclusive=False,
        minimum_count=1,
    )

    assert parse_filter_string(string, colors) == expected


def test_filter_parsing_default_filters():
    """Parse a complex filter string."""
    colors = [Color.white]
    string = (
        "( producer & ( original | shock | battle | check | reveal ) ) "
        "| ( reference{0, 1} & fetch )"
    )

    expected = (
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

    assert parse_filter_string(string, colors) == expected


def test_filter_parsing_invert():
    """Parse a filter with invert operands.

    This test case is interesting because the invert (``~``) operand makes
    the shape of the filter string change.

    With the invert filter, there is no left arm around the operand.
    """
    colors = [Color.white]
    string = "~original"

    expected = ~OriginalDualLandFilter()

    assert parse_filter_string(string, colors) == expected


def test_filter_parsing_invert_complex():
    """Parse a filter mixing invert operands and normal ones."""
    colors = [Color.white]
    string = "(producer & (~original)) | fetch"

    expected = (
        ProducedManaFilter(colors=colors) & ~OriginalDualLandFilter()
    ) | FetchLandFilter()

    assert parse_filter_string(string, colors) == expected
