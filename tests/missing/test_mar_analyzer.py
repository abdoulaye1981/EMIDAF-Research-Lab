import numpy as np
import pandas as pd
import pytest

from emidaf_core.missing.mechanism.mar_analyzer import (
    MARAnalyzer,
    MARResult,
)


def test_mar_analyzer_creation():

    analyzer = MARAnalyzer()

    assert analyzer is not None


def test_invalid_dataframe():

    analyzer = MARAnalyzer()

    with pytest.raises(TypeError):
        analyzer.run(
            dataframe=[1, 2, 3]
        )


def test_invalid_alpha():

    analyzer = MARAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(ValueError):
        analyzer.run(
            dataframe=df,
            alpha=0.0,
        )


def test_empty_dataframe():

    analyzer = MARAnalyzer()

    result = analyzer.run(
        pd.DataFrame()
    )

    assert isinstance(
        result,
        MARResult,
    )

    assert result.executed is False
    assert result.evidence_detected is None


def test_without_missing_values():

    analyzer = MARAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6],
        }
    )

    result = analyzer.run(df)

    assert result.executed is False
    assert result.variables_tested == 0


def test_mar_numeric_signal():

    rng = np.random.default_rng(42)

    n = 600

    age = rng.normal(
        loc=40,
        scale=10,
        size=n,
    )

    income = rng.normal(
        loc=500,
        scale=100,
        size=n,
    )

    score = rng.normal(
        size=n
    )

    df = pd.DataFrame(
        {
            "age": age,
            "income": income,
            "score": score,
        }
    )

    # Missingness de income dépend fortement de age.
    mask = df["age"] > 45

    df.loc[
        mask,
        "income"
    ] = np.nan

    analyzer = MARAnalyzer()

    result = analyzer.run(df)

    assert result.executed is True
    assert result.evidence_detected is True

    income_result = next(
        item
        for item in result.results
        if item.variable == "income"
    )

    assert (
        income_result.evidence_detected
        is True
    )

    assert (
        income_result.significant_count
        >= 1
    )

    assert (
        income_result.strongest_predictor
        == "age"
    )


def test_mar_categorical_signal():

    rng = np.random.default_rng(123)

    n = 500

    region = np.where(
        np.arange(n) < 250,
        "urban",
        "rural",
    )

    income = rng.normal(
        size=n
    )

    df = pd.DataFrame(
        {
            "region": region,
            "income": income,
        }
    )

    # Missingness fortement dépendante de region.
    mask = df["region"] == "rural"

    df.loc[
        mask,
        "income"
    ] = np.nan

    analyzer = MARAnalyzer()

    result = analyzer.run(df)

    income_result = next(
        item
        for item in result.results
        if item.variable == "income"
    )

    assert (
        income_result.evidence_detected
        is True
    )

    assert (
        income_result.strongest_predictor
        == "region"
    )


def test_random_missingness_no_forced_conclusion():

    rng = np.random.default_rng(100)

    n = 1000

    df = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "x3": rng.normal(size=n),
        }
    )

    mask = rng.random(n) < 0.10

    df.loc[
        mask,
        "x2"
    ] = np.nan

    analyzer = MARAnalyzer()

    result = analyzer.run(df)

    assert result.executed is True

    x2_result = next(
        item
        for item in result.results
        if item.variable == "x2"
    )

    assert (
        x2_result.association_count
        >= 1
    )


def test_adjusted_pvalues_are_valid():

    rng = np.random.default_rng(55)

    n = 400

    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    target = rng.normal(size=n)

    df = pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "target": target,
        }
    )

    df.loc[
        df["x1"] > 0.5,
        "target"
    ] = np.nan

    analyzer = MARAnalyzer()

    result = analyzer.run(df)

    target_result = next(
        item
        for item in result.results
        if item.variable == "target"
    )

    for association in (
        target_result.associations
    ):
        assert (
            association.adjusted_pvalue
            is not None
        )

        assert (
            0.0
            <= association.adjusted_pvalue
            <= 1.0
        )
