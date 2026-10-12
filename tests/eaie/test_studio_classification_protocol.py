from emidaf_studio.pages.eaie.callbacks import (
    _classification_protocol,
)


def test_difficulte_maths_uses_positive_class_f1():

    protocol = _classification_protocol(
        "difficulte_maths"
    )

    assert protocol == {
        "selection_metric": "f1",
        "positive_label": 1,
    }


def test_regression_target_keeps_generic_protocol():

    protocol = _classification_protocol(
        "note_maths"
    )

    assert protocol == {
        "selection_metric": None,
        "positive_label": 1,
    }


def test_unknown_target_keeps_generic_protocol():

    protocol = _classification_protocol(
        "target"
    )

    assert protocol == {
        "selection_metric": None,
        "positive_label": 1,
    }
