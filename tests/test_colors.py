# pylint: disable=missing-module-docstring, missing-function-docstring
from manabase.colors import Color


def test_color_from_string():
    colors = "wub"
    expected_colors = [Color.white, Color.blue, Color.black]

    assert Color.from_string(colors) == expected_colors


def test_color_from_string_single():
    colors = "w"
    expected_colors = [Color.white]

    assert Color.from_string(colors) == expected_colors


def test_color_from_string_all():
    colors = "wubrg"
    expected_colors = [Color.white, Color.blue, Color.black, Color.red, Color.green]

    assert Color.from_string(colors) == expected_colors


def test_color_from_string_upper_case():
    colors = "WUBRG"
    expected_colors = [Color.white, Color.blue, Color.black, Color.red, Color.green]

    assert Color.from_string(colors) == expected_colors
