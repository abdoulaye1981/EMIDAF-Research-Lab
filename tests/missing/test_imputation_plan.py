import pytest

from emidaf_core.missing.imputation.imputation_plan import (
    ColumnImputationDecision,
    ImputationPlan,
)


def test_decision_creation():

    decision = ColumnImputationDecision(
        column="age",
        strategy="MEAN",
        reason="Low missing rate.",
        missing_rate=3.5,
        confidence=0.8,
    )

    assert decision.column == "age"
    assert decision.strategy == "MEAN"
    assert decision.missing_rate == 3.5
    assert decision.confidence == 0.8


def test_strategy_is_normalized():

    decision = ColumnImputationDecision(
        column="age",
        strategy="mean",
        reason="Test.",
        missing_rate=2.0,
    )

    assert decision.strategy == "MEAN"


def test_invalid_strategy():

    with pytest.raises(ValueError):

        ColumnImputationDecision(
            column="age",
            strategy="INVALID",
            reason="Test.",
            missing_rate=2.0,
        )


def test_invalid_missing_rate():

    with pytest.raises(ValueError):

        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Test.",
            missing_rate=120.0,
        )


def test_invalid_confidence():

    with pytest.raises(ValueError):

        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Test.",
            missing_rate=10.0,
            confidence=1.5,
        )


def test_plan_creation():

    plan = ImputationPlan()

    assert plan.decisions == []
    assert plan.source == "EMIDAF"
    assert (
        plan.generated_automatically
        is True
    )


def test_add_decision():

    plan = ImputationPlan()

    decision = ColumnImputationDecision(
        column="age",
        strategy="MEAN",
        reason="Low missing rate.",
        missing_rate=4.0,
    )

    plan.add(
        decision
    )

    assert len(
        plan.decisions
    ) == 1


def test_duplicate_column_rejected():

    plan = ImputationPlan()

    decision_1 = (
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Test.",
            missing_rate=4.0,
        )
    )

    decision_2 = (
        ColumnImputationDecision(
            column="age",
            strategy="KNN",
            reason="Test.",
            missing_rate=8.0,
        )
    )

    plan.add(
        decision_1
    )

    with pytest.raises(ValueError):

        plan.add(
            decision_2
        )


def test_get_decision():

    plan = ImputationPlan()

    decision = ColumnImputationDecision(
        column="income",
        strategy="KNN",
        reason="Moderate missing rate.",
        missing_rate=12.0,
    )

    plan.add(
        decision
    )

    result = plan.get(
        "income"
    )

    assert result is not None
    assert result.strategy == "KNN"


def test_get_unknown_column():

    plan = ImputationPlan()

    assert (
        plan.get(
            "unknown"
        )
        is None
    )


def test_strategies_mapping():

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Test.",
            missing_rate=2.0,
        )
    )

    plan.add(
        ColumnImputationDecision(
            column="city",
            strategy="MODE",
            reason="Test.",
            missing_rate=3.0,
        )
    )

    assert plan.strategies() == {
        "age": "MEAN",
        "city": "MODE",
    }


def test_actionable_decisions():

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Test.",
            missing_rate=2.0,
        )
    )

    plan.add(
        ColumnImputationDecision(
            column="comment",
            strategy="REVIEW",
            reason="Too much missing data.",
            missing_rate=70.0,
        )
    )

    actionable = (
        plan.actionable()
    )

    assert len(
        actionable
    ) == 1

    assert (
        actionable[0].column
        == "age"
    )


def test_review_required():

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="comment",
            strategy="REVIEW",
            reason="High missingness.",
            missing_rate=60.0,
        )
    )

    review = (
        plan.review_required()
    )

    assert len(
        review
    ) == 1

    assert (
        review[0].column
        == "comment"
    )


def test_to_dict():

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="age",
            strategy="MEAN",
            reason="Low missing rate.",
            missing_rate=4.0,
            confidence=0.75,
            parameters={
                "example": True
            },
        )
    )

    result = plan.to_dict()

    assert (
        result["source"]
        == "EMIDAF"
    )

    assert len(
        result["decisions"]
    ) == 1

    assert (
        result["decisions"][0][
            "column"
        ]
        == "age"
    )

    assert (
        result["decisions"][0][
            "strategy"
        ]
        == "MEAN"
    )

def test_predictors_creation():

    decision = ColumnImputationDecision(
        column="income",
        strategy="KNN",
        reason="Use observed predictors.",
        missing_rate=15.0,
        predictors=[
            "age",
            "score",
        ],
    )

    assert decision.predictors == [
        "age",
        "score",
    ]


def test_predictors_default_empty():

    decision = ColumnImputationDecision(
        column="age",
        strategy="MEAN",
        reason="Test.",
        missing_rate=5.0,
    )

    assert decision.predictors == []


def test_predictors_must_be_list():

    with pytest.raises(TypeError):

        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=10.0,
            predictors="age",
        )


def test_predictor_must_be_string():

    with pytest.raises(TypeError):

        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=10.0,
            predictors=[
                "age",
                123,
            ],
        )


def test_target_cannot_be_predictor():

    with pytest.raises(ValueError):

        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=10.0,
            predictors=[
                "age",
                "income",
            ],
        )


def test_empty_predictor_rejected():

    with pytest.raises(ValueError):

        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=10.0,
            predictors=[
                "",
            ],
        )


def test_predictors_are_normalized():

    decision = ColumnImputationDecision(
        column="income",
        strategy="KNN",
        reason="Test.",
        missing_rate=10.0,
        predictors=[
            " age ",
            " score ",
        ],
    )

    assert decision.predictors == [
        "age",
        "score",
    ]


def test_duplicate_predictors_removed():

    decision = ColumnImputationDecision(
        column="income",
        strategy="KNN",
        reason="Test.",
        missing_rate=10.0,
        predictors=[
            "age",
            "age",
            "score",
        ],
    )

    assert decision.predictors == [
        "age",
        "score",
    ]


def test_predictors_in_to_dict():

    plan = ImputationPlan()

    plan.add(
        ColumnImputationDecision(
            column="income",
            strategy="KNN",
            reason="Test.",
            missing_rate=10.0,
            predictors=[
                "age",
                "score",
            ],
            parameters={
                "n_neighbors": 3,
            },
        )
    )

    result = plan.to_dict()

    assert (
        result["decisions"][0][
            "predictors"
        ]
        == [
            "age",
            "score",
        ]
    )
