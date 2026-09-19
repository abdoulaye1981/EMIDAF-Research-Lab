from __future__ import annotations

import pandas as pd

from emidaf_core.preprocessing.base import (
    PreprocessingResult,
)

from emidaf_core.preprocessing.outliers import (
    OutlierDetection,
    Outliers,
)


def test_outlier_inspect_returns_result():

    dataframe = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                3.0,
                100.0,
            ]
        }
    )

    result = OutlierDetection.inspect(
        dataframe,
        method="iqr",
    )

    assert isinstance(
        result,
        PreprocessingResult,
    )

    assert result.step == (
        "Outlier Detection"
    )

    assert result.input_shape == (
        4,
        1,
    )

    assert result.output_shape == (
        4,
        1,
    )

    assert result.variables == [
        "x"
    ]

    assert result.statistics[
        "method"
    ] == "iqr"


def test_outliers_service_exposes_inspect():

    assert callable(
        Outliers.inspect
    )

    dataframe = pd.DataFrame(
        {
            "x": [
                1.0,
                2.0,
                100.0,
            ]
        }
    )

    result = Outliers.inspect(
        dataframe,
        method="iqr",
    )

    assert isinstance(
        result,
        PreprocessingResult,
    )
