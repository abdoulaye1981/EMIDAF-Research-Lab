"""
=========================================================
EMIDAF Framework
Tests - Multivariate Outliers Edge Cases
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.multivariate import (
    AutoEncoderOutlier,
    MinimumCovarianceDeterminant,
    PCAOutlier,
    RobustPCAOutlier,
)


# =========================================================
# INFINITE VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    [
        (
            PCAOutlier,
            {
                "n_components": 2,
                "percentile": 95,
            },
        ),
        (
            RobustPCAOutlier,
            {
                "percentile": 97.5,
            },
        ),
        (
            MinimumCovarianceDeterminant,
            {
                "percentile": 97.5,
            },
        ),
    ],
)
def test_multivariate_detector_rejects_infinite_values(
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
            "x3": [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


# =========================================================
# EMPTY COMPLETE DATASET
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    [
        (
            PCAOutlier,
            {
                "n_components": 1,
            },
        ),
        (
            RobustPCAOutlier,
            {},
        ),
        (
            MinimumCovarianceDeterminant,
            {},
        ),
    ],
)
def test_multivariate_detector_rejects_empty_complete_dataset(
    detector,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                np.nan,
                np.nan,
            ],
            "x2": [
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
    [
        (
            PCAOutlier,
            {
                "n_components": 1,
            },
        ),
        (
            RobustPCAOutlier,
            {},
        ),
        (
            MinimumCovarianceDeterminant,
            {},
        ),
    ],
)
def test_multivariate_detector_rejects_no_numeric_columns(
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
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


# =========================================================
# PCA COMPONENTS
# =========================================================


def test_pca_rejects_more_components_than_features():

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                10,
                dtype=float,
            ),
            "x2": np.arange(
                10,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        PCAOutlier.detect(
            dataframe,
            n_components=3,
        )


def test_pca_rejects_more_components_than_samples():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
            ],
            "x2": [
                0.0,
                1.0,
            ],
            "x3": [
                0.0,
                1.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        PCAOutlier.detect(
            dataframe,
            n_components=3,
        )


def test_pca_rejects_zero_components():

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                10,
                dtype=float,
            ),
            "x2": np.arange(
                10,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        PCAOutlier.detect(
            dataframe,
            n_components=0,
        )


# =========================================================
# INVALID PERCENTILES
# =========================================================


@pytest.mark.parametrize(
    "percentile",
    [
        -1,
        101,
    ],
)
@pytest.mark.parametrize(
    "detector, kwargs",
    [
        (
            PCAOutlier,
            {
                "n_components": 1,
            },
        ),
        (
            RobustPCAOutlier,
            {},
        ),
        (
            MinimumCovarianceDeterminant,
            {},
        ),
    ],
)
def test_multivariate_detector_rejects_invalid_percentile(
    detector,
    kwargs,
    percentile,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                20,
                dtype=float,
            ),
            "x2": np.arange(
                20,
                dtype=float,
            ),
            "x3": np.arange(
                20,
                dtype=float,
            ),
        }
    )

    kwargs = {
        **kwargs,
        "percentile": percentile,
    }

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


# =========================================================
# CONSTANT FEATURES
# =========================================================


def test_pca_handles_constant_features():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0] * 20,
            "x2": [2.0] * 20,
            "x3": [3.0] * 20,
        }
    )

    result = PCAOutlier.detect(
        dataframe,
        n_components=2,
        percentile=95,
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
# PERFECT COLLINEARITY
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        RobustPCAOutlier,
        MinimumCovarianceDeterminant,
    ],
)
def test_mcd_based_detector_handles_perfect_collinearity(
    detector,
):

    x = np.arange(
        30,
        dtype=float,
    )

    dataframe = pd.DataFrame(
        {
            "x1": x,
            "x2": 2 * x,
            "x3": 3 * x,
        }
    )

    result = detector.detect(
        dataframe,
        percentile=97.5,
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
# SMALL SAMPLE
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        RobustPCAOutlier,
        MinimumCovarianceDeterminant,
    ],
)
def test_mcd_based_detector_rejects_too_small_sample(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
            ],
            "x2": [
                0.0,
                1.0,
            ],
            "x3": [
                0.0,
                1.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe
        )


# =========================================================
# PCA SCORE CONTRACT
# =========================================================


def test_pca_scores_are_non_negative():

    rng = np.random.default_rng(42)

    dataframe = pd.DataFrame(
        rng.normal(
            size=(100, 4)
        ),
        columns=[
            "x1",
            "x2",
            "x3",
            "x4",
        ],
    )

    result = PCAOutlier.detect(
        dataframe,
        n_components=2,
        percentile=95,
    )

    assert all(
        score >= 0
        for score in result.scores
    )


# =========================================================
# AUTOENCODER PLACEHOLDER
# =========================================================


def test_autoencoder_is_explicitly_not_implemented():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                2.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
            ],
        }
    )

    with pytest.raises(
        NotImplementedError
    ):
        AutoEncoderOutlier.detect(
            dataframe
        )
