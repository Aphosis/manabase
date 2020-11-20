# pylint: disable=missing-module-docstring, missing-function-docstring
from pathlib import Path

from typer.testing import CliRunner

from manabase.app import app

runner = CliRunner()


def test_new(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'Created preset "default".\n'

    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'Preset "default" already exists.\n'


def test_use(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "use", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'No preset named "default".\n'

    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )
    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default2"],
    )
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "use", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'Active preset is now "default".\n'

    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "use", "default"],
    )
    assert result.exit_code == 0
    assert result.stdout == '"default" is already the active preset.\n'


def test_active(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "active"],
    )

    assert result.exit_code == 0
    assert result.stdout == "There is no active preset.\n"

    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "active"],
    )

    assert result.exit_code == 0
    assert result.stdout == "default\n"


def test_list(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "list"],
    )

    assert result.exit_code == 0
    assert result.stdout == (
        "No preset saved. Create one with " "`manabase presets new`.\n"
    )

    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )
    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default2"],
    )
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "list"],
    )

    assert result.exit_code == 0
    assert result.stdout == "- default\n- default2\n"


def test_show(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "show", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'No preset named "default".\n'

    runner.invoke(
        app,
        [
            f"--config={fresh_settings}",
            "presets",
            "new",
            "default",
            "--lands=37",
            "--occurrences=1",
        ],
    )
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "show", "default"],
    )
    assert result.exit_code == 0
    assert result.stdout == "default\n- lands: 37\n- occurrences: 1\n"


def test_update(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "update", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'No preset named "default".\n'

    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "update", "default", "--lands=37"],
    )
    assert result.exit_code == 0
    assert result.stdout == 'Updated preset "default".\n'


def test_patch(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "patch", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'No preset named "default".\n'

    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default", "--lands=37"],
    )
    result = runner.invoke(
        app,
        [
            f"--config={fresh_settings}",
            "presets",
            "patch",
            "default",
            "--filters=original",
            "--lands=4",
            "--occurrences=1",
            "--priorities=original",
            "--filler-weights=1 3 4",
            "--rocks=5",
            "--rock-filters=signet | talisman",
            "--rock-priorities=talisman",
        ],
    )
    assert result.exit_code == 0
    assert result.stdout == 'Patched preset "default".\n'


def test_delete(fresh_settings: Path):
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "delete", "default"],
    )

    assert result.exit_code == 0
    assert result.stdout == 'No preset named "default".\n'

    runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "new", "default"],
    )
    result = runner.invoke(
        app,
        [f"--config={fresh_settings}", "presets", "delete", "default"],
    )
    assert result.exit_code == 0
    assert result.stdout == 'Deleted preset "default".\n'
