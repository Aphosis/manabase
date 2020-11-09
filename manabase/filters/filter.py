"""Implements a filter tree using bitwise operators.

Filters can be chained together using bitwise operators.

Example::

```python
>>> from manabase.filters.filter import CompositeFilter
>>> class MoreThanTwo(CompositeFilter):
...     def filter_value(self, value: int) -> bool:
...         return value > 2
>>> class LessThanTen(CompositeFilter):
...     def filter_value(self, value: int) -> bool:
...         return value < 10
>>> filters = MoreThanTwo() & LessThanTen()
>>> list(filter(filters.filter_value, range(15)))
[3, 4, 5, 6, 7, 8, 9]
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from ..constructor import equals, represent


class Filter(metaclass=ABCMeta):
    """Filter than can be chained using bitwise operators.

    Example::
    ```python
    >>> from manabase.filters.filter import Filter
    >>> class MoreThanTwo(Filter):
    ...     def filter_value(self, value: int) -> bool:
    ...         return value > 2
    >>> class LessThanTen(Filter):
    ...     def filter_value(self, value: int) -> bool:
    ...         return value < 10
    >>> class AndOperator(Filter):
    ...     def __init__(self, left: Filter, right: Filter):
    ...         self.left = left
    ...         self.right = right
    ...     def filter_value(self, value: Any) -> bool:
    ...         left = self.left.filter_value(value)
    ...         if not left:
    ...             return False
    ...         right = self.right.filter_value(value)
    ...         return right
    >>> operator = AndOperator(MoreThanTwo(), LessThanTen())
    >>> operator.filter_value(1)
    False
    >>> operator.filter_value(5)
    True
    >>> operator.filter_value(12)
    False

    ```
    """

    @abstractmethod
    def filter_value(self, value: Any) -> bool:
        """Filter a single value.

        Example::

        ```python
        >>> from manabase.filters.filter import Filter
        >>> class MoreThanTwo(Filter):
        ...     def filter_value(self, value: int) -> bool:
        ...         return value > 2
        >>> filter_ = MoreThanTwo()
        >>> filter_.filter_value(2)
        False
        >>> filter_.filter_value(10)
        True

        ```
        """

    def __repr__(self) -> str:
        return represent(self)

    def __eq__(self, other: Filter) -> bool:
        return equals(self, other)


class CompositeFilter(Filter, metaclass=ABCMeta):
    """A filter that can be chained to other filters using bitwise operators."""

    def __and__(self, other: CompositeFilter) -> CompositeFilter:
        return AndOperator(self, other)

    def __or__(self, other: CompositeFilter) -> CompositeFilter:
        return OrOperator(self, other)

    def __xor__(self, other: CompositeFilter) -> CompositeFilter:
        return XorOperator(self, other)

    def __invert__(self) -> CompositeFilter:
        return InvertOperator(self)


class AndOperator(CompositeFilter):
    """An ``and`` operator.

    The two filters should return ``True`` to let the value through.
    """

    def __init__(self, left: CompositeFilter, right: CompositeFilter):
        self.left = left
        self.right = right

    def filter_value(self, value: Any) -> bool:
        left = self.left.filter_value(value)
        if not left:
            return False
        right = self.right.filter_value(value)
        return right


class OrOperator(CompositeFilter):
    """An ``or`` operator.

    At least one of the two filters should return ``True`` to let the value through.
    """

    def __init__(self, left: CompositeFilter, right: CompositeFilter):
        self.left = left
        self.right = right

    def filter_value(self, value: Any) -> bool:
        left = self.left.filter_value(value)
        if left:
            return True
        right = self.right.filter_value(value)
        return right


class XorOperator(CompositeFilter):
    """An ``xor`` operator.

    Exactly one of the two filters should return ``True`` to let the value through.
    """

    def __init__(self, left: CompositeFilter, right: CompositeFilter):
        self.left = left
        self.right = right

    def filter_value(self, value: Any) -> bool:
        left = self.left.filter_value(value)
        right = self.right.filter_value(value)
        return left.__xor__(right)


class InvertOperator(CompositeFilter):
    """A ``not`` operator.

    Reverses the value of the filter.
    """

    def __init__(self, leaf: CompositeFilter):
        self.leaf = leaf

    def filter_value(self, value: Any) -> bool:
        return not self.leaf.filter_value(value)
