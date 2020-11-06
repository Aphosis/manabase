from __future__ import annotations

from typing import List
from enum import Enum


class Color(Enum):
    white = "W"
    blue = "U"
    black = "B"
    red = "R"
    green = "G"

    @classmethod
    def from_string(cls, colors: str) -> List[Color]:
        return [Color(color.upper()) for color in colors]
