"""Cache management."""
import typer

from ..cache import CacheManager


def clear_cache():
    """Clear the cache."""
    cache = CacheManager()
    cache.clear()

    typer.echo(typer.style("Cache cleared.", fg=typer.colors.GREEN))
