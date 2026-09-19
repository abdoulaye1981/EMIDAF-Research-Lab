import pandas as pd
import pytest

from emidaf_core.missing.imputation.base_imputer import (
    BaseImputer,
    ImputationResult,
)


class DummyImputer(BaseImputer):

    name = "DUMMY"

    def impute(
        self,
        dataframe: pd.DataFrame,
        columns: list[str],
        **kwargs,
    ) -> pd.DataFrame:

        for column in columns:

            dataframe[column] = (
                dataframe[column].fillna(0)
            )

        return dataframe


def test_base_imputer_creation():

    imputer = DummyImputer()

    assert imputer is not None


def test_invalid_dataframe():

    imputer = DummyImputer()

    with pytest.raises(TypeError):

        imputer.execute(
            dataframe=[1, 2, 3]
        )


def test_invalid_columns_type():

    imputer = DummyImputer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(TypeError):

        imputer.execute(
            dataframe=df,
            columns="x",
        )


def test_unknown_column():

    imputer = DummyImputer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0]
        }
    )

    with pytest.raises(ValueError):

        imputer.execute(
            dataframe=df,
            columns=[
                "unknown"
            ],
        )


def test_auto_detect_missing_columns():

    imputer = DummyImputer()

    df = pd.DataFrame(
        {
            "x": [1.0, None, 3.0],
            "y": [4.0, 5.0, 6.0],
        }
    )

    result = imputer.execute(
        dataframe=df
    )

    assert isinstance(
        result,
        ImputationResult,
    )

    assert result.columns == [
        "x"
    ]


def test_values_imputed():

    imputer = DummyImputer()

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
                None,
            ]
        }
    )

    result = imputer.execute(
        dataframe=df
    )

    assert result.values_imputed == 2

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_original_dataframe_not_modified():

    imputer = DummyImputer()

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


def test_no_missing_values():

    imputer = DummyImputer()

    df = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0],
            "y": [4.0, 5.0, 6.0],
        }
    )

    result = imputer.execute(
        dataframe=df
    )

    assert result.columns == []
    assert result.values_imputed == 0
    assert result.success is True
