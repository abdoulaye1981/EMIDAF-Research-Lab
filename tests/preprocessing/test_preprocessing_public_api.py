from __future__ import annotations

import emidaf_core.preprocessing as preprocessing


PUBLIC_SYMBOLS = [
    "BasePreprocessor",
    "BasePreprocessing",
    "PreprocessingResult",
    "PreprocessingPipeline",
    "ConditionalPipeline",
    "Encoding",
    "Encoder",
    "OutlierDetection",
    "Outliers",
    "Categorical",
    "Cleaning",
    "DateTime",
    "Dimensionality",
    "FeatureExtraction",
    "Imputation",
    "Normalization",
    "Numerical",
    "Sampling",
    "Text",
    "Validation",
]


def test_public_api_symbols_exist():

    missing = [
        name
        for name in PUBLIC_SYMBOLS
        if not hasattr(
            preprocessing,
            name,
        )
    ]

    assert missing == []


def test_core_public_api_is_importable():

    from emidaf_core.preprocessing import (
        BasePreprocessor,
        BasePreprocessing,
        PreprocessingResult,
        PreprocessingPipeline,
        ConditionalPipeline,
        Encoding,
        Encoder,
        Imputation,
        Outliers,
    )

    assert BasePreprocessor is not None
    assert BasePreprocessing is not None
    assert PreprocessingResult is not None
    assert PreprocessingPipeline is not None
    assert ConditionalPipeline is not None
    assert Encoding is not None
    assert Encoder is not None
    assert Imputation is not None
    assert Outliers is not None


def test_missforest_is_not_exposed():

    from emidaf_core.preprocessing import Imputation

    assert "missforest" not in (
        Imputation.registry
    )


def test_conditional_pipeline_is_public():

    assert hasattr(
        preprocessing,
        "ConditionalPipeline",
    )
