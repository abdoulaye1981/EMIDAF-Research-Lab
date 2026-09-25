import numpy as np
import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.association import (
    TopicTargetAnalyzer,
)


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "stress examen peur anxiété",
                "stress contrôle peur examen",
                "professeur motivant aide disponible",
                "enseignant motivant explication aide",
                "classe chargée effectif élevé",
                "classe surchargée difficile suivre",
            ],
            "note_maths": [
                7.0,
                8.0,
                15.0,
                14.0,
                9.0,
                10.0,
            ],
        },
        index=[
            10,
            20,
            30,
            40,
            50,
            60,
        ],
    )


def test_topic_target_basic(dataframe):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    assert result.n_documents == 6
    assert result.n_topics == 3
    assert len(result.groups) > 0


def test_topic_target_counts_sum(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    total = sum(
        group.n
        for group in result.groups
    )

    assert total == result.n_documents


def test_topic_target_statistics(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    for group in result.groups:
        assert group.minimum <= group.mean
        assert group.mean <= group.maximum


def test_missing_target_values_excluded():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "stress examen peur",
                "professeur motivant aide",
                "classe chargée difficile",
                "stress contrôle anxiété",
            ],
            "note_maths": [
                8.0,
                None,
                10.0,
                7.0,
            ],
        }
    )

    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=2,
        )
    )

    assert result.n_documents == 3


def test_non_numeric_target_rejected(
    dataframe,
):
    dataframe["niveau"] = [
        "3e",
        "3e",
        "2nde",
        "2nde",
        "1ere",
        "1ere",
    ]

    with pytest.raises(
        TypeError,
        match="doit être numérique",
    ):
        TopicTargetAnalyzer().analyze(
            dataframe,
            "review_text",
            "niveau",
            n_topics=3,
        )


def test_unknown_target_rejected(
    dataframe,
):
    with pytest.raises(
        ValueError,
        match="Variable cible introuvable",
    ):
        TopicTargetAnalyzer().analyze(
            dataframe,
            "review_text",
            "unknown",
            n_topics=3,
        )


def test_engine_exposes_topic_target(
    dataframe,
):
    result = (
        ETAEEngine()
        .analyze_topic_target(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    assert (
        result.target_column
        == "note_maths"
    )


def test_topic_target_inference_available(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    assert result.inference is not None
    assert (
        result.inference.anova.test
        == "ANOVA"
    )
    assert (
        result.inference.kruskal.test
        == "Kruskal-Wallis"
    )
    assert (
        result.inference.levene.test
        == "Levene"
    )


def test_topic_target_alpha(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
            alpha=0.01,
        )
    )

    assert result.inference is not None
    assert (
        result.inference.alpha
        == pytest.approx(0.01)
    )


def test_inference_can_be_disabled(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
            run_inference=False,
        )
    )

    assert result.inference is None


def test_invalid_alpha_rejected(
    dataframe,
):
    with pytest.raises(
        ValueError,
        match="alpha",
    ):
        TopicTargetAnalyzer().analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
            alpha=1.5,
        )


def test_inference_detects_clear_difference():
    samples = [
        pd.Series(
            [1.0, 1.2, 0.9, 1.1, 1.0]
        ).to_numpy(),
        pd.Series(
            [10.0, 10.2, 9.8, 10.1, 9.9]
        ).to_numpy(),
    ]

    result = (
        TopicTargetAnalyzer
        ._run_inference(
            samples=samples,
            alpha=0.05,
        )
    )

    assert result is not None
    assert result.anova.significant is True
    assert result.kruskal.significant is True


def test_welch_anova_available(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    assert result.inference is not None
    assert (
        result.inference
        .welch_anova
        .test
        == "Welch ANOVA"
    )


def test_effect_sizes_available(
    dataframe,
):
    result = (
        TopicTargetAnalyzer()
        .analyze(
            dataframe,
            "review_text",
            "note_maths",
            n_topics=3,
        )
    )

    inference = result.inference

    assert inference is not None

    assert (
        inference
        .eta_squared
        .measure
        == "eta_squared"
    )

    assert (
        inference
        .omega_squared
        .measure
        == "omega_squared"
    )

    assert (
        inference
        .epsilon_squared
        .measure
        == "epsilon_squared"
    )


def test_effect_sizes_bounded():
    samples = [
        np.array(
            [1.0, 1.1, 1.2, 0.9, 1.0]
        ),
        np.array(
            [5.0, 5.1, 4.9, 5.2, 5.0]
        ),
        np.array(
            [9.0, 9.1, 8.9, 9.2, 9.0]
        ),
    ]

    result = (
        TopicTargetAnalyzer
        ._run_inference(
            samples=samples,
            alpha=0.05,
        )
    )

    assert result is not None

    assert (
        0.0
        <= result.eta_squared.value
        <= 1.0
    )

    assert (
        0.0
        <= result.omega_squared.value
        <= 1.0
    )

    assert (
        0.0
        <= result.epsilon_squared.value
        <= 1.0
    )


def test_welch_detects_clear_difference():
    samples = [
        np.array(
            [1.0, 1.1, 0.9, 1.2, 1.0]
        ),
        np.array(
            [
                10.0,
                10.5,
                9.5,
                11.0,
                9.0,
            ]
        ),
    ]

    result = (
        TopicTargetAnalyzer
        ._welch_anova(
            samples=samples,
            alpha=0.05,
        )
    )

    assert result.statistic is not None
    assert result.p_value is not None
    assert result.significant is True


def test_heterogeneous_variances_recommend_welch():
    samples = [
        np.array(
            [
                10.0,
                10.1,
                9.9,
                10.0,
                10.1,
                9.9,
            ]
        ),
        np.array(
            [
                2.0,
                5.0,
                8.0,
                11.0,
                14.0,
                17.0,
            ]
        ),
    ]

    result = (
        TopicTargetAnalyzer
        ._run_inference(
            samples=samples,
            alpha=0.05,
        )
    )

    assert result is not None

    if result.equal_variances is False:
        assert (
            result.recommended_test
            == "Welch ANOVA"
        )
