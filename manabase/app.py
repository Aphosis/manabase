"""CLI."""
from typing import Optional

import typer

from .cache import CacheManager
from .client import Client
from .colors import Color
from .filters.colors import BasicLandReferencedFilter, ProducedManaFilter
from .filters.lands.battle import BattleLandFilter
from .filters.lands.check import CheckLandFilter
from .filters.lands.fetch import FetchLandFilter
from .filters.lands.original import OriginalDualLandFilter
from .filters.lands.reveal import RevealLandFilter
from .filters.lands.shock import ShockLandFilter

manabase = typer.Typer()


@manabase.command()
def generate(
    colors: str,
    _count: int = 23,
    _maximum: int = 4,
    clear_cache: Optional[bool] = False,
):
    """Generate a manabase."""
    color_list = Color.from_string(colors)

    filters = (
        ProducedManaFilter(color_list)
        & (
            OriginalDualLandFilter()
            | ShockLandFilter()
            | BattleLandFilter()
            | CheckLandFilter()
            | RevealLandFilter()
        )
    ) | (
        BasicLandReferencedFilter(
            color_list,
            exclusive=False,
            minimum_count=1,
        )
        & FetchLandFilter()
    )

    cache = CacheManager()

    if clear_cache or not cache.has_cache():

        client = Client()

        # TODO: #5 Multithread that part, it takes longer than forever.
        models = client.fetch()

        cache.write_cache(models)

    else:
        models = cache.read_cache()

    # TODO: #1 Cache filtering results. It should be invalidated if the query
    # cache is invalidated.
    cards = set()
    for model in models:
        if not filters.filter_value(model):
            continue
        cards.add(model)

    print("\n".join([card.name for card in sorted(cards)]))


if __name__ == "__main__":
    manabase()
