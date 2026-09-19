"""
=========================================================
EMIDAF Framework
Tests - Ensemble Outliers Edge Cases
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
# INFINITE VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_rejects_infinite_values(
    detector,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                np.inf,
                3.0,
                4.0,
                5.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


# =========================================================
# ALL MISSING
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_rejects_empty_complete_case_dataset(
    detector,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                np.nan,
                np.nan,
                np.nan,
            ],
            "x2": [
                np.nan,
                np.nan,
                np.nan,
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


# =========================================================
# NO NUMERIC COLUMNS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_detector_rejects_dataset_without_numeric_columns(
    detector,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "category": [
                "A",
                "B",
                "C",
            ],
            "label": [
                "x",
                "y",
                "z",
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


# =========================================================
# ISOLATION FOREST CONTAMINATION
# =========================================================


@pytest.mark.parametrize(
    "contamination",
    [
        0.0,
        -0.1,
        0.8,
    ],
)
def test_isolation_forest_rejects_invalid_contamination(
    contamination,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                30,
                dtype=float,
            ),
            "x2": np.arange(
                30,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        IsolationForestDetector.detect(
            dataframe,
            contamination=contamination,
        )


# =========================================================
# ONE CLASS SVM NU
# =========================================================


@pytest.mark.parametrize(
    "nu",
    [
        0.0,
        -0.1,
        1.5,
    ],
)
def test_one_class_svm_rejects_invalid_nu(
    nu,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                30,
                dtype=float,
            ),
            "x2": np.arange(
                30,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        OneClassSVMDetector.detect(
            dataframe,
            nu=nu,
        )


# =========================================================
# ELLIPTIC ENVELOPE CONTAMINATION
# =========================================================


@pytest.mark.parametrize(
    "contamination",
    [
        0.0,
        -0.1,
        0.8,
    ],
)
def test_elliptic_envelope_rejects_invalid_contamination(
    contamination,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                30,
                dtype=float,
            ),
            "x2": np.arange(
                30,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        EllipticEnvelopeDetector.detect(
            dataframe,
            contamination=contamination,
        )


# =========================================================
# CONSTANT FEATURES
# =========================================================


def test_isolation_forest_handles_constant_features():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0] * 20,
            "x2": [2.0] * 20,
        }
    )

    result = IsolationForestDetector.detect(
        dataframe,
        contamination=0.05,
        random_state=42,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


def test_one_class_svm_handles_constant_features():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0] * 20,
            "x2": [2.0] * 20,
        }
    )

    result = OneClassSVMDetector.detect(
        dataframe,
        nu=0.05,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


# =========================================================
# ELLIPTIC ENVELOPE - COLLINEARITY
# =========================================================


def test_elliptic_envelope_handles_perfect_collinearity():

    x = np.arange(
        30,
        dtype=float,
    )

    dataframe = pd.DataFrame(
        {
            "x1": x,
            "x2": 2 * x,
        }
    )

    result = EllipticEnvelopeDetector.detect(
        dataframe,
        contamination=0.05,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )

    assert (
        len(result.scores)
        == len(dataframe)
    )


# =========================================================
# SMALL DATASET
# =========================================================


def test_isolation_forest_handles_single_observation():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0],
            "x2": [2.0],
        }
    )

    result = IsolationForestDetector.detect(
        dataframe,
        contamination="auto",
        random_state=42,
    )

    assert (
        result.total_observations
        == 1
    )


def test_one_class_svm_handles_single_observation():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0],
            "x2": [2.0],
        }
    )

    result = OneClassSVMDetector.detect(
        dataframe,
        nu=0.05,
    )

    assert (
        result.total_observations
        == 1
    )


# =========================================================
# RANDOM STATE
# =========================================================


def test_isolation_forest_is_reproducible():

    rng = np.random.default_rng(42)

    dataframe = pd.DataFrame(
        rng.normal(
            size=(100, 3)
        ),
        columns=[
            "x1",
            "x2",
            "x3",
        ],
    )

    first = IsolationForestDetector.detect(
        dataframe,
        contamination=0.05,
        random_state=42,
    )

    second = IsolationForestDetector.detect(
        dataframe,
        contamination=0.05,
        random_state=42,
    )

    assert (
        first.outlier_indices
        == second.outlier_indices
    )

    np.testing.assert_allclose(
        first.scores,
        second.scores,
    )


# =========================================================
# SCORE ORIENTATION vs LABELS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_ensemble_outliers_have_higher_median_score_than_inliers(
    detector,
    kwargs,
):

    rng = np.random.default_rng(42)

    normal = rng.normal(
        0.0,
        0.3,
        size=(200, 2),
    )

    dataframe = pd.DataFrame(
        normal,
        columns=[
            "x1",
            "x2",
        ],
    )

    dataframe.loc[
        len(dataframe)
    ] = [
        8.0,
        8.0,
    ]

    result = detector.detect(
        dataframe,
        **kwargs,
    )

    scores = np.asarray(
        result.scores,
        dtype=float,
    )

    labels = np.asarray(
        result.labels,
    )

    outlier_scores = scores[
        labels == -1
    ]

    inlier_scores = scores[
        labels == 1
    ]

    assert (
        len(outlier_scores) > 0
    )

    assert (
        len(inlier_scores) > 0
    )

    assert (
        np.median(outlier_scores)
        >
        np.median(inlier_scores)
    )
