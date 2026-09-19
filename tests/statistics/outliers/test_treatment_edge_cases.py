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
    QuantileCapping,
    RemoveOutliers,
    Winsorization,
)


def make_dataframe():

    return pd.DataFrame(
        {
            "value": [
                1.0,
                2.0,
                3.0,
                100.0,
            ],
            "other": [
                10,
                20,
                30,
                40,
            ],
        },
        index=[
            10,
            20,
            30,
            40,
        ],
    )


# ==========================================================
# INVALID COLUMN
# ==========================================================


@pytest.mark.parametrize(
    "treatment, kwargs",
    [
        (
            RemoveOutliers,
            {
                "lower": 0.0,
                "upper": 10.0,
            },
        ),
        (
            Winsorization,
            {
                "lower": 0.0,
                "upper": 10.0,
            },
        ),
        (
            Capping,
            {
                "lower": 0.0,
                "upper": 10.0,
            },
        ),
        (
            Flooring,
            {
                "lower": 0.0,
            },
        ),
        (
            QuantileCapping,
            {},
        ),
    ],
)
def test_treatment_rejects_unknown_column(
    treatment,
    kwargs,
):

    dataframe = make_dataframe()

    with pytest.raises(
        KeyError
    ):
        treatment.apply(
            dataframe,
            "missing_column",
            **kwargs,
        )


# ==========================================================
# INVALID BOUNDS
# ==========================================================


@pytest.mark.parametrize(
    "treatment",
    [
        RemoveOutliers,
        Winsorization,
        Capping,
    ],
)
def test_treatment_rejects_reversed_bounds(
    treatment,
):

    dataframe = make_dataframe()

    with pytest.raises(
        ValueError
    ):
        treatment.apply(
            dataframe,
            "value",
            lower=10.0,
            upper=0.0,
        )


# ==========================================================
# QUANTILES
# ==========================================================


@pytest.mark.parametrize(
    "q_low, q_high",
    [
        (-0.1, 0.9),
        (0.1, 1.1),
        (0.9, 0.1),
        (0.5, 0.5),
    ],
)
def test_quantile_capping_rejects_invalid_quantiles(
    q_low,
    q_high,
):

    dataframe = make_dataframe()

    with pytest.raises(
        ValueError
    ):
        QuantileCapping.apply(
            dataframe,
            "value",
            q_low=q_low,
            q_high=q_high,
        )


# ==========================================================
# MASK VALIDATION
# ==========================================================


@pytest.mark.parametrize(
    "treatment",
    [
        MeanReplacement,
        MedianReplacement,
        AdaptiveTreatment,
    ],
)
def test_mask_based_treatment_rejects_wrong_length(
    treatment,
):

    dataframe = make_dataframe()

    mask = pd.Series(
        [
            False,
            True,
        ]
    )

    with pytest.raises(
        ValueError
    ):
        treatment.apply(
            dataframe,
            "value",
            mask,
        )


@pytest.mark.parametrize(
    "treatment",
    [
        MeanReplacement,
        MedianReplacement,
        AdaptiveTreatment,
    ],
)
def test_mask_based_treatment_rejects_misaligned_index(
    treatment,
):

    dataframe = make_dataframe()

    mask = pd.Series(
        [
            False,
            False,
            False,
            True,
        ],
        index=[
            100,
            200,
            300,
            400,
        ],
    )

    with pytest.raises(
        ValueError
    ):
        treatment.apply(
            dataframe,
            "value",
            mask,
        )


@pytest.mark.parametrize(
    "treatment",
    [
        MeanReplacement,
        MedianReplacement,
    ],
)
def test_replacement_rejects_all_rows_marked_as_outliers(
    treatment,
):

    dataframe = make_dataframe()

    mask = pd.Series(
        True,
        index=dataframe.index,
    )

    with pytest.raises(
        ValueError
    ):
        treatment.apply(
            dataframe,
            "value",
            mask,
        )


# ==========================================================
# NON NUMERIC COLUMN
# ==========================================================


@pytest.mark.parametrize(
    "treatment, kwargs",
    [
        (
            Winsorization,
            {
                "lower": 0.0,
                "upper": 10.0,
            },
        ),
        (
            Flooring,
            {
                "lower": 0.0,
            },
        ),
        (
            QuantileCapping,
            {},
        ),
    ],
)
def test_numeric_treatment_rejects_non_numeric_column(
    treatment,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "category": [
                "A",
                "B",
                "C",
            ]
        }
    )

    with pytest.raises(
        (TypeError, ValueError)
    ):
        treatment.apply(
            dataframe,
            "category",
            **kwargs,
        )


# ==========================================================
# NAN
# ==========================================================


def test_winsorization_preserves_nan():

    dataframe = pd.DataFrame(
        {
            "value": [
                1.0,
                np.nan,
                100.0,
            ]
        }
    )

    after, _ = Winsorization.apply(
        dataframe,
        "value",
        0.0,
        10.0,
    )

    assert np.isnan(
        after.loc[
            1,
            "value",
        ]
    )


def test_flooring_preserves_nan():

    dataframe = pd.DataFrame(
        {
            "value": [
                -10.0,
                np.nan,
                5.0,
            ]
        }
    )

    after, _ = Flooring.apply(
        dataframe,
        "value",
        0.0,
    )

    assert np.isnan(
        after.loc[
            1,
            "value",
        ]
    )


# ==========================================================
# CAPPING METADATA
# ==========================================================


def test_capping_reports_capping_strategy():

    dataframe = make_dataframe()

    _, result = Capping.apply(
        dataframe,
        "value",
        0.0,
        10.0,
    )

    assert result.strategy == "Capping"


# ==========================================================
# ADAPTIVE ZERO OUTLIERS
# ==========================================================


def test_adaptive_with_no_outliers_returns_unchanged_dataframe():

    dataframe = make_dataframe()

    mask = pd.Series(
        False,
        index=dataframe.index,
    )

    after, _ = AdaptiveTreatment.apply(
        dataframe,
        "value",
        mask,
    )

    pd.testing.assert_frame_equal(
        after,
        dataframe,
    )
