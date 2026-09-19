import pandas as pd
import pytest

from emidaf_core.missing.imputation.missing_imputer import (
    MissingImputer,
)


def test_missing_imputer_creation():

    imputer = MissingImputer()

    assert imputer is not None


def test_invalid_dataframe():

    imputer = MissingImputer()

    with pytest.raises(TypeError):

        imputer.execute(
            dataframe=[1, 2, 3],
            strategy="MEAN",
        )


def test_invalid_strategy_type():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    with pytest.raises(TypeError):

        MissingImputer().execute(
            dataframe=df,
            strategy=123,
        )


def test_unknown_strategy():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    with pytest.raises(ValueError):

        MissingImputer().execute(
            dataframe=df,
            strategy="UNKNOWN",
        )


def test_strategy_is_case_insensitive():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="mean",
    )

    assert result.strategy == "MEAN"


def test_none_strategy():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="NONE",
    )

    assert result.strategy == "NONE"
    assert result.values_imputed == 0
    assert result.success is True
    assert (
        result.details["action_required"]
        is False
    )


def test_none_does_not_modify_dataframe():

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

    result = MissingImputer().execute(
        dataframe=df,
        strategy="NONE",
    )

    assert df.equals(
        original
    )

    assert result.dataframe.equals(
        original
    )


def test_review_strategy():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="REVIEW",
    )

    assert result.strategy == "REVIEW"
    assert result.values_imputed == 0

    assert (
        result.details["action_required"]
        is True
    )

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 1
    )


def test_mean_delegation():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="MEAN",
    )

    assert result.strategy == "MEAN"
    assert result.values_imputed == 1

    assert (
        result.dataframe.loc[
            1,
            "x",
        ]
        == 2.0
    )


def test_mode_delegation():

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

    result = MissingImputer().execute(
        dataframe=df,
        strategy="MODE",
    )

    assert result.strategy == "MODE"

    assert (
        result.dataframe.loc[
            2,
            "city",
        ]
        == "Dakar"
    )


def test_knn_delegation():

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
                30.0,
                40.0,
            ],
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="KNN",
        n_neighbors=2,
    )

    assert result.strategy == "KNN"

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_mice_delegation():

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
                30.0,
                40.0,
            ],
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="MICE",
        random_state=42,
    )

    assert result.strategy == "MICE"

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_selected_columns_are_respected():

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

    result = MissingImputer().execute(
        dataframe=df,
        strategy="MEAN",
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


def test_unknown_column():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    with pytest.raises(ValueError):

        MissingImputer().execute(
            dataframe=df,
            strategy="MEAN",
            columns=["unknown"],
        )


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

    result = MissingImputer().execute(
        dataframe=df,
        strategy="MEAN",
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


def test_knn_parameters_are_forwarded():

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
                30.0,
                40.0,
            ],
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="KNN",
        n_neighbors=2,
        weights="distance",
    )

    assert result.success is True

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_mice_parameters_are_forwarded():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
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

    result = MissingImputer().execute(
        dataframe=df,
        strategy="MICE",
        max_iter=5,
        random_state=123,
        initial_strategy="median",
        sample_posterior=False,
    )

    assert result.success is True

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_review_preserves_missing_count():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                None,
            ]
        }
    )

    result = MissingImputer().execute(
        dataframe=df,
        strategy="REVIEW",
    )

    assert (
        result.details[
            "missing_before"
        ]
        == 2
    )

    assert (
        result.details[
            "missing_after"
        ]
        == 2
    )

    assert result.values_imputed == 0
