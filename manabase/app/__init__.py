"""Manabase CLI."""
import os

import typer

from ..settings import UserSettings
from .cache import clear_cache
from .generate import generate
from .presets import app as presets

manabase = typer.Typer()

manabase.add_typer(presets, name="presets")

manabase.command()(generate)
manabase.command()(clear_cache)


@manabase.callback()
def main(ctx: typer.Context):
    """Landing rock solid mana bases for your decks.

    Manabase is a command-line tool that helps you generate a mana base for your
    Magic: The Gathering decks.

    It uses https://scryfall.com/ as its source of truth.
    """
    path = UserSettings.default_path()

    if os.path.isfile(path):
        settings = UserSettings.from_file(path)
    else:
        settings = UserSettings()

    ctx.obj = settings


__all__ = ["manabase"]
