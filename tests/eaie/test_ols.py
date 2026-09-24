"""
=========================================================
Tests EMIDAF - OLS Regression
=========================================================
"""

import numpy as np
import pandas as pd
import pytest

from emidaf_core.common.results import OLSResult
from emidaf_core.eaie import OLSRegression


def make_linear_dataframe():

    rng = np.random.default_rng(42)

    x1 = np.linspace(
        0,
        20,
        150,
    )

    x2 = rng.normal(
        0,
        1,
        150,
    )

    noise = rng.normal(
        0,
        0.5,
        150,
    )

    y = (
        4.0
        + 2.5 * x1
        - 1.2 * x2
        + noise
    )

    return pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "y": y,
    })


def test_ols_returns_ols_result():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert isinstance(
        result,
        OLSResult,
    )

    assert result.fitted is True
    assert result.success is True
    assert result.task == "regression"
    assert result.algorithm == "OLS"
    assert result.library == "statsmodels"


def test_ols_model_information():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert result.model_name == (
        "OLS Regression"
    )

    assert result.model_type == (
        "statistical_regressor"
    )

    assert result.target == "y"

    assert result.features == [
        "x1",
        "x2",
    ]

    assert result.train_size == 150

    assert result.test_size == 0

    assert result.n_observations == 150


def test_ols_coefficients_are_correct():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert result.intercept == pytest.approx(
        4.0,
        abs=0.2,
    )

    assert result.coefficients[
        "x1"
    ] == pytest.approx(
        2.5,
        abs=0.1,
    )

    assert result.coefficients[
        "x2"
    ] == pytest.approx(
        -1.2,
        abs=0.15,
    )


def test_ols_high_r2():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert result.r2 is not None

    assert result.adjusted_r2 is not None

    assert result.r2 > 0.95

    assert result.adjusted_r2 > 0.95

    assert result.score == result.r2


def test_ols_inference_statistics():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
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
            result.t_statistics
        )

        assert variable in (
            result.p_values
        )

        assert variable in (
            result.confidence_intervals
        )

    assert result.p_values[
        "x1"
    ] < 0.05

    assert result.p_values[
        "x2"
    ] < 0.05


def test_ols_global_f_test():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert result.f_statistic is not None

    assert result.f_pvalue is not None

    assert result.f_pvalue < 0.05


def test_ols_information_criteria():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert result.aic is not None
    assert result.bic is not None
    assert result.log_likelihood is not None


def test_ols_predictions_and_residuals():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert len(
        result.predictions
    ) == len(
        dataframe
    )

    assert len(
        result.residuals
    ) == len(
        dataframe
    )


def test_ols_explicit_features():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
        features=[
            "x1",
        ],
    )

    assert result.features == [
        "x1",
    ]

    assert "x1" in result.coefficients

    assert "x2" not in result.coefficients


def test_ols_without_constant():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
        add_constant=False,
    )

    assert result.intercept is None

    assert "const" not in (
        result.coefficients
    )

    assert (
        result.parameters[
            "add_constant"
        ]
        is False
    )


def test_ols_missing_target():

    dataframe = make_linear_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        OLSRegression.fit(
            dataframe,
            target="unknown",
        )


def test_ols_missing_feature():

    dataframe = make_linear_dataframe()

    with pytest.raises(
        ValueError,
        match="absentes",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
            features=[
                "x1",
                "unknown",
            ],
        )


def test_ols_target_cannot_be_feature():

    dataframe = make_linear_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
            features=[
                "x1",
                "y",
            ],
        )


def test_ols_rejects_missing_values():

    dataframe = make_linear_dataframe()

    dataframe.loc[
        0,
        "x1",
    ] = np.nan

    with pytest.raises(
        ValueError,
        match="valeurs manquantes",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
        )


def test_ols_rejects_non_numeric_data():

    dataframe = make_linear_dataframe()

    dataframe[
        "category"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
        )


def test_ols_rejects_infinite_values():

    dataframe = make_linear_dataframe()

    dataframe.loc[
        0,
        "x1",
    ] = np.inf

    with pytest.raises(
        ValueError,
        match="finies",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
        )


def test_ols_invalid_alpha():

    dataframe = make_linear_dataframe()

    with pytest.raises(
        ValueError,
        match="alpha",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
            alpha=1.5,
        )


def test_ols_empty_dataframe():

    dataframe = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="vide",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
        )


def test_ols_requires_dataframe():

    with pytest.raises(
        TypeError,
        match="DataFrame",
    ):

        OLSRegression.fit(
            [
                [1, 2],
                [3, 4],
            ],
            target="y",
        )


def test_ols_requires_enough_observations():

    dataframe = pd.DataFrame({
        "x1": [
            1,
            2,
        ],
        "y": [
            3,
            5,
        ],
    })

    with pytest.raises(
        ValueError,
        match="nombre d'observations",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
        )


def test_ols_duplicate_features():

    dataframe = make_linear_dataframe()

    with pytest.raises(
        ValueError,
        match="doublons",
    ):

        OLSRegression.fit(
            dataframe,
            target="y",
            features=[
                "x1",
                "x1",
            ],
        )


def test_ols_metadata():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    assert result.metadata[
        "inference"
    ] is True

    assert result.metadata[
        "method"
    ] == (
        "Ordinary Least Squares"
    )

    assert result.metadata[
        "alpha"
    ] == 0.05


def test_ols_summary():

    dataframe = make_linear_dataframe()

    result = OLSRegression.fit(
        dataframe,
        target="y",
    )

    summary = result.summary()

    assert summary[
        "Model"
    ] == "OLS Regression"

    assert "R²" in summary

    assert "Adjusted R²" in summary

    assert "AIC" in summary

    assert "BIC" in summary

    assert summary[
        "Observations"
    ] == 150


def test_ols_run_alias():

    dataframe = make_linear_dataframe()

    result = OLSRegression.run(
        dataframe,
        target="y",
    )

    assert isinstance(
        result,
        OLSResult,
    )

    assert result.fitted is True
