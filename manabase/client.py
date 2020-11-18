"""Fetch data from [scryfall](https://scryfall.com/)."""
from typing import List, Optional, Tuple

import requests
from pydantic import ValidationError

from .cache import CacheManager
from .cards import Card
from .query import QueryBuilder


class Client:
    """A client for the scryfall API."""

    API_URL = "https://api.scryfall.com"

    def __init__(self, api_url: str = API_URL, cache: Optional[CacheManager] = None):
        self.api_url = api_url
        self.cache = cache

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

    def fetch(self, builder: QueryBuilder) -> List[Card]:
        """Fetch a filtered list of cards."""
        if self.cache and self.cache.has_cache(builder.type):
            return self.cache.read_cache(builder.type)

        query = builder.build()
        page = 1

        cards, has_next_page = self._fetch_cards(query, page)
        while has_next_page:
            page += 1
            # TODO: #6 Ensure we only call the API once every .1s at most.
            # This is to comply to Scryfall rate limiting.
            _models, has_next_page = self._fetch_cards(query, page)
            cards.extend(_models)

        if self.cache is not None:
            self.cache.write_cache(builder.type, cards)

        return cards

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
