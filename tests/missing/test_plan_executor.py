import pandas as pd
import pytest

from emidaf_core.missing.imputation.imputation_plan import (
    ColumnImputationDecision,
    ImputationPlan,
)
from emidaf_core.missing.imputation.plan_executor import (
    ImputationPlanExecutor,
    PlanExecutionResult,
)


def build_plan():

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Low missing rate.",
            missing_rate=10.0,
        )
    )

    plan.add(
        ColumnImputationDecision(
            column="city",
            strategy="MODE",
            reason="Categorical variable.",
            missing_rate=10.0,
        )
    )

    return plan


def test_executor_creation():

    executor = ImputationPlanExecutor()

    assert executor is not None


def test_invalid_dataframe():

    executor = ImputationPlanExecutor()

    with pytest.raises(TypeError):

        executor.execute(
            dataframe=[1, 2, 3],
            plan=ImputationPlan(),
        )


def test_invalid_plan():

    executor = ImputationPlanExecutor()

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

        executor.execute(
            dataframe=df,
            plan={},
        )


def test_execute_mean_and_mode():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ],
            "city": [
                "Dakar",
                None,
                "Dakar",
            ],
        }
    )

    plan = build_plan()

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert isinstance(
        result,
        PlanExecutionResult,
    )

    assert result.success is True

    assert (
        result.dataframe["age"]
        .isna()
        .sum()
        == 0
    )

    assert (
        result.dataframe["city"]
        .isna()
        .sum()
        == 0
    )

    assert result.total_values_imputed == 2


def test_original_dataframe_not_modified():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ],
            "city": [
                "Dakar",
                None,
                "Dakar",
            ],
        }
    )

    original = df.copy(
        deep=True
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=build_plan(),
        )
    )

    assert df.equals(
        original
    )

    assert (
        result.dataframe["age"]
        .isna()
        .sum()
        == 0
    )


def test_review_is_preserved():

    df = pd.DataFrame(
        {
            "comment": [
                "ok",
                None,
                None,
            ]
        }
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="comment",
            strategy="REVIEW",
            reason="High missingness.",
            missing_rate=66.67,
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.success is True

    assert result.review_required == [
        "comment"
    ]

    assert (
        result.dataframe["comment"]
        .isna()
        .sum()
        == 2
    )

    assert result.total_values_imputed == 0


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

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="x",
            strategy="NONE",
            reason="No missing values.",
            missing_rate=0.0,
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.success is True

    assert result.total_values_imputed == 0


def test_missing_column_generates_error():

    df = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
            ]
        }
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="unknown",
            strategy="MEAN",
            reason="Test.",
            missing_rate=10.0,
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.success is False

    assert len(
        result.errors
    ) == 1

    assert (
        result.results[0].success
        is False
    )


def test_execution_error_does_not_stop_plan():

    df = pd.DataFrame(
        {
            "city": [
                "Dakar",
                None,
                "Thiès",
            ],
            "age": [
                20.0,
                None,
                40.0,
            ],
        }
    )

    plan = ImputationPlan()

    # Erreur volontaire :
    # MEAN sur variable catégorielle.
    plan.add(
        ColumnImputationDecision(
            column="city",
            strategy="MEAN",
            reason="Invalid test.",
            missing_rate=10.0,
        )
    )

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Valid strategy.",
            missing_rate=10.0,
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.success is False

    assert len(
        result.errors
    ) == 1

    # age doit quand même être traitée.
    assert (
        result.dataframe["age"]
        .isna()
        .sum()
        == 0
    )


def test_parameters_are_forwarded():

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

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="x",
            strategy="KNN",
            reason="Moderate missingness.",
            missing_rate=25.0,
            parameters={
                "n_neighbors": 2,
                "weights": "distance",
            },
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.success is True

    assert (
        result.dataframe["x"]
        .isna()
        .sum()
        == 0
    )


def test_result_count_matches_plan():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ],
            "city": [
                "Dakar",
                None,
                "Dakar",
            ],
        }
    )

    plan = build_plan()

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert len(
        result.results
    ) == len(
        plan.decisions
    )


def test_values_imputed_by_column():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                None,
                40.0,
            ]
        }
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Test.",
            missing_rate=50.0,
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.total_values_imputed == 2

    assert (
        result.results[0]
        .values_imputed
        == 2
    )


def test_knn_uses_predictors():

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
            "score": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
        }
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Use correlated predictors.",
            missing_rate=25.0,
            predictors=[
                "age",
                "score",
            ],
            parameters={
                "n_neighbors": 2,
            },
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
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
        result.results[0]
        .details[
            "predictors"
        ]
        == [
            "age",
            "score",
        ]
    )


def test_mice_uses_predictors():

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

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="income",
            strategy="MICE",
            reason="Multivariate imputation.",
            missing_rate=20.0,
            predictors=[
                "age",
                "score",
            ],
            parameters={
                "random_state": 42,
            },
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
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


def test_predictor_missing_values_are_not_reinjected():

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
                None,
                40.0,
                50.0,
            ],
        }
    )

    original_age = (
        df["age"]
        .copy(
            deep=True
        )
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Use age as predictor.",
            missing_rate=25.0,
            predictors=[
                "age"
            ],
            parameters={
                "n_neighbors": 2,
            },
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    # income est imputée
    assert (
        result.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 0
    )

    # age reste exactement comme avant
    pd.testing.assert_series_equal(
        result.dataframe[
            "age"
        ],
        original_age,
    )


def test_unknown_predictor_generates_error():

    df = pd.DataFrame(
        {
            "income": [
                100.0,
                None,
                300.0,
            ]
        }
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=33.33,
            predictors=[
                "age"
            ],
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert result.success is False

    assert len(
        result.errors
    ) == 1

    assert (
        "unknown predictor"
        in result.errors[0]
    )


def test_mean_ignores_predictors_for_execution():

    df = pd.DataFrame(
        {
            "age": [
                20.0,
                None,
                40.0,
            ],
            "score": [
                1.0,
                None,
                3.0,
            ],
        }
    )

    original_score = (
        df["score"]
        .copy(
            deep=True
        )
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Simple imputation.",
            missing_rate=33.33,
            predictors=[
                "score"
            ],
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert (
        result.dataframe[
            "age"
        ]
        .isna()
        .sum()
        == 0
    )

    pd.testing.assert_series_equal(
        result.dataframe[
            "score"
        ],
        original_score,
    )


def test_total_values_imputed_counts_target_only():

    df = pd.DataFrame(
        {
            "income": [
                100.0,
                None,
                None,
                400.0,
            ],
            "age": [
                20.0,
                None,
                40.0,
                50.0,
            ],
        }
    )

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=50.0,
            predictors=[
                "age"
            ],
            parameters={
                "n_neighbors": 2,
            },
        )
    )

    result = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert (
        result.total_values_imputed
        == 2
    )

    assert (
        result.results[0]
        .values_imputed
        == 2
    )
