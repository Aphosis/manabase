# pylint: disable=missing-module-docstring, missing-function-docstring
from manabase.colors import Color
from manabase.cycles import (
    BattleLandFilter,
    BondLandFilter,
    BounceLandFilter,
    CheckLandFilter,
    CyclingLandFilter,
    FastLandFilter,
    FetchLandFilter,
    FilterLandFilter,
    HorizonLandFilter,
    OriginalDualLandFilter,
    PainLandFilter,
    RevealLandFilter,
    ScryLandFilter,
    ShockLandFilter,
)


def test_original_dual_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = OriginalDualLandFilter(colors)

    data = {
        "oracle_text": "({T}: Add {W} or {U}.)",
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "oracle_text": "({T}: Add {W} or {U}.)\nSome text.",
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_pain_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = PainLandFilter(colors)

    data = {
        "name": "Adarkar Wastes",
        "oracle_text": (
            "{T}: Add {C}.\n{T}: Add {W} or {U}. "
            "Adarkar Wastes deals 1 damage to you."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "oracle_text": (
            "{T}: Add {C}.\n{T}: Add {W} or {U}. "
            "Adarkar Wastes deals 1 damage to you."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_fetch_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = FetchLandFilter(colors)

    data = {
        "name": "Flooded Strand",
        "oracle_text": (
            "{T}, Pay 1 life, Sacrifice Flooded Strand: "
            "Search your library for a Plains or Island card, put it "
            "onto the battlefield, then shuffle your library."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Flooded Strand",
        "oracle_text": (
            "{T}, Pay 1 life, Sacrifice Flooded Strand: "
            "Search your library for a Plains or Island card, put it "
            "onto the battlefield, then shuffle your library."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_filter_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = FilterLandFilter(colors)

    data = {
        "oracle_text": "{1}, {T}: Add {W}{U}.",
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "oracle_text": "{1}, {T}: Add {W}{U}.\nSome text.",
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_bounce_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = BounceLandFilter(colors)

    data = {
        "name": "Dimir Aqueduct",
        "oracle_text": (
            "Dimir Aqueduct enters the battlefield tapped.\n"
            "When Dimir Aqueduct enters the battlefield, return a land "
            "you control to its owner's hand.\n"
            "{T}: Add {U}{B}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Dimir Aqueduct",
        "oracle_text": (
            "Dimir Aqueduct enters the battlefield tapped.\n"
            "When Dimir Aqueduct enters the battlefield, return a land "
            "you control to its owner's hand.\n"
            "{T}: Add {U}{B}.\nSome text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_shock_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = ShockLandFilter(colors)

    data = {
        "name": "Hallowed Fountain",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "As Hallowed Fountain enters the battlefield, you may pay 2 life. "
            "If you don't, it enters the battlefield tapped."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Hallowed Fountain",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "As Hallowed Fountain enters the battlefield, you may pay 2 life. "
            "If you don't, it enters the battlefield tapped.\nSome text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_horizon_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = HorizonLandFilter(colors)

    data = {
        "name": "Silent Clearing",
        "oracle_text": (
            "{T}, Pay 1 life: Add {W} or {B}.\n"
            "{1}, {T}, Sacrifice Silent Clearing: Draw a card."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Silent Clearing",
        "oracle_text": (
            "{T}, Pay 1 life: Add {W} or {B}.\n"
            "{1}, {T}, Sacrifice Silent Clearing: Draw a card."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_scry_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = ScryLandFilter(colors)

    data = {
        "name": "Temple of Enlightenment",
        "oracle_text": (
            "Temple of Enlightenment enters the battlefield tapped.\n"
            "When Temple of Enlightenment enters the battlefield, scry 1. "
            "(Look at the top card of your library. You may put that card "
            "on the bottom of your library.)\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Temple of Enlightenment",
        "oracle_text": (
            "Temple of Enlightenment enters the battlefield tapped.\n"
            "When Temple of Enlightenment enters the battlefield, scry 1. "
            "(Look at the top card of your library. You may put that card "
            "on the bottom of your library.)\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_battle_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = BattleLandFilter(colors)

    data = {
        "name": "Prairie Stream",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Prairie Stream enters the battlefield tapped unless you control "
            "two or more basic lands."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Prairie Stream",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Prairie Stream enters the battlefield tapped unless you control "
            "two or more basic lands."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_check_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = CheckLandFilter(colors)

    data = {
        "name": "Glacial Fortress",
        "oracle_text": (
            "Glacial Fortress enters the battlefield tapped unless you control "
            "a Plains or an Island.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Glacial Fortress",
        "oracle_text": (
            "Glacial Fortress enters the battlefield tapped unless you control "
            "a Plains or an Island.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_fast_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = FastLandFilter(colors)

    data = {
        "name": "Seachrome Coast",
        "oracle_text": (
            "Seachrome Coast enters the battlefield tapped unless you control "
            "two or fewer other lands.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Seachrome Coast",
        "oracle_text": (
            "Seachrome Coast enters the battlefield tapped unless you control "
            "two or fewer other lands.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_reveal_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = RevealLandFilter(colors)

    data = {
        "name": "Port Town",
        "oracle_text": (
            "As Port Town enters the battlefield, you may reveal a "
            "Plains or Island card from your hand. If you don't, "
            "Port Town enters the battlefield tapped.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Port Town",
        "oracle_text": (
            "As Port Town enters the battlefield, you may reveal a "
            "Plains or Island card from your hand. If you don't, "
            "Port Town enters the battlefield tapped.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_cycling_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = CyclingLandFilter(colors)

    data = {
        "name": "Irrigated Farmland",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Irrigated Farmland enters the battlefield tapped.\n"
            "Cycling {2} ({2}, Discard this card: Draw a card.)"
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Irrigated Farmland",
        "oracle_text": (
            "({T}: Add {W} or {U}.)\n"
            "Irrigated Farmland enters the battlefield tapped.\n"
            "Cycling {2} ({2}, Discard this card: Draw a card.)"
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)


def test_bond_land_filter(make_card):
    colors = [Color.white, Color.blue, Color.black]
    filter_ = BondLandFilter(colors)

    data = {
        "name": "Sea of Clouds",
        "oracle_text": (
            "Sea of Clouds enters the battlefield tapped unless you have "
            "two or more opponents.\n"
            "{T}: Add {W} or {U}."
        ),
    }
    card = make_card(**data)

    assert filter_.filter_card(card)

    data = {
        "name": "Sea of Clouds",
        "oracle_text": (
            "Sea of Clouds enters the battlefield tapped unless you have "
            "two or more opponents.\n"
            "{T}: Add {W} or {U}."
            "Some text."
        ),
    }
    card = make_card(**data)

    assert not filter_.filter_card(card)
