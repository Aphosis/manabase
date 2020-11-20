# pylint: disable=missing-module-docstring, missing-function-docstring
import os

import toml

from manabase import __version__


def test_version():
    root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root, "pyproject.toml")

    package = toml.load(path)

    assert __version__ == package["tool"]["poetry"]["version"]
