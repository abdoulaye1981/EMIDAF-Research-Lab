import numpy as np

from emidaf_core.statistics.inferential.group_selector import (
    GroupTestSelector,
)
from emidaf_core.statistics.inferential.group_effect_size import (
    GroupEffectSize,
)


def test_welch_returns_hedges_g():
    rng = np.random.default_rng(10)

    g1 = rng.normal(
        10,
        2,
        120,
    )

    g2 = rng.normal(
        11,
        2,
        120,
    )

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
        )
    )

    assert (
        selection["selected_test"]
        == "welch"
    )

    effect = (
        GroupEffectSize.compute(
            selection,
            g1,
            g2,
        )
    )

    assert (
        effect["name"]
        == "Hedges g"
    )

    assert np.isfinite(
        effect["value"]
    )


def test_mann_whitney_returns_rank_biserial():
    rng = np.random.default_rng(20)

    g1 = rng.exponential(
        1,
        120,
    )

    g2 = rng.exponential(
        2,
        120,
    )

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
        )
    )

    assert (
        selection["selected_test"]
        == "mann_whitney"
    )

    effect = (
        GroupEffectSize.compute(
            selection,
            g1,
            g2,
        )
    )

    assert (
        effect["name"]
        == "Rank-biserial correlation"
    )

    assert (
        -1.0
        <= effect["value"]
        <= 1.0
    )


def test_anova_returns_omega_and_eta_squared():
    rng = np.random.default_rng(30)

    base = rng.normal(
        0,
        1,
        300,
    )

    g1 = base.copy()
    g2 = base + 0.3
    g3 = base + 0.6

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
            g3,
        )
    )

    assert (
        selection["selected_test"]
        == "anova"
    )

    effect = (
        GroupEffectSize.compute(
            selection,
            g1,
            g2,
            g3,
        )
    )

    assert (
        effect["name"]
        == "Omega Squared"
    )

    assert (
        effect["secondary"]["name"]
        == "Eta Squared"
    )


def test_welch_anova_effect_is_marked_descriptive():
    rng = np.random.default_rng(40)

    g1 = rng.normal(
        10,
        1,
        400,
    )

    g2 = rng.normal(
        11,
        2,
        400,
    )

    g3 = rng.normal(
        12,
        3,
        400,
    )

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
            g3,
        )
    )

    assert (
        selection["selected_test"]
        == "welch_anova"
    )

    effect = (
        GroupEffectSize.compute(
            selection,
            g1,
            g2,
            g3,
        )
    )

    assert (
        effect["name"]
        == "Eta Squared (descriptive)"
    )

    assert (
        effect["descriptive_only"]
        is True
    )


def test_kruskal_returns_epsilon_squared():
    rng = np.random.default_rng(50)

    g1 = rng.exponential(
        1,
        200,
    )

    g2 = rng.exponential(
        2,
        200,
    )

    g3 = rng.exponential(
        3,
        200,
    )

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
            g3,
        )
    )

    assert (
        selection["selected_test"]
        == "kruskal"
    )

    effect = (
        GroupEffectSize.compute(
            selection,
            g1,
            g2,
            g3,
        )
    )

    assert (
        effect["name"]
        ==
        "Kruskal-Wallis epsilon squared"
    )

    assert (
        effect["value"]
        >= 0.0
    )
