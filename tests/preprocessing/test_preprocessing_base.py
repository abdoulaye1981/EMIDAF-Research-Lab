from __future__ import annotations

import pandas as pd
import pytest

from emidaf_core.preprocessing.base import (
    BasePreprocessing,
    BasePreprocessor,
    PreprocessingResult,
)


class DummyPreprocessor(
    BasePreprocessing
):

    def fit(
        self,
        X,
        y=None
    ):
        self.fitted = True
        return self

    def transform(
        self,
        X
    ):
        return X.copy()


def test_legacy_base_inherits_modern_base():

    assert issubclass(
        BasePreprocessing,
        BasePreprocessor,
    )


def test_preprocessing_result_contract():

    result = PreprocessingResult(
        step="Scaling",
        input_shape=(10, 3),
        output_shape=(10, 3),
        variables=["a", "b", "c"],
    )

    assert result.step == "Scaling"
    assert result.input_shape == (10, 3)
    assert result.output_shape == (10, 3)

    assert result.variables == [
        "a",
        "b",
        "c",
    ]

    assert result.statistics == {}
    assert result.metadata == {}


def test_preprocessing_result_statistics_are_mutable():

    result = PreprocessingResult(
        step="Test",
    )

    result.statistics["rows"] = 10

    assert result.statistics == {
        "rows": 10
    }


def test_preprocessing_result_instances_do_not_share_state():

    first = PreprocessingResult()
    second = PreprocessingResult()

    first.statistics["x"] = 1
    first.variables.append("a")

    assert second.statistics == {}
    assert second.variables == []


def test_preprocessing_result_to_dict():

    result = PreprocessingResult(
        step="Encoding",
        input_shape=(5, 2),
        output_shape=(5, 4),
        variables=["a", "b", "c", "d"],
    )

    payload = result.to_dict()

    assert payload["step"] == "Encoding"
    assert payload["input_shape"] == (5, 2)
    assert payload["output_shape"] == (5, 4)

    assert payload["variables"] == [
        "a",
        "b",
        "c",
        "d",
    ]


def test_base_preprocessing_fit_transform():

    dataframe = pd.DataFrame(
        {
            "x": [1, 2, 3]
        }
    )

    processor = DummyPreprocessor()

    result = processor.fit_transform(
        dataframe
    )

    pd.testing.assert_frame_equal(
        result,
        dataframe,
    )

    assert processor.fitted is True


def test_validate_dataframe():

    processor = DummyPreprocessor()

    dataframe = pd.DataFrame(
        {
            "x": [1]
        }
    )

    assert (
        processor._validate_dataframe(
            dataframe
        )
        is dataframe
    )

    with pytest.raises(
        TypeError,
        match="pandas DataFrame",
    ):
        processor._validate_dataframe(
            [1, 2, 3]
        )


def test_copy_dataframe_is_defensive():

    processor = DummyPreprocessor()

    dataframe = pd.DataFrame(
        {
            "x": [1, 2]
        }
    )

    copied = processor._copy_dataframe(
        dataframe
    )

    assert copied is not dataframe

    pd.testing.assert_frame_equal(
        copied,
        dataframe,
    )
