from __future__ import annotations

import pandas as pd
import pytest

from emidaf_core.common.results import ReportResult
from emidaf_core.statistics.outliers.report import (
    OutlierReport,
)


# ==========================================================
# FIXTURES
# ==========================================================


@pytest.fixture
def univariate_dataframe():

    return pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                3.0,
                4.0,
                100.0,
            ],
            "category": [
                "A",
                "B",
                "C",
                "D",
                "E",
            ],
        }
    )


@pytest.fixture
def multivariate_dataframe():

    return pd.DataFrame(
        {
            "x1": [
                0.0,
                0.1,
                -0.1,
                0.2,
                0.0,
                0.1,
                -0.1,
                0.2,
                5.0,
                5.2,
                5.1,
                5.3,
                10.0,
                10.2,
                10.1,
                10.3,
                0.3,
                -0.3,
                0.4,
                -0.4,
                1.0,
                1.1,
                0.9,
                1.2,
                2.0,
            ],
            "x2": [
                0.0,
                -0.1,
                0.1,
                0.2,
                0.1,
                0.0,
                -0.2,
                0.1,
                5.0,
                5.1,
                5.2,
                5.3,
                10.0,
                10.1,
                10.2,
                10.3,
                0.2,
                -0.2,
                0.3,
                -0.3,
                1.1,
                1.0,
                1.2,
                0.9,
                2.1,
            ],
            "category": [
                "A"
            ] * 25,
        }
    )


# ==========================================================
# REPORT RESULT
# ==========================================================


def test_generate_returns_report_result(
    univariate_dataframe,
):

    report = OutlierReport.generate(
        univariate_dataframe
    )

    assert isinstance(
        report,
        ReportResult,
    )


def test_report_general_metadata(
    univariate_dataframe,
):

    report = OutlierReport.generate(
        univariate_dataframe
    )

    assert (
        report.report_name
        == "Outlier Detection Report"
    )

    assert (
        report.report_type
        == "Outlier Analysis"
    )

    assert (
        report.title
        == "Outlier Analysis Report"
    )


def test_report_contains_six_sections(
    univariate_dataframe,
):

    report = OutlierReport.generate(
        univariate_dataframe
    )

    assert len(
        report.sections
    ) == 6

    assert report.sections == [
        "Statistical Detection",
        "Distance Detection",
        "Density Detection",
        "Clustering Detection",
        "Ensemble Detection",
        "Multivariate Detection",
    ]


# ==========================================================
# STATISTICS STRUCTURE
# ==========================================================


def test_report_contains_all_detection_families(
    univariate_dataframe,
):

    report = OutlierReport.generate(
        univariate_dataframe
    )

    assert set(
        report.statistics
    ) == {
        "statistical",
        "distance",
        "density",
        "clustering",
        "ensemble",
        "multivariate",
    }


def test_report_analyzes_numeric_columns_only(
    univariate_dataframe,
):

    report = OutlierReport.generate(
        univariate_dataframe
    )

    statistical = report.statistics[
        "statistical"
    ]

    assert "value" in statistical
    assert "category" not in statistical


def test_univariate_report_skips_multivariate_families(
    univariate_dataframe,
):

    report = OutlierReport.generate(
        univariate_dataframe
    )

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
# MULTIVARIATE
# ==========================================================


def test_multivariate_report_runs_native_families(
    multivariate_dataframe,
):

    report = OutlierReport.generate(
        multivariate_dataframe
    )

    assert report.statistics[
        "distance"
    ]

    assert report.statistics[
        "density"
    ]

    assert report.statistics[
        "clustering"
    ]

    assert report.statistics[
        "ensemble"
    ]

    assert report.statistics[
        "multivariate"
    ]


def test_multivariate_report_works_without_pyod(
    multivariate_dataframe,
):

    report = OutlierReport.generate(
        multivariate_dataframe
    )

    ensemble = report.statistics[
        "ensemble"
    ]

    multivariate = report.statistics[
        "multivariate"
    ]

    assert "hbos" not in ensemble
    assert "abod" not in ensemble
    assert "ecod" not in ensemble
    assert "copod" not in ensemble

    assert (
        "feature_bagging"
        not in multivariate
    )


# ==========================================================
# IMMUTABILITY
# ==========================================================


def test_generate_does_not_modify_dataframe(
    univariate_dataframe,
):

    original = univariate_dataframe.copy(
        deep=True
    )

    OutlierReport.generate(
        univariate_dataframe
    )

    pd.testing.assert_frame_equal(
        univariate_dataframe,
        original,
    )


# ==========================================================
# PUBLIC HELPERS
# ==========================================================


def test_statistics_helper_returns_statistics(
    univariate_dataframe,
):

    expected = OutlierReport.generate(
        univariate_dataframe
    ).statistics

    actual = OutlierReport.statistics(
        univariate_dataframe
    )

    assert actual.keys() == expected.keys()


def test_export_returns_report_result(
    univariate_dataframe,
):

    report = OutlierReport.export(
        univariate_dataframe
    )

    assert isinstance(
        report,
        ReportResult,
    )


def test_summary_helper_returns_summary_information(
    univariate_dataframe,
):

    summary = OutlierReport.summary(
        univariate_dataframe
    )

    assert isinstance(
        summary,
        dict,
    )

    assert (
        summary["Report"]
        == "Outlier Detection Report"
    )

    assert (
        summary["Type"]
        == "Outlier Analysis"
    )

    assert summary["Sections"] == 6
