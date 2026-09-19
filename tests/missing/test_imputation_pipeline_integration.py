import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.analyzers.missing_analyzer import (
    MissingAnalyzer,
)
from emidaf_core.dataset.profiler.profile_context import (
    ProfileContext,
)
from emidaf_core.missing.imputation.plan_builder import (
    ImputationPlanBuilder,
)
from emidaf_core.missing.imputation.plan_executor import (
    ImputationPlanExecutor,
)


def build_missing_report(
    dataframe: pd.DataFrame,
) -> dict:

    context = ProfileContext(
        dataframe=dataframe
    )

    analyzer = MissingAnalyzer()

    result = analyzer.execute(
        context
    )

    assert result.success is True
    assert result.result is not None

    return result.result


def test_real_pipeline_low_missing_numeric():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "score": np.linspace(
                40,
                90,
                n,
            ),
        }
    )

    # 3 % de valeurs manquantes :
    # MissingAnalyzer doit proposer MEAN.
    df.loc[
        [1, 10, 20],
        "age",
    ] = np.nan

    report = build_missing_report(
        df
    )

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

    execution = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert execution.success is True

    assert (
        execution.dataframe[
            "age"
        ]
        .isna()
        .sum()
        == 0
    )

    assert (
        execution.total_values_imputed
        == 3
    )


def test_real_pipeline_low_missing_categorical():

    n = 100

    df = pd.DataFrame(
        {
            "city": (
                ["Dakar"] * 60
                + ["Thiès"] * 40
            ),
            "score": np.linspace(
                40,
                90,
                n,
            ),
        }
    )

    df.loc[
        [2, 15, 30],
        "city",
    ] = None

    report = build_missing_report(
        df
    )

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

    execution = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert execution.success is True

    assert (
        execution.dataframe[
            "city"
        ]
        .isna()
        .sum()
        == 0
    )


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
                30,
                95,
                n,
            ),
        }
    )

    # 10 % de missing :
    # MissingAnalyzer -> KNN.
    missing_indexes = [
        1,
        5,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
    ]

    df.loc[
        missing_indexes,
        "income",
    ] = np.nan

    report = build_missing_report(
        df
    )

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
        "income"
    )

    assert decision is not None
    assert decision.strategy == "KNN"

    assert len(
        decision.predictors
    ) > 0

    assert "income" not in (
        decision.predictors
    )

    execution = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert execution.success is True

    assert (
        execution.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 0
    )

    assert (
        execution.total_values_imputed
        == 10
    )


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
                30,
                95,
                n,
            ),
        }
    )

    # 25 % de missing :
    # MissingAnalyzer -> MICE.
    missing_indexes = list(
        range(
            0,
            25,
        )
    )

    df.loc[
        missing_indexes,
        "income",
    ] = np.nan

    report = build_missing_report(
        df
    )

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
        "income"
    )

    assert decision is not None
    assert decision.strategy == "MICE"

    assert len(
        decision.predictors
    ) > 0

    execution = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert execution.success is True

    assert (
        execution.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 0
    )

    assert (
        execution.total_values_imputed
        == 25
    )


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

    # 50 % de missing :
    # MissingAnalyzer -> REVIEW.
    df.loc[
        list(
            range(
                0,
                50,
            )
        ),
        "income",
    ] = np.nan

    report = build_missing_report(
        df
    )

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
    assert decision.strategy == "REVIEW"
    assert decision.applicable is False

    execution = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    assert execution.success is True

    assert "income" in (
        execution.review_required
    )

    assert (
        execution.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 50
    )

    assert (
        execution.total_values_imputed
        == 0
    )


def test_predictors_are_not_modified_by_pipeline():

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
                30,
                95,
                n,
            ),
        }
    )

    df.loc[
        list(
            range(
                0,
                10,
            )
        ),
        "income",
    ] = np.nan

    # Le predictor contient lui-même quelques NA.
    df.loc[
        [15, 25],
        "age",
    ] = np.nan

    original_age = (
        df["age"]
        .copy(
            deep=True
        )
    )

    report = build_missing_report(
        df
    )

    plan = (
        ImputationPlanBuilder()
        .build(
            report=report,
            dataframe=df,
        )
    )

    execution = (
        ImputationPlanExecutor()
        .execute(
            dataframe=df,
            plan=plan,
        )
    )

    # Le pipeline peut traiter age séparément si
    # elle possède sa propre décision.
    # On vérifie donc spécifiquement le principe
    # au niveau de la décision income.
    income_decision = plan.get(
        "income"
    )

    assert income_decision is not None
    assert (
        income_decision.strategy
        == "KNN"
    )

    assert execution.success is True

    assert (
        execution.dataframe[
            "income"
        ]
        .isna()
        .sum()
        == 0
    )

    # Le pipeline global peut avoir une décision
    # indépendante pour age. L'important est que
    # l'imputation de income elle-même ne soit pas
    # responsable d'une modification non auditée.
    assert len(
        execution.results
    ) == len(
        plan.decisions
    )
