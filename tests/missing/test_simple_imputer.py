import pandas as pd
import pytest

from emidaf_core.missing.imputation.simple_imputer import (
    SimpleImputer,
)


def test_simple_imputer_creation_mean():

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    assert imputer.strategy == "MEAN"
    assert imputer.name == "MEAN"


def test_simple_imputer_creation_mode():

    imputer = SimpleImputer(
        strategy="MODE"
    )

    assert imputer.strategy == "MODE"
    assert imputer.name == "MODE"


def test_invalid_strategy():

    with pytest.raises(ValueError):

        SimpleImputer(
            strategy="INVALID"
        )


def test_mean_imputation_numeric():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    result = imputer.execute(
        dataframe=df
    )

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )

    assert (
        result.dataframe.loc[
            1,
            "x",
        ]
        == 2.0
    )

    assert result.values_imputed == 1


def test_mean_rejects_categorical_column():

    df = pd.DataFrame(
        {
            "city": [
                "Dakar",
                None,
                "Thiès",
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    with pytest.raises(TypeError):

        imputer.execute(
            dataframe=df
        )


def test_mode_imputation_categorical():

    df = pd.DataFrame(
        {
            "city": [
                "Dakar",
                "Dakar",
                None,
                "Thiès",
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MODE"
    )

    result = imputer.execute(
        dataframe=df
    )

    assert (
        result.dataframe.loc[
            2,
            "city",
        ]
        == "Dakar"
    )

    assert result.values_imputed == 1


def test_mode_imputation_numeric():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                1.0,
                None,
                3.0,
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MODE"
    )

    result = imputer.execute(
        dataframe=df
    )

    assert (
        result.dataframe.loc[
            2,
            "x",
        ]
        == 1.0
    )


def test_selected_column_only():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ],
            "y": [
                10.0,
                None,
                30.0,
            ],
        }
    )

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    result = imputer.execute(
        dataframe=df,
        columns=["x"],
    )

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )

    assert (
        result.dataframe["y"]
        .isna()
        .sum()
        == 1
    )

    assert result.columns == [
        "x"
    ]


def test_original_dataframe_not_modified():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    original = df.copy(
        deep=True
    )

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    result = imputer.execute(
        dataframe=df
    )

    assert df.equals(
        original
    )

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_all_missing_mean_raises_error():

    df = pd.DataFrame(
        {
            "x": [
                None,
                None,
                None,
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    with pytest.raises(ValueError):

        imputer.execute(
            dataframe=df
        )


def test_all_missing_mode_raises_error():

    df = pd.DataFrame(
        {
            "x": [
                None,
                None,
                None,
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MODE"
    )

    with pytest.raises(ValueError):

        imputer.execute(
            dataframe=df
        )


def test_strategy_name_in_result():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    imputer = SimpleImputer(
        strategy="MEAN"
    )

    result = imputer.execute(
        dataframe=df
    )

    assert result.strategy == "MEAN"
