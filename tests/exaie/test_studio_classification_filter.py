import numpy as np
import pandas as pd

from emidaf_studio.pages.exaie import callbacks


class FakeEstimator:

    def __init__(self, predictions):
        self._predictions = np.asarray(
            predictions
        )

    def predict(self, X):
        return self._predictions[
            :len(X)
        ]


def _context():

    # réel :
    # 1 1 0 0 1 0 1 0
    #
    # prédit :
    # 1 0 1 0 1 0 0 1
    #
    # VP = 2
    # FN = 2
    # FP = 2
    # VN = 2

    X_test = pd.DataFrame(
        {
            "x": range(8),
        }
    )

    y_test = pd.Series(
        [1, 1, 0, 0, 1, 0, 1, 0]
    )

    estimator = FakeEstimator(
        [1, 0, 1, 0, 1, 0, 0, 1]
    )

    return {
        "task": "classification",
        "X_test": X_test,
        "y_test": y_test,
        "estimator": estimator,
        "positive_label": 1,
    }


def test_filter_all_observations(
    monkeypatch,
):

    monkeypatch.setattr(
        callbacks,
        "get_eaie_run",
        lambda project_id, dataset_id: (
            _context()
        ),
    )

    options, value = (
        callbacks.filter_local_observations(
            "all",
            8,
            10,
        )
    )

    assert len(options) == 8
    assert value == 0


def test_filter_true_positives(
    monkeypatch,
):

    monkeypatch.setattr(
        callbacks,
        "get_eaie_run",
        lambda project_id, dataset_id: (
            _context()
        ),
    )

    options, value = (
        callbacks.filter_local_observations(
            "tp",
            8,
            10,
        )
    )

    assert [
        option["value"]
        for option in options
    ] == [0, 4]

    assert value == 0

    assert all(
        "— VP " in option["label"]
        for option in options
    )


def test_filter_false_negatives(
    monkeypatch,
):

    monkeypatch.setattr(
        callbacks,
        "get_eaie_run",
        lambda project_id, dataset_id: (
            _context()
        ),
    )

    options, value = (
        callbacks.filter_local_observations(
            "fn",
            8,
            10,
        )
    )

    assert [
        option["value"]
        for option in options
    ] == [1, 6]

    assert value == 1

    assert all(
        "réel=1" in option["label"]
        and "prédit=0" in option["label"]
        for option in options
    )


def test_filter_false_positives(
    monkeypatch,
):

    monkeypatch.setattr(
        callbacks,
        "get_eaie_run",
        lambda project_id, dataset_id: (
            _context()
        ),
    )

    options, value = (
        callbacks.filter_local_observations(
            "fp",
            8,
            10,
        )
    )

    assert [
        option["value"]
        for option in options
    ] == [2, 7]

    assert value == 2


def test_filter_true_negatives(
    monkeypatch,
):

    monkeypatch.setattr(
        callbacks,
        "get_eaie_run",
        lambda project_id, dataset_id: (
            _context()
        ),
    )

    options, value = (
        callbacks.filter_local_observations(
            "tn",
            8,
            10,
        )
    )

    assert [
        option["value"]
        for option in options
    ] == [3, 5]

    assert value == 3


def test_regression_keeps_all_rows(
    monkeypatch,
):

    context = _context()
    context["task"] = "regression"

    monkeypatch.setattr(
        callbacks,
        "get_eaie_run",
        lambda project_id, dataset_id: (
            context
        ),
    )

    options, value = (
        callbacks.filter_local_observations(
            "fn",
            8,
            10,
        )
    )

    assert len(options) == 8
    assert value == 0
