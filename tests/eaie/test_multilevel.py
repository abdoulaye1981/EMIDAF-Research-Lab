"""
=========================================================
Tests EMIDAF - Multilevel Linear Model
=========================================================
"""

import numpy as np
import pandas as pd
import pytest

from emidaf_core.common.results import (
    MultilevelResult,
)
from emidaf_core.eaie import (
    MultilevelLinearModel,
)


def make_multilevel_dataframe():

    rng = np.random.default_rng(42)

    n_groups = 10
    n_per_group = 20

    groups = np.repeat(
        np.arange(n_groups),
        n_per_group,
    )

    n = len(groups)

    x1 = rng.normal(
        0,
        1,
        n,
    )

    x2 = rng.normal(
        0,
        1,
        n,
    )

    group_effects = rng.normal(
        0,
        2.5,
        n_groups,
    )

    y = (
        5.0
        + 2.0 * x1
        - 1.2 * x2
        + group_effects[groups]
        + rng.normal(
            0,
            1.5,
            n,
        )
    )

    return pd.DataFrame({
        "group": groups,
        "x1": x1,
        "x2": x2,
        "y": y,
    })


def test_multilevel_returns_result():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert isinstance(
        result,
        MultilevelResult,
    )

    assert result.fitted is True
    assert result.success is True

    assert result.algorithm == (
        "MixedLM"
    )

    assert result.task == (
        "regression"
    )

    assert result.library == (
        "statsmodels"
    )


def test_multilevel_converges():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert result.converged is True


def test_multilevel_group_information():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert result.group_column == (
        "group"
    )

    assert result.n_groups == 10


def test_multilevel_fixed_effects():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert "const" in (
        result.fixed_effects
    )

    assert "x1" in (
        result.fixed_effects
    )

    assert "x2" in (
        result.fixed_effects
    )

    assert result.fixed_effects[
        "x1"
    ] == pytest.approx(
        2.0,
        abs=0.3,
    )

    assert result.fixed_effects[
        "x2"
    ] == pytest.approx(
        -1.2,
        abs=0.3,
    )


def test_multilevel_coefficients():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert "x1" in (
        result.coefficients
    )

    assert "x2" in (
        result.coefficients
    )

    assert "const" not in (
        result.coefficients
    )

    assert result.intercept is not None


def test_multilevel_inference():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    for variable in [
        "const",
        "x1",
        "x2",
    ]:

        assert variable in (
            result.standard_errors
        )

        assert variable in (
            result.z_statistics
        )

        assert variable in (
            result.p_values
        )

        assert variable in (
            result.confidence_intervals
        )


def test_multilevel_variances():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert result.group_variance is not None
    assert result.residual_variance is not None

    assert result.group_variance >= 0
    assert result.residual_variance > 0


def test_multilevel_icc():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert result.icc is not None

    assert 0 <= result.icc <= 1


def test_multilevel_information_criteria():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert result.log_likelihood is not None

    assert result.aic is not None

    assert result.bic is not None


def test_multilevel_predictions_and_residuals():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert len(
        result.predictions
    ) == len(df)

    assert len(
        result.residuals
    ) == len(df)


def test_multilevel_explicit_features():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
        features=[
            "x1",
        ],
    )

    assert result.features == [
        "x1",
    ]

    assert "x1" in (
        result.coefficients
    )

    assert "x2" not in (
        result.coefficients
    )


def test_multilevel_without_constant():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
        add_constant=False,
    )

    assert result.intercept is None

    assert "const" not in (
        result.fixed_effects
    )


def test_multilevel_metadata():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    assert result.metadata[
        "multilevel"
    ] is True

    assert result.metadata[
        "mixed_effects"
    ] is True

    assert result.metadata[
        "random_intercept"
    ] is True

    assert result.metadata[
        "n_groups"
    ] == 10


def test_multilevel_summary():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.fit(
        df,
        target="y",
        group="group",
    )

    summary = result.summary()

    assert summary[
        "Model"
    ] == (
        "Multilevel Linear Model"
    )

    assert summary[
        "Groups"
    ] == 10

    assert "ICC" in summary
    assert "AIC" in summary
    assert "BIC" in summary


def test_multilevel_run_alias():

    df = make_multilevel_dataframe()

    result = MultilevelLinearModel.run(
        df,
        target="y",
        group="group",
    )

    assert isinstance(
        result,
        MultilevelResult,
    )


def test_multilevel_requires_dataframe():

    with pytest.raises(
        TypeError,
        match="DataFrame",
    ):

        MultilevelLinearModel.fit(
            [],
            target="y",
            group="group",
        )


def test_multilevel_empty_dataframe():

    with pytest.raises(
        ValueError,
        match="vide",
    ):

        MultilevelLinearModel.fit(
            pd.DataFrame(),
            target="y",
            group="group",
        )


def test_multilevel_missing_target():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        MultilevelLinearModel.fit(
            df,
            target="unknown",
            group="group",
        )


def test_multilevel_missing_group():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="groupe",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="unknown",
        )


def test_multilevel_target_equals_group():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="différentes",
    ):

        MultilevelLinearModel.fit(
            df,
            target="group",
            group="group",
        )


def test_multilevel_group_not_feature():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="groupe",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
            features=[
                "x1",
                "group",
            ],
        )


def test_multilevel_target_not_feature():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
            features=[
                "x1",
                "y",
            ],
        )


def test_multilevel_duplicate_features():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="doublons",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
            features=[
                "x1",
                "x1",
            ],
        )


def test_multilevel_missing_feature():

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="absentes",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
            features=[
                "x1",
                "unknown",
            ],
        )


def test_multilevel_missing_values():

    df = make_multilevel_dataframe()

    df.loc[
        0,
        "x1",
    ] = np.nan

    with pytest.raises(
        ValueError,
        match="valeurs manquantes",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
        )


def test_multilevel_non_numeric_feature():

    df = make_multilevel_dataframe()

    df[
        "category"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
        )


def test_multilevel_non_numeric_target():

    df = make_multilevel_dataframe()

    df[
        "y"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
        )


def test_multilevel_infinite_values():

    df = make_multilevel_dataframe()

    df.loc[
        0,
        "x1",
    ] = np.inf

    with pytest.raises(
        ValueError,
        match="finies",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
        )


def test_multilevel_requires_two_groups():

    df = make_multilevel_dataframe()

    df[
        "group"
    ] = 1

    with pytest.raises(
        ValueError,
        match="deux groupes",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
        )


def test_multilevel_requires_two_observations_per_group():

    df = make_multilevel_dataframe()

    df.loc[
        0,
        "group",
    ] = 999

    with pytest.raises(
        ValueError,
        match="deux observations",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
        )


@pytest.mark.parametrize(
    "alpha",
    [
        0,
        1,
        -0.1,
        1.2,
        "invalid",
    ],
)
def test_multilevel_invalid_alpha(
    alpha,
):

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="alpha",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
            alpha=alpha,
        )


@pytest.mark.parametrize(
    "maxiter",
    [
        0,
        -1,
        "invalid",
    ],
)
def test_multilevel_invalid_maxiter(
    maxiter,
):

    df = make_multilevel_dataframe()

    with pytest.raises(
        ValueError,
        match="maxiter",
    ):

        MultilevelLinearModel.fit(
            df,
            target="y",
            group="group",
            maxiter=maxiter,
        )
