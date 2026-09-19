import numpy as np
import pandas as pd
import pytest

from emidaf_core.missing.missing_pipeline import (
    MissingPipeline,
    MissingPipelineResult,
)


# =========================================================
# VALIDATION
# =========================================================


def test_invalid_dataframe():

    pipeline = MissingPipeline()

    with pytest.raises(
        TypeError
    ):
        pipeline.run(
            dataframe=[]
        )


def test_invalid_apply_imputation():

    pipeline = MissingPipeline()

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    with pytest.raises(
        TypeError
    ):
        pipeline.run(
            dataframe=df,
            apply_imputation="yes",
        )


def test_invalid_copy_input():

    pipeline = MissingPipeline()

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    with pytest.raises(
        TypeError
    ):
        pipeline.run(
            dataframe=df,
            copy_input="yes",
        )


# =========================================================
# NO MISSING VALUES
# =========================================================


def test_pipeline_without_missing_values():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                30.0,
                40.0,
                50.0,
            ],
            "score": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
        }
    )

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df
    )

    assert isinstance(
        result,
        MissingPipelineResult,
    )

    assert result.success is True

    assert result.applied is True

    assert (
        result.total_values_imputed
        == 0
    )

    assert (
        result.dataframe
        .isna()
        .sum()
        .sum()
        == 0
    )


# =========================================================
# ANALYSIS ONLY
# =========================================================


def test_analysis_only():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
                50.0,
            ],
            "score": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
        }
    )

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df,
        apply_imputation=False,
    )

    assert result.success is True

    assert result.applied is False

    assert result.execution is None

    assert (
        result.dataframe[
            "age"
        ]
        .isna()
        .sum()
        == 1
    )


# =========================================================
# MEAN IMPUTATION
# =========================================================


def test_real_pipeline_mean_imputation():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                10,
                100,
                n,
            ),
        }
    )

    # 3 % missing
    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df
    )

    assert result.success is True

    assert result.applied is True

    assert (
        result.dataframe[
            "age"
        ]
        .isna()
        .sum()
        == 0
    )

    assert (
        result.total_values_imputed
        >= 3
    )


# =========================================================
# KNN
# =========================================================


def test_real_pipeline_knn():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
            "score": np.linspace(
                0,
                100,
                n,
            ),
        }
    )

    # 10 % missing -> KNN
    df.loc[
        list(
            range(
                10
            )
        ),
        "income",
    ] = np.nan

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df
    )

    assert result.success is True

    assert (
        result.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 0
    )

    assert (
        result.total_values_imputed
        >= 10
    )


# =========================================================
# MICE
# =========================================================


def test_real_pipeline_mice():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
            "score": np.linspace(
                0,
                100,
                n,
            ),
        }
    )

    # 25 % missing -> MICE
    df.loc[
        list(
            range(
                25
            )
        ),
        "income",
    ] = np.nan

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df
    )

    assert result.success is True

    assert (
        result.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 0
    )

    assert (
        result.total_values_imputed
        >= 25
    )


# =========================================================
# REVIEW
# =========================================================


def test_real_pipeline_review():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
        }
    )

    # 50 % missing -> REVIEW
    df.loc[
        list(
            range(
                50
            )
        ),
        "income",
    ] = np.nan

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df
    )

    assert result.success is True

    assert (
        result.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 50
    )

    assert (
        "income"
        in result.review_required
    )


# =========================================================
# ORIGINAL DATAFRAME
# =========================================================


def test_original_dataframe_is_not_modified():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                10,
                100,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    original = df.copy(
        deep=True
    )

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df
    )

    pd.testing.assert_frame_equal(
        df,
        original,
    )

    assert (
        result.dataframe[
            "age"
        ]
        .isna()
        .sum()
        == 0
    )


# =========================================================
# REPORT AND PLAN
# =========================================================


def test_pipeline_exposes_report_and_plan():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
                50.0,
            ],
            "score": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
        }
    )

    pipeline = MissingPipeline()

    result = pipeline.run(
        dataframe=df,
        apply_imputation=False,
    )

    assert isinstance(
        result.report,
        dict,
    )

    assert result.plan is not None

    assert (
        "imputation_candidates"
        in result.report
    )


# =========================================================
# SUMMARY / AUDIT
# =========================================================


def test_summary_structure():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                10,
                100,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df
        )
    )

    summary = result.summary()

    assert isinstance(
        summary,
        dict,
    )

    assert (
        summary[
            "success"
        ]
        is True
    )

    assert (
        summary[
            "rows"
        ]
        == 100
    )

    assert (
        summary[
            "columns"
        ]
        == 2
    )

    assert (
        summary[
            "initial_missing_values"
        ]
        == 3
    )

    assert (
        summary[
            "final_missing_values"
        ]
        == 0
    )

    assert (
        summary[
            "total_values_imputed"
        ]
        == 3
    )


def test_missing_values_reduction():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                0,
                1,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df
        )
    )

    assert (
        result.initial_missing_values
        == 3
    )

    assert (
        result.final_missing_values
        == 0
    )

    assert (
        result.missing_values_reduction
        == 3
    )


def test_summary_contains_strategies():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                10,
                100,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    summary = result.summary()

    assert (
        "strategies"
        in summary
    )

    assert (
        summary[
            "strategies"
        ][
            "age"
        ]
        == "MEAN"
    )


def test_summary_review_variable():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
        }
    )

    df.loc[
        list(
            range(
                50
            )
        ),
        "income",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df
        )
    )

    summary = result.summary()

    assert (
        "income"
        in summary[
            "review_required"
        ]
    )

    assert (
        summary[
            "strategies"
        ][
            "income"
        ]
        == "REVIEW"
    )


def test_to_dict():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    result = (
        MissingPipeline()
        .run(
            dataframe=df
        )
    )

    data = result.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert (
        "summary"
        in data
    )

    assert (
        "report"
        in data
    )

    assert (
        "plan"
        in data
    )


def test_analysis_only_summary():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
                50.0,
            ]
        }
    )

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    summary = result.summary()

    assert (
        summary[
            "imputation_applied"
        ]
        is False
    )

    assert (
        summary[
            "initial_missing_values"
        ]
        == 1
    )

    assert (
        summary[
            "final_missing_values"
        ]
        == 1
    )

    assert (
        summary[
            "total_values_imputed"
        ]
        == 0
    )

# =========================================================
# SUMMARY DATAFRAME
# =========================================================


def test_summary_dataframe_structure():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                10,
                100,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    table = (
        result.summary_dataframe()
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )

    assert list(
        table.columns
    ) == [
        "column",
        "missing_rate",
        "strategy",
        "predictors",
        "applicable",
        "review_required",
        "parameters",
    ]


def test_summary_dataframe_mean():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                10,
                100,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    table = (
        result.summary_dataframe()
    )

    age_row = (
        table[
            table[
                "column"
            ]
            == "age"
        ]
        .iloc[
            0
        ]
    )

    assert (
        age_row[
            "missing_rate"
        ]
        == 3.0
    )

    assert (
        age_row[
            "strategy"
        ]
        == "MEAN"
    )

    assert (
        bool(
            age_row[
                "applicable"
            ]
        )
        is True
    )

    assert (
        bool(
            age_row[
                "review_required"
            ]
        )
        is False
    )


def test_summary_dataframe_knn_predictors():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
            "score": np.linspace(
                0,
                100,
                n,
            ),
        }
    )

    df.loc[
        list(
            range(
                10
            )
        ),
        "income",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    table = (
        result.summary_dataframe()
    )

    income_row = (
        table[
            table[
                "column"
            ]
            == "income"
        ]
        .iloc[
            0
        ]
    )

    assert (
        income_row[
            "strategy"
        ]
        == "KNN"
    )

    assert isinstance(
        income_row[
            "predictors"
        ],
        list,
    )

    assert len(
        income_row[
            "predictors"
        ]
    ) >= 1

    assert (
        "income"
        not in income_row[
            "predictors"
        ]
    )


def test_summary_dataframe_review():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
        }
    )

    df.loc[
        list(
            range(
                50
            )
        ),
        "income",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    table = (
        result.summary_dataframe()
    )

    income_row = (
        table[
            table[
                "column"
            ]
            == "income"
        ]
        .iloc[
            0
        ]
    )

    assert (
        income_row[
            "strategy"
        ]
        == "REVIEW"
    )

    assert (
        bool(
            income_row[
                "applicable"
            ]
        )
        is False
    )

    assert (
        bool(
            income_row[
                "review_required"
            ]
        )
        is True
    )


def test_summary_dataframe_parameters():

    n = 100

    df = pd.DataFrame(
        {
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "age": np.linspace(
                20,
                65,
                n,
            ),
        }
    )

    df.loc[
        list(
            range(
                10
            )
        ),
        "income",
    ] = np.nan

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    table = (
        result.summary_dataframe()
    )

    income_row = (
        table[
            table[
                "column"
            ]
            == "income"
        ]
        .iloc[
            0
        ]
    )

    parameters = (
        income_row[
            "parameters"
        ]
    )

    assert isinstance(
        parameters,
        dict,
    )

    assert (
        parameters[
            "n_neighbors"
        ]
        == 5
    )


def test_summary_dataframe_no_missing():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                30.0,
                40.0,
            ],
            "score": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    result = (
        MissingPipeline()
        .run(
            dataframe=df,
            apply_imputation=False,
        )
    )

    table = (
        result.summary_dataframe()
    )

    assert len(
        table
    ) == 2

    assert set(
        table[
            "strategy"
        ]
    ) == {
        "NONE"
    }
