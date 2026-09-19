from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.common.results import ReportResult
from emidaf_core.statistics.outliers.report import (
    OutlierReport,
)


# ==========================================================
# EMPTY DATAFRAME
# ==========================================================


def test_report_handles_empty_dataframe():

    dataframe = pd.DataFrame()

    report = OutlierReport.generate(
        dataframe
    )

    assert isinstance(
        report,
        ReportResult,
    )

    assert report.statistics[
        "statistical"
    ] == {}

    assert report.statistics[
        "distance"
    ] == {}

    assert report.statistics[
        "density"
    ] == {}

    assert report.statistics[
        "clustering"
    ] == {}

    assert report.statistics[
        "ensemble"
    ] == {}

    assert report.statistics[
        "multivariate"
    ] == {}


# ==========================================================
# NO NUMERIC COLUMNS
# ==========================================================


def test_report_handles_no_numeric_columns():

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

    report = OutlierReport.generate(
        dataframe
    )

    assert report.statistics[
        "statistical"
    ] == {}

    assert report.statistics[
        "distance"
    ] == {}

    assert report.statistics[
        "density"
    ] == {}

    assert report.statistics[
        "clustering"
    ] == {}

    assert report.statistics[
        "ensemble"
    ] == {}

    assert report.statistics[
        "multivariate"
    ] == {}


# ==========================================================
# SINGLE NUMERIC COLUMN
# ==========================================================


def test_report_with_single_numeric_column_skips_multivariate():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                3.0,
                100.0,
            ]
        }
    )

    report = OutlierReport.generate(
        dataframe
    )

    assert "value" in report.statistics[
        "statistical"
    ]

    for family in [
        "distance",
        "density",
        "clustering",
        "ensemble",
        "multivariate",
    ]:
        assert (
            report.statistics[family]
            == {}
        )


# ==========================================================
# SMALL MULTIVARIATE SAMPLE
# ==========================================================


def test_report_handles_small_multivariate_sample():

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
            ],
            "x2": [
                1.0,
                2.0,
            ],
            "x3": [
                1.0,
                2.0,
            ],
        }
    )

    report = OutlierReport.generate(
        dataframe
    )

    assert isinstance(
        report,
        ReportResult,
    )

    assert report.statistics[
        "statistical"
    ]


# ==========================================================
# NAN
# ==========================================================


def test_report_handles_nan_values():

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                np.nan,
                3.0,
                4.0,
                5.0,
            ],
            "x2": [
                1.0,
                2.0,
                np.nan,
                4.0,
                5.0,
            ],
        }
    )

    report = OutlierReport.generate(
        dataframe
    )

    assert isinstance(
        report,
        ReportResult,
    )


# ==========================================================
# INFINITE VALUES
# ==========================================================


def test_report_rejects_infinite_values_cleanly():

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
                np.inf,
                4.0,
                5.0,
            ],
            "x2": [
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
        OutlierReport.generate(
            dataframe
        )


# ==========================================================
# INVALID TARGET
# ==========================================================


def test_report_with_unknown_target_is_handled_cleanly():

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                30,
                dtype=float,
            ),
            "x2": np.arange(
                30,
                dtype=float,
            ) + 1.0,
        }
    )

    with pytest.raises(
        (KeyError, ValueError)
    ):
        OutlierReport.generate(
            dataframe,
            target="missing_target",
        )


# ==========================================================
# CONSTANT FEATURES
# ==========================================================


def test_report_handles_constant_numeric_features():

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0
            ] * 30,
            "x2": [
                2.0
            ] * 30,
        }
    )

    report = OutlierReport.generate(
        dataframe
    )

    assert isinstance(
        report,
        ReportResult,
    )


# ==========================================================
# ORIGINAL DATAFRAME
# ==========================================================


def test_report_edge_cases_do_not_modify_original_dataframe():

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
                np.nan,
                4.0,
                5.0,
            ],
            "x2": [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
            ],
        }
    )

    original = dataframe.copy(
        deep=True
    )

    try:
        OutlierReport.generate(
            dataframe
        )
    except Exception:
        pass

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_report_records_unavailable_family_errors():

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
            ],
            "x2": [
                1.0,
                2.0,
            ],
            "x3": [
                1.0,
                2.0,
            ],
        }
    )

    report = OutlierReport.generate(
        dataframe
    )

    errors = report.metadata[
        "errors"
    ]

    assert isinstance(
        errors,
        dict,
    )

    assert errors

    assert "distance" in errors
