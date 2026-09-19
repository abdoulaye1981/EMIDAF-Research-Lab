import pandas as pd
import pytest

from emidaf_core.missing.imputation.plan_builder import (
    ImputationPlanBuilder,
)
from emidaf_core.missing.imputation.imputation_plan import (
    ImputationPlan,
)


def test_builder_creation():

    builder = ImputationPlanBuilder()

    assert builder.max_predictors == 5


def test_custom_max_predictors():

    builder = ImputationPlanBuilder(
        max_predictors=3
    )

    assert builder.max_predictors == 3


def test_invalid_max_predictors_type():

    with pytest.raises(TypeError):

        ImputationPlanBuilder(
            max_predictors=2.5
        )


def test_invalid_max_predictors_value():

    with pytest.raises(ValueError):

        ImputationPlanBuilder(
            max_predictors=0
        )


def test_invalid_report():

    builder = ImputationPlanBuilder()

    with pytest.raises(TypeError):

        builder.build(
            report=[],
            dataframe=pd.DataFrame(),
        )


def test_invalid_dataframe():

    builder = ImputationPlanBuilder()

    with pytest.raises(TypeError):

        builder.build(
            report={},
            dataframe=[],
        )


def test_empty_candidates():

    builder = ImputationPlanBuilder()

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    plan = builder.build(
        report={
            "imputation_candidates": {}
        },
        dataframe=df,
    )

    assert isinstance(
        plan,
        ImputationPlan,
    )

    assert plan.decisions == []


def test_mean_decision():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "age": {
                "strategy": "MEAN"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "age"
    )

    assert decision is not None
    assert decision.strategy == "MEAN"
    assert decision.predictors == []


def test_mode_decision():

    df = pd.DataFrame(
        {
            "city": [
                "Dakar",
                None,
                "Dakar",
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "city": {
                "strategy": "MODE"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "city"
    )

    assert decision is not None
    assert decision.strategy == "MODE"


def test_string_candidate():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "age": "MEAN"
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    assert (
        plan.get(
            "age"
        ).strategy
        == "MEAN"
    )


def test_knn_predictor_selection():

    df = pd.DataFrame(
        {
            "income": [
                100.0,
                None,
                300.0,
                400.0,
                500.0,
            ],
            "age": [
                20.0,
                30.0,
                40.0,
                50.0,
                60.0,
            ],
            "score": [
                10.0,
                20.0,
                30.0,
                40.0,
                50.0,
            ],
        }
    )

    report = {
        "imputation_candidates": {
            "income": {
                "strategy": "KNN"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "income"
    )

    assert decision is not None
    assert decision.strategy == "KNN"

    assert set(
        decision.predictors
    ) == {
        "age",
        "score",
    }

    assert (
        decision.parameters[
            "n_neighbors"
        ]
        == 5
    )


def test_mice_predictor_selection():

    df = pd.DataFrame(
        {
            "score": [
                10.0,
                None,
                30.0,
                40.0,
                50.0,
            ],
            "age": [
                20.0,
                30.0,
                40.0,
                50.0,
                60.0,
            ],
            "income": [
                100.0,
                200.0,
                300.0,
                400.0,
                500.0,
            ],
        }
    )

    report = {
        "imputation_candidates": {
            "score": {
                "strategy": "MICE"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "score"
    )

    assert decision is not None
    assert decision.strategy == "MICE"

    assert len(
        decision.predictors
    ) == 2

    assert (
        decision.parameters[
            "random_state"
        ]
        == 42
    )


def test_multivariate_without_predictor_becomes_review():

    df = pd.DataFrame(
        {
            "income": [
                100.0,
                None,
                300.0,
            ],
            "city": [
                "Dakar",
                "Thiès",
                "Dakar",
            ],
        }
    )

    report = {
        "imputation_candidates": {
            "income": {
                "strategy": "KNN"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "income"
    )

    assert decision.strategy == "REVIEW"
    assert decision.applicable is False
    assert decision.predictors == []


def test_high_missing_review():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                None,
                None,
                5.0,
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "x": {
                "strategy": "REVIEW"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "x"
    )

    assert decision.strategy == "REVIEW"
    assert decision.applicable is False
    assert decision.missing_rate == 60.0


def test_none_decision():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "x": {
                "strategy": "NONE"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "x"
    )

    assert decision.strategy == "NONE"
    assert decision.missing_rate == 0.0


def test_unknown_report_column_is_ignored():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "unknown": {
                "strategy": "MEAN"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    assert plan.decisions == []


def test_predictor_limit():

    df = pd.DataFrame(
        {
            "target": [
                1.0,
                None,
                3.0,
                4.0,
                5.0,
            ],
            "x1": [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
            ],
            "x2": [
                2.0,
                4.0,
                6.0,
                8.0,
                10.0,
            ],
            "x3": [
                5.0,
                4.0,
                3.0,
                2.0,
                1.0,
            ],
        }
    )

    report = {
        "imputation_candidates": {
            "target": {
                "strategy": "KNN"
            }
        }
    }

    plan = (
        ImputationPlanBuilder(
            max_predictors=2
        )
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "target"
    )

    assert len(
        decision.predictors
    ) == 2


def test_all_missing_predictor_is_excluded():

    df = pd.DataFrame(
        {
            "target": [
                1.0,
                None,
                3.0,
                4.0,
            ],
            "good": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
            "empty": [
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
            ],
        }
    )

    report = {
        "imputation_candidates": {
            "target": {
                "strategy": "KNN"
            }
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "target"
    )

    assert "good" in (
        decision.predictors
    )

    assert "empty" not in (
        decision.predictors
    )


def test_plan_metadata():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    report = {
        "imputation_candidates": {
            "x": "MEAN"
        }
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    assert (
        plan.source
        == "MissingAnalyzer"
    )

    assert (
        plan.generated_automatically
        is True
    )

def test_real_analyzer_list_format():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ],
            "score": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    report = {
        "imputation_candidates": [
            {
                "column": "age",
                "dtype": "float64",
                "missing_percentage": 33.33,
                "recommended_strategy": "Mean",
            },
            {
                "column": "score",
                "dtype": "float64",
                "missing_percentage": 0.0,
                "recommended_strategy": "None",
            },
        ]
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    assert (
        plan.get(
            "age"
        ).strategy
        == "MEAN"
    )

    assert (
        plan.get(
            "score"
        ).strategy
        == "NONE"
    )


def test_real_analyzer_knn_list_format():

    df = pd.DataFrame(
        {
            "income": [
                100.0,
                None,
                300.0,
                400.0,
            ],
            "age": [
                20.0,
                30.0,
                40.0,
                50.0,
            ],
        }
    )

    report = {
        "imputation_candidates": [
            {
                "column": "income",
                "dtype": "float64",
                "missing_percentage": 25.0,
                "recommended_strategy": "KNN",
            }
        ]
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "income"
    )

    assert decision is not None
    assert decision.strategy == "KNN"

    assert "age" in (
        decision.predictors
    )


def test_invalid_list_candidate_type():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    report = {
        "imputation_candidates": [
            "invalid"
        ]
    }

    with pytest.raises(TypeError):

        ImputationPlanBuilder().build(
            report=report,
            dataframe=df,
        )


def test_list_candidate_requires_column():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                None,
                3.0,
            ]
        }
    )

    report = {
        "imputation_candidates": [
            {
                "recommended_strategy":
                    "Mean"
            }
        ]
    }

    with pytest.raises(ValueError):

        ImputationPlanBuilder().build(
            report=report,
            dataframe=df,
        )
def test_review_variable_alias_is_normalized():

    df = pd.DataFrame(
        {
            "income": [
                100.0,
                None,
                None,
                400.0,
            ]
        }
    )

    report = {
        "imputation_candidates": [
            {
                "column": "income",
                "dtype": "float64",
                "missing_percentage": 50.0,
                "recommended_strategy":
                    "Review Variable",
            }
        ]
    }

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    decision = plan.get(
        "income"
    )

    assert decision is not None

    assert (
        decision.strategy
        == "REVIEW"
    )

    assert (
        decision.applicable
        is False
    )


def test_strategy_alias_normalization():

    builder = (
        ImputationPlanBuilder()
    )

    assert (
        builder._normalize_strategy(
            "Mean"
        )
        == "MEAN"
    )

    assert (
        builder._normalize_strategy(
            "Review Variable"
        )
        == "REVIEW"
    )

    assert (
        builder._normalize_strategy(
            "None"
        )
        == "NONE"
    )
