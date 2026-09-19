from __future__ import annotations

import pandas as pd

from emidaf_core.statistics.outliers.base import (
    BaseOutlierDetector,
)


class DummyDetector(BaseOutlierDetector):

    name = "Dummy"

    method_family = "test_family"
    score_type = "test_score"

    score_direction = (
        "higher_is_more_anomalous"
    )

    scaling_sensitive = True

    @classmethod
    def detect(
        cls,
        values,
        **kwargs,
    ):

        series = pd.Series(
            values,
            dtype=float,
        )

        return cls.build_result(
            series,
            indices=[
                series.index[-1]
            ],
            scores=[
                0.1,
                0.2,
                10.0,
            ],
        )


def test_base_detector_propagates_method_family():

    result = DummyDetector.detect(
        [
            1.0,
            2.0,
            100.0,
        ]
    )

    assert (
        result.method_family
        == "test_family"
    )


def test_base_detector_propagates_score_type():

    result = DummyDetector.detect(
        [
            1.0,
            2.0,
            100.0,
        ]
    )

    assert (
        result.score_type
        == "test_score"
    )


def test_base_detector_propagates_score_direction():

    result = DummyDetector.detect(
        [
            1.0,
            2.0,
            100.0,
        ]
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )


def test_base_detector_propagates_scaling_sensitivity():

    result = DummyDetector.detect(
        [
            1.0,
            2.0,
            100.0,
        ]
    )

    assert (
        result.scaling_sensitive
        is True
    )


def test_base_detector_has_safe_metadata_defaults():

    assert BaseOutlierDetector.method_family == ""
    assert BaseOutlierDetector.score_type == ""

    assert (
        BaseOutlierDetector.score_direction
        == "none"
    )

    assert (
        BaseOutlierDetector.scaling_sensitive
        is False
    )
