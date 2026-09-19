from __future__ import annotations

import pandas as pd
import pytest

from emidaf_core.preprocessing.pipeline import (
    ConditionalPipeline,
)


class AddConstant:

    def __init__(
        self,
        value
    ):
        self.value = value

    def fit(
        self,
        X,
        y=None
    ):
        return self

    def transform(
        self,
        X
    ):
        result = X.copy()

        result["x"] = (
            result["x"]
            + self.value
        )

        return result


def test_conditional_step_runs():

    dataframe = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0]
        }
    )

    pipeline = ConditionalPipeline(
        verbose=False
    )

    pipeline.add_conditional_step(
        "add",
        AddConstant(10),
        lambda X, y: True,
    )

    result = pipeline.fit_transform(
        dataframe
    )

    assert result["x"].tolist() == [
        11.0,
        12.0,
        13.0,
    ]

    assert pipeline.skipped_steps_ == []


def test_conditional_step_is_skipped():

    dataframe = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0]
        }
    )

    pipeline = ConditionalPipeline(
        verbose=False
    )

    pipeline.add_conditional_step(
        "skip",
        AddConstant(10),
        lambda X, y: False,
    )

    result = pipeline.fit_transform(
        dataframe
    )

    pd.testing.assert_frame_equal(
        result,
        dataframe,
    )

    assert pipeline.skipped_steps_ == [
        "skip"
    ]

    assert pipeline.fitted_steps == []


def test_condition_receives_current_data():

    dataframe = pd.DataFrame(
        {
            "x": [1.0, 1.0]
        }
    )

    pipeline = ConditionalPipeline(
        verbose=False
    )

    pipeline.add_step(
        "first",
        AddConstant(1),
    )

    pipeline.add_conditional_step(
        "second",
        AddConstant(10),
        lambda X, y: (
            X["x"].mean() >= 2
        ),
    )

    result = pipeline.fit_transform(
        dataframe
    )

    # La condition de "second" doit voir
    # les données APRES l'étape "first".
    assert result["x"].tolist() == [
        12.0,
        12.0,
    ]


def test_non_boolean_condition_is_rejected():

    dataframe = pd.DataFrame(
        {
            "x": [1.0, 2.0]
        }
    )

    pipeline = ConditionalPipeline(
        verbose=False
    )

    pipeline.add_conditional_step(
        "bad",
        AddConstant(1),
        lambda X, y: "yes",
    )

    with pytest.raises(
        TypeError,
        match="boolean",
    ):
        pipeline.fit(
            dataframe
        )


def test_condition_must_be_callable():

    pipeline = ConditionalPipeline(
        verbose=False
    )

    with pytest.raises(
        TypeError,
        match="callable",
    ):
        pipeline.add_conditional_step(
            "bad",
            AddConstant(1),
            True,
        )


def test_remove_step_removes_condition():

    pipeline = ConditionalPipeline(
        verbose=False
    )

    pipeline.add_conditional_step(
        "temporary",
        AddConstant(1),
        lambda X, y: True,
    )

    pipeline.remove_step(
        "temporary"
    )

    assert "temporary" not in (
        pipeline.conditions
    )

    assert "temporary" not in (
        pipeline.step_names()
    )


def test_reset_clears_skipped_steps():

    dataframe = pd.DataFrame(
        {
            "x": [1.0]
        }
    )

    pipeline = ConditionalPipeline(
        verbose=False
    )

    pipeline.add_conditional_step(
        "skip",
        AddConstant(1),
        lambda X, y: False,
    )

    pipeline.fit(
        dataframe
    )

    assert pipeline.skipped_steps_ == [
        "skip"
    ]

    pipeline.reset()

    assert pipeline.skipped_steps_ == []
