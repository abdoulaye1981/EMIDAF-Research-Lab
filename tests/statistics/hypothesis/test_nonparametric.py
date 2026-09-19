import numpy as np
import pytest

from emidaf_core.statistics.hypothesis import (
    MannWhitneyTest,
    WilcoxonTest,
    KruskalWallisTest,
    FriedmanTest,
    SpearmanTest,
    MoodMedianTest,
    SignTest,
    mann_whitney_test,
    wilcoxon_test,
    kruskal_wallis_test,
    friedman_test,
    spearman_test,
    mood_median_test,
    sign_test,
)
from emidaf_core.common.results import HypothesisResult


def test_mann_whitney():

    result = MannWhitneyTest().test(
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Mann-Whitney U"
    assert result.p_value < 0.05
    assert result.reject_null is True


def test_mann_whitney_function():

    result = mann_whitney_test(
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    )

    assert isinstance(result, HypothesisResult)


def test_mann_whitney_missing():

    result = MannWhitneyTest().test(
        [1, 2, np.nan, 4, 5],
        [6, 7, 8, np.nan, 10]
    )

    assert result.extra["n_group1"] == 4
    assert result.extra["n_group2"] == 4


def test_mann_whitney_invalid_size():

    with pytest.raises(ValueError):

        MannWhitneyTest().test(
            [1],
            [2, 3]
        )


def test_wilcoxon():

    result = WilcoxonTest().test(
        [10, 11, 12, 13, 14],
        [11, 12, 13, 14, 15]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Wilcoxon Signed-Rank"
    assert result.p_value == pytest.approx(0.0625)


def test_wilcoxon_function():

    result = wilcoxon_test(
        [10, 11, 12, 13, 14],
        [11, 12, 13, 14, 15]
    )

    assert isinstance(result, HypothesisResult)


def test_wilcoxon_invalid_size():

    with pytest.raises(ValueError):

        WilcoxonTest().test(
            [1, 2, 3],
            [1, 2]
        )


def test_kruskal_wallis():

    result = KruskalWallisTest().test(
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Kruskal-Wallis"
    assert result.p_value < 0.05
    assert result.reject_null is True


def test_kruskal_wallis_function():

    result = kruskal_wallis_test(
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    )

    assert isinstance(result, HypothesisResult)


def test_kruskal_wallis_invalid_groups():

    with pytest.raises(ValueError):

        KruskalWallisTest().test(
            [1, 2, 3]
        )


def test_friedman():

    result = FriedmanTest().test(
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Friedman"
    assert result.p_value < 0.05
    assert result.reject_null is True


def test_friedman_function():

    result = friedman_test(
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5]
    )

    assert isinstance(result, HypothesisResult)


def test_friedman_invalid_groups():

    with pytest.raises(ValueError):

        FriedmanTest().test(
            [1, 2, 3],
            [2, 3, 4]
        )


def test_spearman():

    result = SpearmanTest().test(
        [1, 2, 3, 4, 5],
        [2, 4, 6, 8, 10]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Spearman Rank Correlation"
    assert result.statistic == pytest.approx(1.0)
    assert result.p_value < 0.05
    assert result.reject_null is True


def test_spearman_function():

    result = spearman_test(
        [1, 2, 3, 4, 5],
        [2, 4, 6, 8, 10]
    )

    assert isinstance(result, HypothesisResult)


def test_spearman_missing():

    result = SpearmanTest().test(
        [1, 2, np.nan, 4, 5],
        [2, 4, 6, 8, 10]
    )

    assert result.extra["n"] == 4


def test_spearman_invalid_size():

    with pytest.raises(ValueError):

        SpearmanTest().test(
            [1, 2],
            [2, 4]
        )


def test_mood_median():

    result = MoodMedianTest().test(
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Mood Median Test"
    assert result.p_value < 0.05
    assert result.reject_null is True


def test_mood_median_function():

    result = mood_median_test(
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    )

    assert isinstance(result, HypothesisResult)


def test_sign_test():

    result = SignTest().test(
        [10, 11, 12, 13, 14],
        [11, 12, 13, 14, 15]
    )

    assert isinstance(result, HypothesisResult)
    assert result.test_name == "Sign Test"
    assert result.p_value == pytest.approx(0.0625)


def test_sign_test_function():

    result = sign_test(
        [10, 11, 12, 13, 14],
        [11, 12, 13, 14, 15]
    )

    assert isinstance(result, HypothesisResult)


def test_invalid_alpha():

    with pytest.raises(ValueError):
        MannWhitneyTest(alpha=0)

    with pytest.raises(ValueError):
        MannWhitneyTest(alpha=1)

    with pytest.raises(ValueError):
        MannWhitneyTest(alpha=-0.1)

    with pytest.raises(ValueError):
        MannWhitneyTest(alpha=1.1)


def test_result_summary():

    result = MannWhitneyTest().test(
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    )

    summary = result.summary()

    assert isinstance(summary, dict)
    assert "Test" in summary
    assert "Statistic" in summary
    assert "P-value" in summary
    assert "Alpha" in summary
    assert "Reject H0" in summary
    assert "Decision" in summary
    assert "Interpretation" in summary


def test_result_to_dict():

    result = SpearmanTest().test(
        [1, 2, 3, 4, 5],
        [2, 4, 6, 8, 10]
    )

    data = result.to_dict()

    assert isinstance(data, dict)
    assert data["test_name"] == "Spearman Rank Correlation"
    assert data["p_value"] < 0.05
    assert data["reject_null"] is True


def test_test_object_stores_result():

    test = MannWhitneyTest()

    assert test.result is None

    result = test.test(
        [1, 2, 3],
        [4, 5, 6]
    )

    assert test.result is result
    assert test.p_value == result.p_value
    assert test.statistic == result.statistic
    assert test.significant == result.significant
