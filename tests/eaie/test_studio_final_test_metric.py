from types import SimpleNamespace

from emidaf_studio.pages.eaie.callbacks import (
    _final_test_metric,
)


def _result():

    return SimpleNamespace(
        f1_score=0.74,
        f1_positive=0.65,
        precision_positive=0.72,
        recall_positive=0.60,
        roc_auc=0.83,
        pr_auc=0.78,
        r2=0.41,
        score=0.74,
    )


def test_final_test_metric_uses_positive_f1():

    label, value = _final_test_metric(
        _result(),
        "f1",
    )

    assert label == "F1 classe positive"
    assert value == 0.65


def test_final_test_metric_keeps_weighted_f1():

    label, value = _final_test_metric(
        _result(),
        "f1_weighted",
    )

    assert label == "F1 pondéré"
    assert value == 0.74


def test_final_test_metric_uses_pr_auc():

    label, value = _final_test_metric(
        _result(),
        "average_precision",
    )

    assert label == "PR-AUC"
    assert value == 0.78


def test_final_test_metric_uses_r2():

    label, value = _final_test_metric(
        _result(),
        "r2",
    )

    assert label == "R²"
    assert value == 0.41
