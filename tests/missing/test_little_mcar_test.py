import pandas as pd
import pytest

from emidaf_core.missing.mechanism.little_mcar_test import (
    LittleMCARResult,
    LittleMCARTest,
)


def test_little_mcar_test_creation():

    test = LittleMCARTest()

    assert test is not None


def test_invalid_dataframe():

    test = LittleMCARTest()

    with pytest.raises(TypeError):

        test.run(
            dataframe=[1, 2, 3]
        )


def test_invalid_alpha_zero():

    test = LittleMCARTest()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(ValueError):

        test.run(
            dataframe=df,
            alpha=0.0,
        )


def test_invalid_alpha_one():

    test = LittleMCARTest()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(ValueError):

        test.run(
            dataframe=df,
            alpha=1.0,
        )


def test_empty_dataframe():

    test = LittleMCARTest()

    df = pd.DataFrame()

    result = test.run(df)

    assert isinstance(
        result,
        LittleMCARResult
    )

    assert result.executed is False
    assert result.is_mcar is None
    assert result.statistic is None
    assert result.pvalue is None


def test_dataframe_without_missing_values():

    test = LittleMCARTest()

    df = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0],
            "y": [4.0, 5.0, 6.0],
        }
    )

    result = test.run(df)

    assert isinstance(
        result,
        LittleMCARResult
    )

    assert result.executed is False
    assert result.is_mcar is None


def test_dataframe_with_missing_values_pending():

    test = LittleMCARTest()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0],
            "y": [4.0, 5.0, None],
        }
    )

    result = test.run(df)

    assert isinstance(
        result,
        LittleMCARResult
    )

    assert result.executed is False
    assert result.statistic is None
    assert result.pvalue is None

import numpy as np


def test_little_mcar_executes_on_valid_numeric_data():

    rng = np.random.default_rng(42)

    n = 300

    df = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "x3": rng.normal(size=n),
        }
    )

    # Missingness générée indépendamment des valeurs :
    # situation compatible avec MCAR.
    mask_x1 = rng.random(n) < 0.10
    mask_x2 = rng.random(n) < 0.15
    mask_x3 = rng.random(n) < 0.08

    df.loc[mask_x1, "x1"] = np.nan
    df.loc[mask_x2, "x2"] = np.nan
    df.loc[mask_x3, "x3"] = np.nan

    test = LittleMCARTest()

    result = test.run(df)

    assert isinstance(
        result,
        LittleMCARResult,
    )

    assert result.executed is True

    assert result.statistic is not None
    assert result.statistic >= 0

    assert result.pvalue is not None
    assert 0 <= result.pvalue <= 1

    assert result.degrees_of_freedom is not None
    assert result.degrees_of_freedom > 0

    assert isinstance(
        result.is_mcar,
        bool,
    )


def test_little_mcar_rejects_structured_missingness():

    rng = np.random.default_rng(123)

    n = 500

    x1 = rng.normal(size=n)

    x2 = (
        2.5 * x1
        + rng.normal(
            scale=0.5,
            size=n,
        )
    )

    x3 = rng.normal(size=n)

    df = pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "x3": x3,
        }
    )

    # Missingness dépend fortement d'une variable observée :
    # ce mécanisme n'est donc pas MCAR.
    mask = df["x1"] > 0.5

    df.loc[
        mask,
        "x2"
    ] = np.nan

    test = LittleMCARTest()

    result = test.run(
        df,
        alpha=0.05,
    )

    assert result.executed is True

    assert result.pvalue is not None

    assert result.pvalue <= 0.05

    assert result.is_mcar is False
