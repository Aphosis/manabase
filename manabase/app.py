"""CLI."""
import typer

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

    client = Client()

    # TODO: Cache the query results, it takes forever.
    # TODO: Split data fetching from scryfall and filtering, `Client.fetch`
    # should not do both. `Client` should not know about filters.
    # TODO: Profile filtering. It currently tales forever, probably due to
    # un-compiled regexes being used a pretty high number of times.
    # TODO: Cache filtering results. It should be invalidated if the query
    # cache is invalidated.
    cards = client.fetch(filters)

    print("\n".join([card.name for card in sorted(cards)]))


if __name__ == "__main__":
    manabase()
