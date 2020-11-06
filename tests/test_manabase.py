# pylint: disable=missing-module-docstring, missing-function-docstring
from manabase import __version__


def test_version():
    assert __version__ == "0.1.0"
