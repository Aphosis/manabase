"""CLI."""
from typing import List, Optional

import typer

from .client import Client
from .colors import Color
from .cycles import Cycle
from .filters import CycleFilter, ProvideColorFilter

manabase = typer.Typer()


@manabase.command()
def generate(
    colors: str,
    _count: int = 23,
    _maximum: int = 4,
    ignore_colors: Optional[List[Cycle]] = None,
):
    """Generate a manabase."""
    color_list = Color.from_string(colors)

    cycles = Cycle.default()

    # TODO: Once land filters are actual filters, filters should return a list
    # of ``FilteredCard`` instead of simple ``Card``s.
    # This way, the next filter will know the filter that let the card in,
    # and can ignore the card, for example the ``ProvideColorFilter``
    # will ignore cards coming from a land filter with ``ignore_colors`` on.
    # HACK: Until then, we'll just pretend it works.
    filters = [
        ProvideColorFilter(*color_list),
        CycleFilter(color_list, cycles, ignore_colors),
    ]

    client = Client()

    cards = client.fetch(filters)

    print("\n".join([card.name for card in sorted(cards)]))


if __name__ == "__main__":
    manabase()
