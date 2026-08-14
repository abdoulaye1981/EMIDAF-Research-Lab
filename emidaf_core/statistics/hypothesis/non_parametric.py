"""
=========================================================
EMIDAF Framework
Non Parametric Hypothesis Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Tests non paramétriques.

Contient

- Mann-Whitney U
- Wilcoxon Signed-Rank
- Kruskal-Wallis
- Friedman
- Mood Median Test
- Sign Test

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np

from scipy.stats import (
    friedmanchisquare,
    kruskal,
    median_test,
    mannwhitneyu,
    wilcoxon,
)

from ...common.results import HypothesisResult
from ..base.hypothesis_test import HypothesisTest
from ..descriptive.validator import StatisticsValidator


# ==========================================================
# BASE
# ==========================================================

class NonParametricTest(HypothesisTest, ABC):

    category = "Non Parametric"


# ==========================================================
# MANN-WHITNEY
# ==========================================================

class MannWhitney(NonParametricTest):

    name = "Mann-Whitney U"

    @classmethod
    def compute(
        cls,
        group1,
        group2,
        alpha=0.05,
    ):

        g1 = StatisticsValidator.require_numeric(group1)

        g2 = StatisticsValidator.require_numeric(group2)

        statistic, pvalue = mannwhitneyu(

            g1,

            g2,

            alternative="two-sided"

        )

        return HypothesisResult(

            test_name="Mann-Whitney U",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(g1) + len(g2),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision="Reject H0" if pvalue < alpha else "Fail to Reject H0",

            interpretation="Groups differ significantly."
            if pvalue < alpha
            else "No significant difference."

        )


# ==========================================================
# WILCOXON
# ==========================================================

class Wilcoxon(NonParametricTest):

    name = "Wilcoxon Signed Rank"

    @classmethod
    def compute(
        cls,
        before,
        after,
        alpha=0.05,
    ):

        before = StatisticsValidator.require_numeric(before)

        after = StatisticsValidator.require_numeric(after)

        statistic, pvalue = wilcoxon(

            before,

            after

        )

        return HypothesisResult(

            test_name="Wilcoxon",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(before),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision="Reject H0" if pvalue < alpha else "Fail to Reject H0",

            interpretation="Paired samples differ."
            if pvalue < alpha
            else "No paired difference."

        )


# ==========================================================
# KRUSKAL WALLIS
# ==========================================================

class KruskalWallis(NonParametricTest):

    name = "Kruskal-Wallis"

    @classmethod
    def compute(
        cls,
        *groups,
        alpha=0.05,
    ):

        samples = [

            StatisticsValidator.require_numeric(g)

            for g in groups

        ]

        statistic, pvalue = kruskal(

            *samples

        )

        return HypothesisResult(

            test_name="Kruskal-Wallis",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=sum(len(g) for g in samples),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision="Reject H0" if pvalue < alpha else "Fail to Reject H0",

            interpretation="At least one group differs."
            if pvalue < alpha
            else "No significant difference."

        )


# ==========================================================
# FRIEDMAN
# ==========================================================

class Friedman(NonParametricTest):

    name = "Friedman"

    @classmethod
    def compute(
        cls,
        *groups,
        alpha=0.05,
    ):

        samples = [

            StatisticsValidator.require_numeric(g)

            for g in groups

        ]

        statistic, pvalue = friedmanchisquare(

            *samples

        )

        return HypothesisResult(

            test_name="Friedman",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=sum(len(g) for g in samples),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision="Reject H0" if pvalue < alpha else "Fail to Reject H0",

            interpretation="Repeated measures differ."
            if pvalue < alpha
            else "No repeated-measures difference."

        )


# ==========================================================
# MOOD MEDIAN TEST
# ==========================================================

class MoodMedianTest(NonParametricTest):

    name = "Mood Median Test"

    @classmethod
    def compute(
        cls,
        *groups,
        alpha=0.05,
    ):

        statistic, pvalue, median, table = median_test(

            *groups

        )

        return HypothesisResult(

            test_name="Mood Median",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=sum(len(g) for g in groups),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision="Reject H0" if pvalue < alpha else "Fail to Reject H0",

            interpretation="Medians differ."
            if pvalue < alpha
            else "No median difference.",

            extra={

                "median": float(median),

                "table": table.tolist()

            }

        )


# ==========================================================
# SIGN TEST
# ==========================================================

class SignTest(NonParametricTest):

    """
    Test des signes.

    Implémentation simple basée sur
    les différences positives/négatives.
    """

    name = "Sign Test"

    @classmethod
    def compute(
        cls,
        before,
        after,
        alpha=0.05,
    ):

        before = StatisticsValidator.require_numeric(before)

        after = StatisticsValidator.require_numeric(after)

        diff = after - before

        positive = int((diff > 0).sum())

        negative = int((diff < 0).sum())

        statistic = min(

            positive,

            negative

        )

        return HypothesisResult(

            test_name="Sign Test",

            statistic=float(statistic),

            alpha=alpha,

            sample_size=len(diff),

            interpretation=(

                "Positive differences: "

                f"{positive}, "

                f"Negative differences: "

                f"{negative}"

            ),

            extra={

                "positive": positive,

                "negative": negative

            }

        )


# ==========================================================
# SERVICE
# ==========================================================

class NonParametricTests:

    @staticmethod
    def compute(
        group1,
        group2,
        alpha=0.05,
    ):

        return {

            "mann_whitney":

                MannWhitney.compute(

                    group1,

                    group2,

                    alpha

                ),

            "wilcoxon":

                Wilcoxon.compute(

                    group1,

                    group2,

                    alpha

                )

        }