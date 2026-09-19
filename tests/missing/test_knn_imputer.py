import pandas as pd
import pytest

from emidaf_core.missing.imputation.knn_imputer import (
    KNNImputer,
)


def test_knn_imputer_creation():

    imputer = KNNImputer()

    assert imputer.name == "KNN"
    assert imputer.n_neighbors == 5
    assert imputer.weights == "uniform"


def test_custom_parameters():

    imputer = KNNImputer(
        n_neighbors=3,
        weights="distance",
    )

    assert imputer.n_neighbors == 3
    assert imputer.weights == "distance"


def test_invalid_neighbors_type():

    with pytest.raises(TypeError):

        KNNImputer(
            n_neighbors=2.5
        )


def test_invalid_neighbors_value():

    with pytest.raises(ValueError):

        KNNImputer(
            n_neighbors=0
        )


def test_invalid_weights():

    with pytest.raises(ValueError):

        KNNImputer(
            weights="invalid"
        )


def test_knn_imputation_numeric():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                None,
                4.0,
                5.0,
            ],
            "y": [
                10.0,
                20.0,
                30.0,
                40.0,
                50.0,
            ],
        }
    )

    imputer = KNNImputer(
        n_neighbors=2
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

    assert result.values_imputed == 1


def test_multiple_numeric_columns():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
                4.0,
            ],
            "y": [
                10.0,
                20.0,
                None,
                40.0,
            ],
        }
    )

    imputer = KNNImputer(
        n_neighbors=2
    )

    result = imputer.execute(
        dataframe=df
    )

    assert (
        result.dataframe[
            ["x", "y"]
        ]
        .isna()
        .sum()
        .sum()
        == 0
    )

    assert result.values_imputed == 2


def test_rejects_categorical_column():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ],
            "city": [
                "Dakar",
                None,
                "Thiès",
            ],
        }
    )

    imputer = KNNImputer()

    with pytest.raises(TypeError):

        imputer.execute(
            dataframe=df
        )


def test_selected_numeric_column_only():

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

    imputer = KNNImputer(
        n_neighbors=2
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


def test_original_dataframe_not_modified():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ],
            "y": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    original = df.copy(
        deep=True
    )

    imputer = KNNImputer(
        n_neighbors=2
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


def test_all_missing_column_raises_error():

    df = pd.DataFrame(
        {
            "x": [
                float("nan"),
                float("nan"),
                float("nan"),
            ],
            "y": [
                1.0,
                2.0,
                3.0,
            ],
        }
    )

    imputer = KNNImputer()

    with pytest.raises(ValueError):

        imputer.execute(
            dataframe=df
        )


def test_no_missing_values():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ],
            "y": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    imputer = KNNImputer()

    result = imputer.execute(
        dataframe=df
    )

    assert result.values_imputed == 0
    assert result.columns == []


def test_strategy_name():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ],
            "y": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    result = KNNImputer(
        n_neighbors=2
    ).execute(
        dataframe=df
    )

    assert result.strategy == "KNN"
