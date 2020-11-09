"""Test `CompositeFilter`."""
# pylint: disable=no-self-use, missing-function-docstring
from manabase.filters.composite import CompositeFilter


class LessThan(CompositeFilter):
    """Filters integer values strictly under ``maximum``."""

    def __init__(self, maximum: int) -> None:
        self.maximum = maximum

    def filter_value(self, value: int) -> bool:
        return value < self.maximum


class MoreThan(CompositeFilter):
    """Filters integer values strictly over ``minimum``."""

    def __init__(self, minimum: int) -> None:
        self.minimum = minimum

    def filter_value(self, value: int) -> bool:
        return value > self.minimum


def test_composite_filter_and():
    filter_ = MoreThan(2) & LessThan(10)

    assert not filter_.filter_value(1)
    assert filter_.filter_value(5)
    assert not filter_.filter_value(11)


def test_composite_filter_or():
    filter_ = MoreThan(10) | LessThan(2)

    assert filter_.filter_value(1)
    assert not filter_.filter_value(5)
    assert filter_.filter_value(11)


def test_composite_filter_xor():
    filter_ = MoreThan(10) ^ MoreThan(2)

    assert not filter_.filter_value(1)
    assert filter_.filter_value(5)
    assert not filter_.filter_value(11)


def test_composite_filter_invert():
    filter_ = ~MoreThan(10)

    assert filter_.filter_value(1)
    assert not filter_.filter_value(11)
