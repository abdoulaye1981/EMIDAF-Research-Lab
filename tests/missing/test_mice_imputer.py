import pandas as pd
import pytest

from emidaf_core.missing.imputation.mice_imputer import (
    MICEImputer,
)


def test_mice_imputer_creation():

    imputer = MICEImputer()

    assert imputer.name == "MICE"
    assert imputer.max_iter == 10
    assert imputer.random_state == 42
    assert imputer.initial_strategy == "mean"
    assert imputer.sample_posterior is False


def test_custom_parameters():

    imputer = MICEImputer(
        max_iter=20,
        random_state=123,
        initial_strategy="median",
        sample_posterior=True,
    )

    assert imputer.max_iter == 20
    assert imputer.random_state == 123
    assert imputer.initial_strategy == "median"
    assert imputer.sample_posterior is True


def test_invalid_max_iter_type():

    with pytest.raises(TypeError):

        MICEImputer(
            max_iter=5.5
        )


def test_invalid_max_iter_value():

    with pytest.raises(ValueError):

        MICEImputer(
            max_iter=0
        )


def test_invalid_random_state():

    with pytest.raises(TypeError):

        MICEImputer(
            random_state="42"
        )


def test_invalid_initial_strategy():

    with pytest.raises(ValueError):

        MICEImputer(
            initial_strategy="invalid"
        )


def test_invalid_sample_posterior():

    with pytest.raises(TypeError):

        MICEImputer(
            sample_posterior="yes"
        )


def test_mice_imputation_numeric():

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

    imputer = MICEImputer(
        max_iter=10,
        random_state=42,
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
                5.0,
            ],
            "y": [
                10.0,
                20.0,
                None,
                40.0,
                50.0,
            ],
            "z": [
                100.0,
                200.0,
                300.0,
                None,
                500.0,
            ],
        }
    )

    result = MICEImputer(
        random_state=42
    ).execute(
        dataframe=df
    )

    assert (
        result.dataframe[
            ["x", "y", "z"]
        ]
        .isna()
        .sum()
        .sum()
        == 0
    )

    assert result.values_imputed == 3


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

    imputer = MICEImputer()

    with pytest.raises(TypeError):

        imputer.execute(
            dataframe=df
        )


def test_selected_numeric_columns_only():

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
                None,
                30.0,
                40.0,
            ],
        }
    )

    result = MICEImputer(
        random_state=42
    ).execute(
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

    original = df.copy(
        deep=True
    )

    result = MICEImputer(
        random_state=42
    ).execute(
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

    imputer = MICEImputer()

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

    result = MICEImputer().execute(
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

    result = MICEImputer().execute(
        dataframe=df
    )

    assert result.strategy == "MICE"


def test_deterministic_with_random_state():

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
                None,
                40.0,
                50.0,
            ],
            "z": [
                5.0,
                10.0,
                15.0,
                20.0,
                25.0,
            ],
        }
    )

    result_1 = MICEImputer(
        random_state=42
    ).execute(
        dataframe=df
    )

    result_2 = MICEImputer(
        random_state=42
    ).execute(
        dataframe=df
    )

    pd.testing.assert_frame_equal(
        result_1.dataframe,
        result_2.dataframe,
    )
