"""Test utilities."""
from pathlib import Path
from typing import Callable, Iterator

import pytest

from manabase.cards import Card


@pytest.fixture(scope="session")
def make_card() -> Callable[..., Card]:
    """Create a card with default values.

    Specify any field to override by keyword argument.
    """

    def inner(**data):
        default = {
            "name": "",
            "oracle_text": "",
            "colors": [],
            "color_identity": [],
            "produced_mana": [],
            "legalities": {},
            "textless": False,
            "scryfall_uri": "",
            "set": "",
        }
        default.update(data)
        return Card(**default)

    return inner


@pytest.fixture()
def fresh_settings(tmp_path: Path) -> Iterator[Path]:
    """Provides a default settings file path."""
    path = tmp_path / "manabase.yml"

    path.write_text("active: null\npresets: []")

    yield path


@pytest.fixture()
def cache(tmp_path: Path) -> Iterator[Path]:
    """Provides a default cache file path."""
    path = tmp_path / "cache"

    yield path


@pytest.fixture()
def fixtures_dir() -> Iterator[Path]:
    """Provides the path to the fixtures (data) directory."""
    yield Path(__file__).parent / "fixtures"
