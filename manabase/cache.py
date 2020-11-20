"""Handles request cards caching."""
from pathlib import Path
from typing import List, Optional

from appdirs import user_cache_dir
from diskcache import Index
from pydantic.main import BaseModel

from . import __app_name__, __version__
from .cards import Card
from .query import QueryType


class CacheManager(BaseModel):
    """Manages card cache."""

    path: Path
    _index: Index

    class Config:  # pylint: disable=missing-class-docstring
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True

    def __init__(self, path: Optional[Path] = None) -> None:
        path = path or CacheManager.default_path()

        super().__init__(path=path)

        self._index = self._create_index()

    @staticmethod
    def default_path() -> Path:
        """Return a default cache directory"""
        return Path(user_cache_dir(__app_name__, version=__version__))

    def _create_index(self) -> Index:
        """Create a disk index."""
        index = Index(str(self.path))
        return index

    def has_cache(self, query: QueryType) -> bool:
        """Return ``True`` if ``index`` has a card cache."""
        try:
            self._index[query]
        except KeyError:
            return False
        return True

    def write_cache(self, query: QueryType, cards: List[Card]):
        """Write cards to the local cache."""
        self._index.update({query: cards})

    def read_cache(self, query: QueryType) -> List[Card]:
        """Read cards from the local cache."""
        return self._index.get(query, [])

    def clear(self):
        """Clear the cache."""
        self._index.clear()
