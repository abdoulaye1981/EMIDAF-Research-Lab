import pandas as pd

from sklearn.linear_model import LogisticRegression

from emidaf_studio.pages.exaie.callbacks import (
    _classification_decision,
)


def test_classification_decision_types():

    assert _classification_decision(
        1, 1, 1
    ) == "tp"

    assert _classification_decision(
        1, 0, 1
    ) == "fn"

    assert _classification_decision(
        0, 1, 1
    ) == "fp"

    assert _classification_decision(
        0, 0, 1
    ) == "tn"


def test_decision_respects_positive_label():

    assert _classification_decision(
        0, 0, 0
    ) == "tp"

    assert _classification_decision(
        0, 1, 0
    ) == "fn"

    assert _classification_decision(
        1, 0, 0
    ) == "fp"

    assert _classification_decision(
        1, 1, 0
    ) == "tn"


def test_positive_probability_respects_class_label():

    X = pd.DataFrame(
        {
            "x": [
                -3, -2, -1,
                1, 2, 3,
            ]
        }
    )

    y = pd.Series(
        [0, 0, 0, 1, 1, 1]
    )

    model = LogisticRegression(
        random_state=42
    )

    model.fit(X, y)

    probabilities = model.predict_proba(
        X.iloc[[0]]
    )

    classes = list(
        model.classes_
    )

    positive_index = classes.index(1)

    probability_positive = float(
        probabilities[
            0,
            positive_index
        ]
    )

    assert (
        0.0
        <= probability_positive
        <= 1.0
    )
