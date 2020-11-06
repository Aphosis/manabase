"""Color definitions.

Colors are defined as an enum for convenience.

It can be parsed from a string of color identifiers using the `Color.from_string`
method.

Example::

```python
>>> from manabase.colors import Color
>>> Color.from_string("w")
[<Color.white: 'W'>]

```

This method is case insensitive to work with most APIs by default.

Example::

```python
>>> from manabase.colors import Color
>>> Color.from_string("wUb")
[<Color.white: 'W'>, <Color.blue: 'U'>, <Color.black: 'B'>]

```
"""
from __future__ import annotations

from enum import Enum
from typing import List


class Color(Enum):
    """Definition of all possible colors."""

    white = "W"
    blue = "U"
    black = "B"
    red = "R"
    green = "G"

    @classmethod
    def from_string(cls, colors: str) -> List[Color]:
        """Generate a list of `Color` from a string of color identifiers.

        Color identifiers are single letters corresponding to a color.

        A string of color identifiers is any string containing one or more
        of these letters, in any order, for example ``"wub"``

        Methods manipulating these strings are case insensitive, to work
        with most APIs.

        Colors are identified by the following letters:

            - White: ``w``
            - Blue: ``u``
            - Black: ``b``
            - Red: ``r``
            - Green: ``g``
        """
        return [Color(color.upper()) for color in colors]
