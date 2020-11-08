"""Fetch data from [scryfall](https://scryfall.com/)."""
from typing import List, Tuple

import requests
from pydantic import ValidationError

from .cards import Card
from .filters.filter import Filter


class Client:
    """A client for the scryfall API."""

    API_URL = "https://api.scryfall.com"

    def __init__(self, api_url: str = API_URL):
        self.api_url = api_url

    def route(self, path: str) -> str:
        """Build an URL endpoint from a relative path.

        Example::

        ```python
        >>> from manabase.client import Client
        >>> client = Client()
        >>> client.route("cards/search")
        'https://api.scryfall.com/cards/search'
        """
        return "/".join([self.api_url, path])

    def fetch(self, filters: Filter) -> List[Card]:
        """Fetch a filtered list of cards."""
        query = "t:land"
        page = 1

        models, has_next_page = self._fetch_cards(query, page)
        while has_next_page:
            page += 1
            _models, has_next_page = self._fetch_cards(query, page)
            models.extend(_models)

        cards = set()
        for model in models:
            if not filters.filter_value(model):
                continue
            cards.add(model)

        return list(cards)

    def _fetch_cards(self, query: str, page: int) -> Tuple[List[Card], bool]:
        params = {"q": query, "page": page}
        response = requests.get(self.route("cards/search"), params=params)
        cards = response.json()
        models = []

        for data in cards["data"]:

            if "produced_mana" not in data:
                # Fetch lands don't have the ``produced_mana`` field.
                data.update({"produced_mana": []})

            try:
                model = Card(**data)
            except ValidationError:
                continue

            models.append(model)

        return models, cards["has_more"]