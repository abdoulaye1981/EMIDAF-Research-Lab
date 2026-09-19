from emidaf_core.missing import (
    ColumnImputationDecision,
    ImputationPlan,
    ImputationPlanBuilder,
    ImputationPlanExecutor,
    KNNImputer,
    MICEImputer,
    MissingImputer,
    MissingPipeline,
    MissingPipelineResult,
    SimpleImputer,
)


def test_missing_public_api_imports():

    objects = [
        MissingPipeline,
        MissingPipelineResult,
        ColumnImputationDecision,
        ImputationPlan,
        ImputationPlanBuilder,
        ImputationPlanExecutor,
        MissingImputer,
        SimpleImputer,
        KNNImputer,
        MICEImputer,
    ]

    for obj in objects:
        assert obj is not None


def test_missing_pipeline_public_api():

    pipeline = MissingPipeline()

    assert isinstance(
        pipeline,
        MissingPipeline,
    )
