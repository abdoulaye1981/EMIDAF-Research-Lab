"""
=========================================================
EMIDAF Framework
Tests - Ensemble Outlier Detection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.ensemble import (
    EllipticEnvelopeDetector,
    IsolationForestDetector,
    OneClassSVMDetector,
)


# =========================================================
# FIXTURE
# =========================================================


@pytest.fixture
def ensemble_dataframe() -> pd.DataFrame:
    """
    Dataset bidimensionnel avec un point très isolé.
    """

    rng = np.random.default_rng(42)

    normal = rng.normal(
        loc=0.0,
        scale=0.30,
        size=(200, 2),
    )

    dataframe = pd.DataFrame(
        normal,
        columns=[
            "x1",
            "x2",
        ],
        index=[
            f"row_{i}"
            for i in range(200)
        ],
    )

    dataframe.loc[
        "row_OUTLIER"
    ] = [
        8.0,
        8.0,
    ]

    return dataframe


# =========================================================
# DETECTOR CONFIGURATION
# =========================================================


DETECTORS = [
    (
        IsolationForestDetector,
        {
            "contamination": 0.05,
            "random_state": 42,
        },
    ),
    (
        OneClassSVMDetector,
        {
            "nu": 0.05,
            "kernel": "rbf",
        },
    ),
    (
        EllipticEnvelopeDetector,
        {
            "contamination": 0.05,
        },
    ),
]


# =========================================================
# OUTLIER DETECTION
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_detects_extreme_point(
    detector,
    kwargs,
    ensemble_dataframe,
):

    result = detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


# =========================================================
# INDEX PRESERVATION
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_preserves_custom_index(
    detector,
    kwargs,
    ensemble_dataframe,
):

    result = detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    original_index = set(
        ensemble_dataframe.index
    )

    assert set(
        result.outlier_indices
    ).issubset(
        original_index
    )

    assert set(
        result.inlier_indices
    ).issubset(
        original_index
    )

    assert (
        set(result.outlier_indices)
        |
        set(result.inlier_indices)
        == original_index
    )


# =========================================================
# LABEL CONTRACT
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_labels_match_observation_count(
    detector,
    kwargs,
    ensemble_dataframe,
):

    result = detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    assert (
        len(result.labels)
        == result.total_observations
    )


# =========================================================
# SCORE CONTRACT
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_scores_match_observation_count(
    detector,
    kwargs,
    ensemble_dataframe,
):

    result = detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    assert (
        len(result.scores)
        == result.total_observations
    )

    assert all(
        np.isfinite(score)
        for score in result.scores
    )


# =========================================================
# SCORE ORIENTATION
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_score_is_higher_for_stronger_anomaly(
    detector,
    kwargs,
    ensemble_dataframe,
):
    """
    Contrat EMIDAF :

        score élevé = observation plus atypique.

    Cette convention doit être identique entre
    LOF, Isolation Forest, One-Class SVM,
    Elliptic Envelope et les futurs détecteurs.
    """

    result = detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    score_by_index = dict(
        zip(
            ensemble_dataframe.index,
            result.scores,
        )
    )

    outlier_score = score_by_index[
        "row_OUTLIER"
    ]

    normal_scores = [
        score_by_index[index]
        for index
        in ensemble_dataframe.index
        if index != "row_OUTLIER"
    ]

    assert (
        outlier_score
        >
        np.median(normal_scores)
    )


# =========================================================
# COUNTS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_counts_are_consistent(
    detector,
    kwargs,
    ensemble_dataframe,
):

    result = detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


# =========================================================
# IMMUTABILITY
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_does_not_mutate_input(
    detector,
    kwargs,
    ensemble_dataframe,
):

    before = ensemble_dataframe.copy(
        deep=True
    )

    detector.detect(
        ensemble_dataframe,
        **kwargs,
    )

    pd.testing.assert_frame_equal(
        ensemble_dataframe,
        before,
    )


# =========================================================
# NON-NUMERIC COLUMNS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_ignores_non_numeric_columns(
    detector,
    kwargs,
    ensemble_dataframe,
):

    dataframe = ensemble_dataframe.copy(
        deep=True
    )

    dataframe[
        "category"
    ] = "A"

    result = detector.detect(
        dataframe,
        **kwargs,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


# =========================================================
# MISSING VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_excludes_missing_rows(
    detector,
    kwargs,
    ensemble_dataframe,
):

    dataframe = ensemble_dataframe.copy(
        deep=True
    )

    dataframe.loc[
        "row_0",
        "x1",
    ] = np.nan

    result = detector.detect(
        dataframe,
        **kwargs,
    )

    assert (
        "row_0"
        not in result.outlier_indices
    )

    assert (
        "row_0"
        not in result.inlier_indices
    )

    assert (
        result.total_observations
        == len(dataframe) - 1
    )
