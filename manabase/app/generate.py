"""CLI."""
# pylint: disable=too-many-arguments
from typing import Callable, List, Optional

import typer

from ..cache import CacheManager
from ..cards import CardList
from ..client import Client
from ..colors import Color
from ..defaults import (
    default_land_filters,
    default_land_priorities,
    default_rock_filters,
    default_rock_priorities,
)
from ..filler.distribution import WeightedDistribution
from ..filler.filler import BasicLandFiller
from ..filter.data import FilterAlias
from ..filter.manager import FilterManager
from ..filters.composite import CompositeFilter
from ..formatter import Formatter, Output
from ..generator import ListGenerator
from ..priorities import PriorityManager
from ..query import QueryBuilder
from ..settings import UserSettings

LANDS_DEFAULT = 23
OCCURRENCES_DEFAULT = 4


def generate(  # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, line-too-long
    ctx: typer.Context,
    colors: str,
    filters: Optional[str] = None,
    lands: Optional[int] = None,
    occurrences: Optional[int] = None,
    priorities: Optional[str] = None,
    filler_weights: Optional[str] = None,
    rocks: Optional[int] = None,
    rock_filters: Optional[str] = None,
    rock_priorities: Optional[str] = None,
):
    """Generate a manabase."""
    settings: UserSettings = ctx.obj.settings
    cache: CacheManager = ctx.obj.cache

    if settings.active and settings.active in settings.presets:
        preset = settings.presets[settings.active]

        if filters is None:
            filters = preset.filters
        if lands is None:
            lands = preset.lands
        if occurrences is None:
            occurrences = preset.occurrences
        if priorities is None:
            priorities = preset.priorities
        if filler_weights is None:
            filler_weights = preset.filler_weights
        if rocks is None:
            rocks = preset.rocks
        if rock_filters is None:
            rock_filters = preset.rock_filters
        if rock_priorities is None:
            rock_priorities = preset.rock_priorities

    if lands is None:
        lands = LANDS_DEFAULT
    if occurrences is None:
        occurrences = OCCURRENCES_DEFAULT

    color_list = Color.from_string(colors)

    client = Client(cache=cache)

    # TODO: #12 Support more formatting options.
    formatter = Formatter(output=Output.list)

    if rocks is not None and rocks > 0:
        rock_list = generate_rocks(
            rock_filters,
            rock_priorities,
            rocks,
            occurrences,
            color_list,
            client,
        )
        typer.echo("// Rocks")
        typer.echo(formatter.format_cards(rock_list))

    if lands > 0:
        land_list = generate_lands(
            filters,
            priorities,
            lands,
            occurrences,
            filler_weights,
            color_list,
            client,
        )
        typer.echo("// Lands")
        typer.echo(formatter.format_cards(land_list))


def generate_rocks(
    filter_string: Optional[str],
    priority_string: Optional[str],
    rocks: int,
    occurrences: int,
    colors: List[Color],
    client: Client,
) -> CardList:
    """Generate the lands card list."""
    filter_manager = _parse_filters(filter_string, colors, default_rock_filters)
    priority_manager = _parse_priorities(
        priority_string,
        rocks,
        occurrences,
        default_rock_priorities,
    )

    query = QueryBuilder(type="artifact")

    generator = ListGenerator(
        filters=filter_manager,
        priorities=priority_manager,
        query=query,
        filler=None,
    )

    return generator.generate(client)


def generate_lands(
    filter_string: Optional[str],
    priority_string: Optional[str],
    lands: int,
    occurrences: int,
    weights: Optional[str],
    colors: List[Color],
    client: Client,
) -> CardList:
    """Generate the lands card list."""
    filter_manager = _parse_filters(filter_string, colors, default_land_filters)
    priority_manager = _parse_priorities(
        priority_string,
        lands,
        occurrences,
        default_land_priorities,
    )

    query = QueryBuilder(type="land")

    distribution = _parse_weights(weights, occurrences, len(colors))

    filler = BasicLandFiller(distribution=distribution, colors=colors)

    generator = ListGenerator(
        filters=filter_manager,
        priorities=priority_manager,
        query=query,
        filler=filler,
    )

    return generator.generate(client)


def _parse_filters(
    filter_string: Optional[str],
    colors: List[Color],
    defaults: Callable[[List[Color]], CompositeFilter],
) -> FilterManager:
    if filter_string is not None:
        return FilterManager.from_string(filter_string, colors)
    return FilterManager(colors=colors, filters=defaults(colors))


def _parse_priorities(
    priority_string: Optional[str],
    maximum: int,
    occurrences: int,
    defaults: Callable[[], List[FilterAlias]],
) -> PriorityManager:
    if priority_string is not None:
        return PriorityManager.from_string(
            priority_string,
            maximum,
            occurrences,
        )
    return PriorityManager(
        maximum=maximum,
        occurrences=occurrences,
        priorities=defaults(),
    )


def _parse_weights(
    weights: Optional[str],
    maximum: int,
    count: int,
) -> WeightedDistribution:
    if weights is not None:
        weights_ = [int(weight) for weight in weights.split()]
    else:
        weights_ = [1] * count

    return WeightedDistribution(
        maximum=maximum,
        weights=weights_,
    )
