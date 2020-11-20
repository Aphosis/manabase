"""Generation presets management."""
from __future__ import annotations

import os
from typing import Dict, Optional

import yaml
from appdirs import user_config_dir
from pydantic import BaseModel, BaseSettings

from . import __app_name__, __version__

DEFAULT_CONFIG = "manabase.yml"


class GenerationPreset(BaseModel):
    """A `generate` command preset."""

    name: str
    filters: Optional[str] = None
    lands: Optional[int] = None
    occurrences: Optional[int] = None
    priorities: Optional[str] = None
    filler_weights: Optional[str] = None
    rocks: Optional[int] = None
    rock_filters: Optional[str] = None
    rock_priorities: Optional[str] = None


class UserSettings(BaseSettings):
    """Application user settings."""

    presets: Dict[str, GenerationPreset] = {}
    active: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        env_prefix = "manabase_"

    @classmethod
    def from_file(cls, path: str) -> UserSettings:
        """Read settings from a YAML file."""
        with open(path) as handle:
            data = yaml.safe_load(handle)
        return cls(**data)

    @staticmethod
    def default_path() -> str:
        """Return the default configuration path."""
        return os.path.join(
            user_config_dir(__app_name__, version=__version__), DEFAULT_CONFIG
        )

    def save(self, path: Optional[str] = None):
        """Save settings to file.

        If no file path is provided, saves to `UserSettings.default_path`.
        """
        path = path or self.default_path()

        parent = os.path.dirname(path)
        if not os.path.isdir(parent):
            os.makedirs(parent)

        with open(path, "w") as handle:
            yaml.safe_dump(self.dict(), handle)
