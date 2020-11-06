def test_color_from_string():
    from manabase.colors import Color

    colors = "wub"
    expected_colors = [Color.white, Color.blue, Color.black]

    assert Color.from_string(colors) == expected_colors


def test_color_from_string_single():
    from manabase.colors import Color

    colors = "w"
    expected_colors = [Color.white]

    assert Color.from_string(colors) == expected_colors


def test_color_from_string_all():
    from manabase.colors import Color

    colors = "wubrg"
    expected_colors = [Color.white, Color.blue, Color.black, Color.red, Color.green]

    assert Color.from_string(colors) == expected_colors


def test_color_from_string_upper_case():
    from manabase.colors import Color

    colors = "WUBRG"
    expected_colors = [Color.white, Color.blue, Color.black, Color.red, Color.green]

    assert Color.from_string(colors) == expected_colors
