"""
=========================================================
EMIDAF Framework
Tests - Density Outliers Edge Cases
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.density import (
    DBSCANOutlier,
    DensityOutlierDetector,
    LOF,
    OPTICSOutlier,
)


# =========================================================
# HELPERS
# =========================================================


def make_small_dataframe() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "x1": [
                0.0,
                0.1,
                -0.1,
                0.2,
                5.0,
            ],
            "x2": [
                0.0,
                -0.1,
                0.1,
                0.2,
                5.0,
            ],
        },
        index=[
            "a",
            "b",
            "c",
            "d",
            "outlier",
        ],
    )


# =========================================================
# INFINITE VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_rejects_infinite_values(
    detector,
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

    with pytest.raises(
        ValueError
    ):
        detector.detect(
            dataframe
        )


# =========================================================
# ALL MISSING
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_rejects_empty_complete_case_dataset(
    detector,
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

    with pytest.raises(
        ValueError
    ):
        detector.detect(
            dataframe
        )


# =========================================================
# NO NUMERIC COLUMNS
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_rejects_dataset_without_numeric_columns(
    detector,
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

    with pytest.raises(
        ValueError
    ):
        detector.detect(
            dataframe
        )


# =========================================================
# LOF SMALL SAMPLE
# =========================================================


def test_lof_handles_neighbors_larger_than_sample():

    dataframe = make_small_dataframe()

    result = LOF.detect(
        dataframe,
        n_neighbors=20,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(dataframe.index)
    )


def test_lof_rejects_invalid_neighbors():

    dataframe = make_small_dataframe()

    with pytest.raises(
        ValueError
    ):
        LOF.detect(
            dataframe,
            n_neighbors=0,
        )


# =========================================================
# LOF CONTAMINATION
# =========================================================


@pytest.mark.parametrize(
    "contamination",
    [
        0.0,
        -0.1,
        0.8,
    ],
)
def test_lof_rejects_invalid_contamination(
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

    with pytest.raises(
        ValueError
    ):
        LOF.detect(
            dataframe,
            contamination=contamination,
        )


# =========================================================
# DBSCAN PARAMETERS
# =========================================================


def test_dbscan_rejects_non_positive_eps():

    dataframe = make_small_dataframe()

    with pytest.raises(
        ValueError
    ):
        DBSCANOutlier.detect(
            dataframe,
            eps=0,
        )


def test_dbscan_rejects_invalid_min_samples():

    dataframe = make_small_dataframe()

    with pytest.raises(
        ValueError
    ):
        DBSCANOutlier.detect(
            dataframe,
            min_samples=0,
        )


# =========================================================
# OPTICS PARAMETERS
# =========================================================


def test_optics_rejects_invalid_min_samples():

    dataframe = make_small_dataframe()

    with pytest.raises(
        ValueError
    ):
        OPTICSOutlier.detect(
            dataframe,
            min_samples=0,
        )


@pytest.mark.parametrize(
    "xi",
    [
        0.0,
        -0.1,
        1.0,
        1.5,
    ],
)
def test_optics_rejects_invalid_xi(
    xi,
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
        }
    )

    with pytest.raises(
        ValueError
    ):
        OPTICSOutlier.detect(
            dataframe,
            xi=xi,
        )


# =========================================================
# LABEL CONTRACT
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_labels_match_observation_count(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.linspace(
                0,
                1,
                30,
            ),
            "x2": np.linspace(
                0,
                1,
                30,
            ),
        }
    )

    result = detector.detect(
        dataframe
    )

    assert (
        len(result.labels)
        == result.total_observations
    )


# =========================================================
# LOF SCORE CONTRACT
# =========================================================


def test_lof_scores_match_observation_count():

    dataframe = pd.DataFrame(
        {
            "x1": np.linspace(
                0,
                1,
                30,
            ),
            "x2": np.linspace(
                0,
                1,
                30,
            ),
        }
    )

    result = LOF.detect(
        dataframe
    )

    assert (
        len(result.scores)
        == result.total_observations
    )

    assert all(
        np.isfinite(
            score
        )
        for score
        in result.scores
    )


# =========================================================
# DBSCAN / OPTICS SCORE CONTRACT
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_cluster_density_detectors_have_no_scores(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.linspace(
                0,
                1,
                30,
            ),
            "x2": np.linspace(
                0,
                1,
                30,
            ),
        }
    )

    result = detector.detect(
        dataframe
    )

    assert result.scores == []


# =========================================================
# SERVICE CONTRACT
# =========================================================


def test_density_service_returns_all_methods():

    dataframe = pd.DataFrame(
        {
            "x1": np.linspace(
                0,
                1,
                30,
            ),
            "x2": np.linspace(
                0,
                1,
                30,
            ),
        }
    )

    result = (
        DensityOutlierDetector.compute(
            dataframe
        )
    )

    assert set(result) == {
        "lof",
        "dbscan",
        "optics",
    }
