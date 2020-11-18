"""CLI."""
from typing import Optional

import typer

from manabase.filler.distribution import WeightedDistribution
from manabase.filler.filler import BasicLandFiller
from manabase.generator import ListGenerator
from manabase.query import QueryBuilder

from .cache import CacheManager
from .client import Client
from .colors import Color
from .filter.manager import FilterManager
from .priorities import PriorityManager

manabase = typer.Typer()


@manabase.command()
def generate(  # pylint: disable=too-many-arguments, too-many-locals
    colors: str,
    filters: Optional[str] = None,
    lands: int = 23,
    occurrences: int = 4,
    priorities: Optional[str] = None,
    clear_cache: Optional[bool] = False,
    filler_weights: Optional[str] = None,
):
    """Generate a manabase."""
    color_list = Color.from_string(colors)

    if filters is not None:
        filter_manager = FilterManager.from_string(filters, color_list)
    else:
        filter_manager = FilterManager.default(color_list)

    if priorities is not None:
        priority_manager = PriorityManager.from_string(
            priorities,
            lands,
            occurrences,
        )
    else:
        priority_manager = PriorityManager.default(
            lands,
            occurrences,
        )

    cache = None if clear_cache else CacheManager()
    client = Client(cache=cache)

    land_query = QueryBuilder(type="land")

    land_weights = [int(w) for w in filler_weights.split()] or [1] * len(color_list)
    land_distribution = WeightedDistribution(
        maximum=occurrences,
        weights=land_weights,
    )
    land_filler = BasicLandFiller(distribution=land_distribution, colors=color_list)

    generator = ListGenerator(
        filters=filter_manager,
        priorities=priority_manager,
        query=land_query,
        filler=land_filler,
    )

    card_list = generator.generate(client)

    # TODO: #12 Support more formatting options.
    print("\n".join([f"{card.occurrences} {card.name}" for card in card_list.entries]))


if __name__ == "__main__":
    manabase()
