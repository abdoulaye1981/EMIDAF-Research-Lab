import numpy as np
import pandas as pd
import pytest

from emidaf_core.missing.mechanism.mechanism_analyzer import (
    MechanismAnalyzer,
)


def test_mechanism_analyzer_creation():

    analyzer = MechanismAnalyzer()

    assert analyzer is not None


def test_invalid_dataframe():

    analyzer = MechanismAnalyzer()

    with pytest.raises(TypeError):

        analyzer.analyze(
            dataframe=[1, 2, 3]
        )


def test_invalid_alpha():

    analyzer = MechanismAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(ValueError):

        analyzer.analyze(
            dataframe=df,
            alpha=0.0,
        )


def test_empty_dataframe():

    analyzer = MechanismAnalyzer()

    result = analyzer.analyze(
        pd.DataFrame()
    )

    assert (
        result["status"]
        == "Not evaluated"
    )

    assert (
        result["candidate"]
        == "Unknown"
    )

    assert (
        result["detected"]
        is False
    )


def test_without_missing_values():

    analyzer = MechanismAnalyzer()

    df = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6],
        }
    )

    result = analyzer.analyze(df)

    assert (
        result["status"]
        == "Not required"
    )

    assert (
        result["candidate"]
        == "None"
    )

    assert (
        result["detected"]
        is False
    )


def test_mcar_candidate():

    rng = np.random.default_rng(42)

    n = 1200

    df = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "x3": rng.normal(size=n),
        }
    )

    mask_x1 = (
        rng.random(n) < 0.08
    )

    mask_x2 = (
        rng.random(n) < 0.10
    )

    mask_x3 = (
        rng.random(n) < 0.06
    )

    df.loc[
        mask_x1,
        "x1"
    ] = np.nan

    df.loc[
        mask_x2,
        "x2"
    ] = np.nan

    df.loc[
        mask_x3,
        "x3"
    ] = np.nan

    analyzer = MechanismAnalyzer()

    result = analyzer.analyze(df)

    if result["candidate"] == "MCAR":

        assert result["detected"] is False

    assert (
        result["candidate"]
        in {
            "MCAR",
            "Unknown",
        }
    )

    assert (
        "tests"
        in result
    )

    assert (
        result["tests"]["mcar"]["executed"]
        is True
    )


def test_mar_candidate():

    rng = np.random.default_rng(123)

    n = 800

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

    df.loc[
        df["age"] > 45,
        "income"
    ] = np.nan

    analyzer = MechanismAnalyzer()

    result = analyzer.analyze(df)

    assert (
        result["status"]
        == "Evaluated"
    )

    assert (
        result["candidate"]
        == "MAR"
    )

    assert (
        result["detected"]
        is True
    )

    assert (
        result["tests"]["mar"]["executed"]
        is True
    )


def test_result_has_builder_contract():

    rng = np.random.default_rng(321)

    n = 300

    df = pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": rng.normal(size=n),
        }
    )

    mask = (
        rng.random(n) < 0.15
    )

    df.loc[
        mask,
        "y"
    ] = np.nan

    analyzer = MechanismAnalyzer()

    result = analyzer.analyze(df)

    required_keys = {
        "status",
        "candidate",
        "detected",
        "confidence",
        "pvalue",
        "statistic",
        "test_name",
        "explanation",
        "tests",
    }

    assert required_keys.issubset(
        result.keys()
    )


def test_confidence_is_bounded():

    rng = np.random.default_rng(555)

    n = 500

    df = pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": rng.normal(size=n),
            "z": rng.normal(size=n),
        }
    )

    df.loc[
        df["x"] > 0.5,
        "y"
    ] = np.nan

    analyzer = MechanismAnalyzer()

    result = analyzer.analyze(df)

    assert (
        0.0
        <= result["confidence"]
        <= 1.0
    )
