"""CLI."""
from typing import Optional

import typer

from .cache import CacheManager
from .client import Client
from .colors import Color
from .filter.manager import FilterManager

manabase = typer.Typer()


@manabase.command()
def generate(
    colors: str,
    filters: Optional[str] = None,
    _count: int = 23,
    _maximum: int = 4,
    clear_cache: Optional[bool] = False,
):
    """Generate a manabase."""
    # TODO: #7 Take ``count`` and ``maximum`` into account.
    # TODO: #8 Find a more meaningful name for ``maximum``, i.e --land-occurrences.
    # TODO: #9 Rename ``count`` to ``lands`` as we aim to support mana rocks.
    # TODO: #10 Manage priorities when reaching the lands limit.
    color_list = Color.from_string(colors)

    if filters is not None:
        filter_manager = FilterManager.from_string(filters, color_list)
    else:
        filter_manager = FilterManager.default(color_list)

    cache = CacheManager()

    if clear_cache or not cache.has_cache():

        client = Client()

        # TODO: #5 Multithread that part, it takes longer than forever.
        cards = client.fetch()

        cache.write_cache(cards)

    else:
        cards = cache.read_cache()

    # TODO: #1 Cache filtering results. It should be invalidated if the query
    # cache is invalidated.
    filtered_cards = filter_manager.filter_cards(cards)

    # TODO: #12 Support more formatting options.
    print("\n".join([card.name for card in sorted(filtered_cards)]))


if __name__ == "__main__":
    manabase()
