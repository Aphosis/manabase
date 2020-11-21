# pylint: disable=missing-module-docstring, missing-function-docstring
from pathlib import Path

from typer.testing import CliRunner

from manabase.app import app

runner = CliRunner()


def test_generate_default(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "generate", "WUB"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Lands\n"
        "1 Arid Mesa\n"
        "1 Bloodstained Mire\n"
        "1 Flooded Strand\n"
        "1 Marsh Flats\n"
        "1 Misty Rainforest\n"
        "1 Polluted Delta\n"
        "1 Scalding Tarn\n"
        "1 Verdant Catacombs\n"
        "1 Windswept Heath\n"
        "1 Scrubland\n"
        "1 Tundra\n"
        "1 Underground Sea\n"
        "1 Godless Shrine\n"
        "1 Hallowed Fountain\n"
        "1 Watery Grave\n"
        "1 Prairie Stream\n"
        "1 Sunken Hollow\n"
        "1 Drowned Catacomb\n"
        "1 Glacial Fortress\n"
        "1 Isolated Chapel\n"
        "1 Choked Estuary\n"
        "1 Port Town\n"
        "5 Plains\n"
        "5 Island\n"
        "5 Swamp\n"
    )


def test_generate_filters(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "generate", "--filters=original", "WUB"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Lands\n"
        "1 Badlands\n"
        "1 Bayou\n"
        "1 Plateau\n"
        "1 Savannah\n"
        "1 Scrubland\n"
        "1 Taiga\n"
        "1 Tropical Island\n"
        "1 Tundra\n"
        "1 Underground Sea\n"
        "1 Volcanic Island\n"
        "9 Plains\n"
        "9 Island\n"
        "9 Swamp\n"
    )


def test_generate_lands(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "generate", "--lands=10", "WUB"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Lands\n"
        "1 Arid Mesa\n"
        "1 Bloodstained Mire\n"
        "1 Flooded Strand\n"
        "1 Marsh Flats\n"
        "1 Misty Rainforest\n"
        "1 Polluted Delta\n"
        "1 Scalding Tarn\n"
        "1 Verdant Catacombs\n"
        "1 Windswept Heath\n"
        "1 Scrubland\n"
    )


def test_generate_occurrences(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "generate", "--occurrences=4", "WUB"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Lands\n"
        "4 Arid Mesa\n"
        "4 Bloodstained Mire\n"
        "4 Flooded Strand\n"
        "4 Marsh Flats\n"
        "4 Misty Rainforest\n"
        "4 Polluted Delta\n"
        "4 Scalding Tarn\n"
        "4 Verdant Catacombs\n"
        "4 Windswept Heath\n"
        "1 Scrubland\n"
    )


def test_generate_priorities(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "generate", "--priorities=shock", "WUB"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Lands\n"
        "1 Godless Shrine\n"
        "1 Hallowed Fountain\n"
        "1 Watery Grave\n"
        "1 Arid Mesa\n"
        "1 Bloodstained Mire\n"
        "1 Choked Estuary\n"
        "1 Drowned Catacomb\n"
        "1 Flooded Strand\n"
        "1 Glacial Fortress\n"
        "1 Isolated Chapel\n"
        "1 Marsh Flats\n"
        "1 Misty Rainforest\n"
        "1 Polluted Delta\n"
        "1 Port Town\n"
        "1 Prairie Stream\n"
        "1 Scalding Tarn\n"
        "1 Scrubland\n"
        "1 Sunken Hollow\n"
        "1 Tundra\n"
        "1 Underground Sea\n"
        "1 Verdant Catacombs\n"
        "1 Windswept Heath\n"
        "5 Plains\n"
        "5 Island\n"
        "5 Swamp\n"
    )


def test_generate_filler_weights(fresh_settings: Path):
    # TODO: Once we have a custom list for tests, we could
    # avoid using another option to filter the land list.
    result = runner.invoke(
        app,
        [
            f"--config={fresh_settings}",
            "generate",
            "--filters=shock & producer",
            "--occurrences=1",
            "--filler-weights=1 3 1",
            "WUB",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Lands\n"
        "1 Godless Shrine\n"
        "1 Hallowed Fountain\n"
        "1 Watery Grave\n"
        "7 Plains\n"
        "21 Island\n"
        "6 Swamp\n"
    )


def test_generate_rocks(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "generate", "--lands=0", "--rocks=5", "WUB"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Rocks\n"
        "1 Azorius Signet\n"
        "1 Dimir Signet\n"
        "1 Orzhov Signet\n"
        "1 Talisman of Dominance\n"
        "1 Talisman of Hierarchy\n"
    )


def test_generate_rock_filters(fresh_settings: Path):
    result = runner.invoke(
        app,
        [
            f"--config={fresh_settings}",
            "generate",
            "--lands=0",
            "--rocks=5",
            "--rock-filters=obelisk | crystal",
            "WUB",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Rocks\n"
        "1 Indatha Crystal\n"
        "1 Ketria Crystal\n"
        "1 Raugrin Crystal\n"
        "1 Savai Crystal\n"
        "1 Zagoth Crystal\n"
    )


def test_generate_rock_priorities(fresh_settings: Path):
    result = runner.invoke(
        app,
        [
            f"--config={fresh_settings}",
            "generate",
            "--lands=0",
            "--rocks=5",
            "--rock-priorities=obelisk",
            "WUB",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Rocks\n"
        "1 Obelisk of Esper\n"
        "1 Azorius Signet\n"
        "1 Dimir Signet\n"
        "1 Orzhov Signet\n"
        "1 Talisman of Dominance\n"
    )


def test_generate_preset(fixtures_dir: Path):
    settings = fixtures_dir / "setting-with-preset.yml"

    result = runner.invoke(
        app,
        [
            f"--config={settings}",
            "generate",
            "WUB",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "// Rocks\n"
        "1 Obelisk of Esper\n"
        "// Lands\n"
        "1 Scrubland\n"
        "1 Tundra\n"
        "1 Underground Sea\n"
        "1 Godless Shrine\n"
        "1 Hallowed Fountain\n"
        "1 Watery Grave\n"
        "7 Plains\n"
        "19 Island\n"
        "5 Swamp\n"
    )
