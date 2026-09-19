import numpy as np
import pandas as pd
import pytest

from emidaf_core.missing.mechanism.mnar_analyzer import (
    MNARAnalyzer,
    MNARResult,
)


def test_mnar_analyzer_creation():

    analyzer = MNARAnalyzer()

    assert analyzer is not None


def test_invalid_dataframe():

    analyzer = MNARAnalyzer()

    with pytest.raises(TypeError):
        analyzer.run(
            dataframe=[1, 2, 3]
        )


def test_invalid_threshold():

    analyzer = MNARAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(ValueError):
        analyzer.run(
            dataframe=df,
            high_missing_rate=0.0,
        )


def test_invalid_mar_evidence():

    analyzer = MNARAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(TypeError):
        analyzer.run(
            dataframe=df,
            mar_evidence=["x"],
        )


def test_empty_dataframe():

    analyzer = MNARAnalyzer()

    result = analyzer.run(
        pd.DataFrame()
    )

    assert isinstance(
        result,
        MNARResult,
    )

    assert result.executed is False

    assert (
        result.evidence_level
        == "not_evaluated"
    )


def test_without_missing_values():

    analyzer = MNARAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6],
        }
    )

    result = analyzer.run(df)

    assert result.executed is False

    assert (
        result.evidence_level
        == "not_required"
    )

    assert (
        result.sensitivity_required
        is False
    )


def test_low_missing_rate_with_mar_evidence():

    rng = np.random.default_rng(42)

    n = 500

    df = pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": rng.normal(size=n),
        }
    )

    mask = rng.random(n) < 0.05

    df.loc[
        mask,
        "y"
    ] = np.nan

    analyzer = MNARAnalyzer()

    result = analyzer.run(
        dataframe=df,
        mar_evidence={
            "y": True,
        },
    )

    y_result = next(
        item
        for item in result.results
        if item.variable == "y"
    )

    assert (
        y_result.risk_level
        == "low"
    )

    assert (
        y_result.sensitivity_required
        is False
    )


def test_high_missing_rate_without_mar_evidence():

    rng = np.random.default_rng(123)

    n = 500

    df = pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": rng.normal(size=n),
        }
    )

    df.loc[
        :249,
        "y"
    ] = np.nan

    analyzer = MNARAnalyzer()

    result = analyzer.run(
        dataframe=df,
        mar_evidence={
            "y": False,
        },
    )

    y_result = next(
        item
        for item in result.results
        if item.variable == "y"
    )

    assert (
        y_result.risk_level
        == "high"
    )

    assert (
        y_result.sensitivity_required
        is True
    )

    assert (
        result.sensitivity_required
        is True
    )


def test_entirely_missing_variable_is_high_risk():

    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
            ],
        }
    )

    analyzer = MNARAnalyzer()

    result = analyzer.run(
        dataframe=df,
        mar_evidence={
            "y": False,
        },
    )

    y_result = next(
        item
        for item in result.results
        if item.variable == "y"
    )

    assert (
        y_result.risk_level
        == "high"
    )

    assert (
        y_result.suspicion_score
        >= 0.8
    )

    assert (
        result.evidence_level
        == "high_risk"
    )
