# pylint: disable=missing-module-docstring, missing-function-docstring
from pathlib import Path

from manabase.settings import UserSettings


def test_default_path_works():
    UserSettings.default_path()


def test_save_creates_parent_dirs(fresh_settings: Path, tmp_path: Path):
    settings = UserSettings.from_file(fresh_settings)

    new_settings = tmp_path / "settings" / "settings.yml"
    settings.save(new_settings)
