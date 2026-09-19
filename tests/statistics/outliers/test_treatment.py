from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.treatment import (
    AdaptiveTreatment,
    Capping,
    Flooring,
    MeanReplacement,
    MedianReplacement,
    OutlierTreatment,
    QuantileCapping,
    RemoveOutliers,
    Winsorization,
)


# ==========================================================
# FIXTURES
# ==========================================================


@pytest.fixture
def simple_dataframe():

    return pd.DataFrame(
        {
            "value": [
                -100.0,
                1.0,
                2.0,
                3.0,
                4.0,
                100.0,
            ],
            "other": [
                10,
                20,
                30,
                40,
                50,
                60,
            ],
        },
        index=[
            101,
            205,
            309,
            412,
            587,
            999,
        ],
    )


# ==========================================================
# REMOVE OUTLIERS
# ==========================================================


def test_remove_outliers_removes_values_outside_bounds(
    simple_dataframe,
):

    original = simple_dataframe.copy(
        deep=True
    )

    after, result = RemoveOutliers.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    assert list(after.index) == [
        205,
        309,
        412,
        587,
    ]

    assert after["value"].tolist() == [
        1.0,
        2.0,
        3.0,
        4.0,
    ]

    pd.testing.assert_frame_equal(
        simple_dataframe,
        original,
    )

    assert result is not None


def test_remove_outliers_keeps_boundary_values():

    dataframe = pd.DataFrame(
        {
            "value": [
                0.0,
                5.0,
                10.0,
            ]
        }
    )

    after, _ = RemoveOutliers.apply(
        dataframe,
        "value",
        0.0,
        10.0,
    )

    assert after["value"].tolist() == [
        0.0,
        5.0,
        10.0,
    ]


# ==========================================================
# WINSORIZATION
# ==========================================================


def test_winsorization_clips_both_tails(
    simple_dataframe,
):

    original = simple_dataframe.copy(
        deep=True
    )

    after, result = Winsorization.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    assert after.loc[101, "value"] == 0.0
    assert after.loc[999, "value"] == 10.0

    assert after.loc[205, "value"] == 1.0
    assert after.loc[587, "value"] == 4.0

    pd.testing.assert_frame_equal(
        simple_dataframe,
        original,
    )

    assert result is not None


def test_winsorization_preserves_other_columns(
    simple_dataframe,
):

    after, _ = Winsorization.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    pd.testing.assert_series_equal(
        after["other"],
        simple_dataframe["other"],
    )


# ==========================================================
# CAPPING
# ==========================================================


def test_capping_has_same_numeric_effect_as_winsorization(
    simple_dataframe,
):

    capped, _ = Capping.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    winsorized, _ = Winsorization.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    pd.testing.assert_frame_equal(
        capped,
        winsorized,
    )


# ==========================================================
# FLOORING
# ==========================================================


def test_flooring_replaces_only_values_below_lower_bound(
    simple_dataframe,
):

    original = simple_dataframe.copy(
        deep=True
    )

    after, result = Flooring.apply(
        simple_dataframe,
        "value",
        0.0,
    )

    assert after.loc[101, "value"] == 0.0

    assert after.loc[205, "value"] == 1.0
    assert after.loc[999, "value"] == 100.0

    pd.testing.assert_frame_equal(
        simple_dataframe,
        original,
    )

    assert result is not None


# ==========================================================
# MEAN REPLACEMENT
# ==========================================================


def test_mean_replacement_uses_non_outlier_observations():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                3.0,
                100.0,
            ]
        },
        index=[
            10,
            20,
            30,
            40,
        ],
    )

    mask = pd.Series(
        [
            False,
            False,
            False,
            True,
        ],
        index=dataframe.index,
    )

    after, result = MeanReplacement.apply(
        dataframe,
        "value",
        mask,
    )

    assert after.loc[40, "value"] == pytest.approx(
        2.0
    )

    assert result is not None


def test_mean_replacement_does_not_modify_original():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                100.0,
            ]
        }
    )

    original = dataframe.copy(
        deep=True
    )

    mask = pd.Series(
        [
            False,
            False,
            True,
        ],
        index=dataframe.index,
    )

    MeanReplacement.apply(
        dataframe,
        "value",
        mask,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


# ==========================================================
# MEDIAN REPLACEMENT
# ==========================================================


def test_median_replacement_uses_non_outlier_observations():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                3.0,
                4.0,
                100.0,
            ]
        }
    )

    mask = pd.Series(
        [
            False,
            False,
            False,
            False,
            True,
        ],
        index=dataframe.index,
    )

    after, result = MedianReplacement.apply(
        dataframe,
        "value",
        mask,
    )

    assert after.loc[4, "value"] == pytest.approx(
        2.5
    )

    assert result is not None


# ==========================================================
# QUANTILE CAPPING
# ==========================================================


def test_quantile_capping_uses_requested_quantiles():

    dataframe = pd.DataFrame(
        {
            "value": np.arange(
                101,
                dtype=float,
            )
        }
    )

    expected_lower = dataframe[
        "value"
    ].quantile(
        0.10
    )

    expected_upper = dataframe[
        "value"
    ].quantile(
        0.90
    )

    after, result = QuantileCapping.apply(
        dataframe,
        "value",
        q_low=0.10,
        q_high=0.90,
    )

    assert after["value"].min() == pytest.approx(
        expected_lower
    )

    assert after["value"].max() == pytest.approx(
        expected_upper
    )

    assert result is not None


# ==========================================================
# ADAPTIVE TREATMENT
# ==========================================================


def test_adaptive_treatment_below_one_percent_removes_outlier():

    values = np.arange(
        200,
        dtype=float,
    )

    dataframe = pd.DataFrame(
        {
            "value": values
        }
    )

    mask = pd.Series(
        False,
        index=dataframe.index,
    )

    mask.iloc[-1] = True

    after, _ = AdaptiveTreatment.apply(
        dataframe,
        "value",
        mask,
    )

    assert len(after) == 199

    assert 199 not in after.index


def test_adaptive_treatment_between_one_and_five_percent_winsorizes():

    dataframe = pd.DataFrame(
        {
            "value": np.concatenate(
                [
                    np.arange(
                        98,
                        dtype=float,
                    ),
                    [
                        1000.0,
                        2000.0,
                    ],
                ]
            )
        }
    )

    mask = pd.Series(
        False,
        index=dataframe.index,
    )

    mask.iloc[-2:] = True

    after, _ = AdaptiveTreatment.apply(
        dataframe,
        "value",
        mask,
    )

    assert len(after) == len(dataframe)

    assert (
        after["value"].max()
        <
        dataframe["value"].max()
    )


def test_adaptive_treatment_above_five_percent_uses_median():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                100.0,
                200.0,
                300.0,
                400.0,
                500.0,
            ]
        }
    )

    mask = pd.Series(
        [
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
        ],
        index=dataframe.index,
    )

    after, _ = AdaptiveTreatment.apply(
        dataframe,
        "value",
        mask,
    )

    expected_median = 3.0

    assert (
        after.loc[
            mask,
            "value",
        ]
        == expected_median
    ).all()


# ==========================================================
# PUBLIC SERVICE
# ==========================================================


def test_outlier_treatment_remove_delegates_correctly(
    simple_dataframe,
):

    direct, _ = RemoveOutliers.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    service, _ = OutlierTreatment.remove(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    pd.testing.assert_frame_equal(
        service,
        direct,
    )


def test_outlier_treatment_winsorize_delegates_correctly(
    simple_dataframe,
):

    direct, _ = Winsorization.apply(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    service, _ = OutlierTreatment.winsorize(
        simple_dataframe,
        "value",
        0.0,
        10.0,
    )

    pd.testing.assert_frame_equal(
        service,
        direct,
    )


def test_outlier_treatment_median_delegates_correctly():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                100.0,
            ]
        }
    )

    mask = pd.Series(
        [
            False,
            False,
            True,
        ],
        index=dataframe.index,
    )

    direct, _ = MedianReplacement.apply(
        dataframe,
        "value",
        mask,
    )

    service, _ = OutlierTreatment.median(
        dataframe,
        "value",
        mask,
    )

    pd.testing.assert_frame_equal(
        service,
        direct,
    )
