"""Card list generator."""
from pydantic import BaseModel

from manabase.client import Client
from manabase.filter.manager import FilterManager

from .cards import CardList
from .filler.filler import ListFiller
from .priorities import PriorityManager
from .query import QueryBuilder


class ListGenerator(BaseModel):
    """Generates a list of cards from a query, filters, priorities and filler cards."""

    filters: FilterManager
    priorities: PriorityManager
    query: QueryBuilder
    filler: ListFiller

    def generate(self, client: Client) -> CardList:
        """Generate the list of cards."""
        cards = client.fetch(self.query)

        # TODO: #1 Cache filtering results. It should be invalidated if the query
        # cache is invalidated.
        results = self.filters.filter_cards(cards)

        card_list = self.priorities.build_list(results)

        if card_list.available:
            filler_list = self.filler.generate_filler(card_list.available)
            card_list.update(filler_list)

        return card_list
