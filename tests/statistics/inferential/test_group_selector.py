import numpy as np

from emidaf_core.statistics.inferential.group_selector import (
    GroupTestSelector,
)


def test_two_compatible_groups_choose_welch():
    rng = np.random.default_rng(42)

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

    assert (
        selection[
            "parametric_compatible"
        ]
        is True
    )


def test_two_incompatible_groups_choose_mann_whitney():
    rng = np.random.default_rng(42)

    g1 = rng.exponential(
        scale=1.0,
        size=120,
    )

    g2 = rng.exponential(
        scale=2.0,
        size=120,
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

    assert (
        selection[
            "parametric_compatible"
        ]
        is False
    )


def test_k_groups_equal_variances_choose_anova():
    rng = np.random.default_rng(123)

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

    assert (
        selection[
            "variance_homogeneous"
        ]
        is True
    )


def test_k_groups_unequal_variances_choose_welch_anova():
    rng = np.random.default_rng(456)

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

    assert (
        selection[
            "variance_homogeneous"
        ]
        is False
    )


def test_k_groups_incompatible_choose_kruskal():
    rng = np.random.default_rng(789)

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


def test_selector_keeps_diagnostics():
    rng = np.random.default_rng(100)

    g1 = rng.normal(
        0,
        1,
        100,
    )

    g2 = rng.normal(
        1,
        1,
        100,
    )

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
        )
    )

    diagnostics = (
        selection[
            "group_diagnostics"
        ]
    )

    assert len(diagnostics) == 2

    for item in diagnostics:
        assert "n" in item
        assert "skewness" in item
        assert "kurtosis" in item
        assert "shapiro_p_value" in item
        assert (
            "parametric_compatible"
            in item
        )


def test_small_samples_use_shapiro_and_shape():
    g1 = np.array(
        [
            1.0,
            1.2,
            0.9,
            1.1,
            1.3,
            0.8,
            1.0,
            1.1,
            0.9,
            1.2,
        ]
    )

    g2 = np.array(
        [
            2.0,
            2.1,
            1.9,
            2.2,
            2.0,
            1.8,
            2.1,
            1.9,
            2.2,
            2.0,
        ]
    )

    selection = (
        GroupTestSelector()
        .select(
            g1,
            g2,
        )
    )

    for item in selection[
        "group_diagnostics"
    ]:
        assert (
            item[
                "decision_basis"
            ]
            ==
            "small_sample_shape_and_shapiro"
        )


def test_selector_requires_two_groups():
    selector = (
        GroupTestSelector()
    )

    try:
        selector.select(
            [1, 2, 3]
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "ValueError attendu."
        )
