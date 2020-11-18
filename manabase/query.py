"""Scryfall queries."""
from enum import Enum

from pydantic import BaseModel


class QueryType(Enum):
    """Type of queries available."""

    land = "land"
    artifact = "artifact"


class QueryBuilder(BaseModel):
    """Builds a scryfall query string."""

    type: QueryType

    def build(self) -> str:
        """Build the query string."""
        return f"t:{self.type.value}"
