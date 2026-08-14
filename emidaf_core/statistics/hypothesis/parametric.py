"""
=========================================================
EMIDAF Framework
Parametric Hypothesis Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Tests paramétriques.

Contient

- Student Independent T-Test
- Welch T-Test
- Paired Student T-Test
- One-Way ANOVA
- One Sample T-Test
- F-Test

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np

from scipy.stats import (
    f,
    f_oneway,
    ttest_1samp,
    ttest_ind,
    ttest_rel,
)

from ...common.results import HypothesisResult
from ..base.hypothesis_test import HypothesisTest
from ..descriptive.validator import StatisticsValidator


# ==========================================================
# BASE
# ==========================================================

class ParametricTest(HypothesisTest, ABC):

    category = "Parametric"


# ==========================================================
# ONE SAMPLE T TEST
# ==========================================================

class OneSampleTTest(ParametricTest):

    name = "One Sample T-Test"

    @classmethod
    def compute(
        cls,
        values,
        population_mean,
        alpha=0.05,
    ):

        values = StatisticsValidator.require_numeric(values)

        statistic, pvalue = ttest_1samp(

            values,

            popmean=population_mean

        )

        return HypothesisResult(

            test_name="One Sample T-Test",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(values),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Population mean differs significantly."

                if pvalue < alpha

                else "No significant difference."

            )

        )


# ==========================================================
# STUDENT
# ==========================================================

class StudentTTest(ParametricTest):

    name = "Student Independent T-Test"

    @classmethod
    def compute(
        cls,
        group1,
        group2,
        alpha=0.05,
    ):

        g1 = StatisticsValidator.require_numeric(group1)

        g2 = StatisticsValidator.require_numeric(group2)

        statistic, pvalue = ttest_ind(

            g1,

            g2,

            equal_var=True

        )

        return HypothesisResult(

            test_name="Student T-Test",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(g1) + len(g2),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Means are significantly different."

                if pvalue < alpha

                else "Means are statistically equal."

            )

        )


# ==========================================================
# WELCH
# ==========================================================

class WelchTTest(ParametricTest):

    name = "Welch T-Test"

    @classmethod
    def compute(
        cls,
        group1,
        group2,
        alpha=0.05,
    ):

        g1 = StatisticsValidator.require_numeric(group1)

        g2 = StatisticsValidator.require_numeric(group2)

        statistic, pvalue = ttest_ind(

            g1,

            g2,

            equal_var=False

        )

        return HypothesisResult(

            test_name="Welch T-Test",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(g1) + len(g2),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Means are significantly different."

                if pvalue < alpha

                else "Means are statistically equal."

            )

        )


# ==========================================================
# PAIRED T TEST
# ==========================================================

class PairedTTest(ParametricTest):

    name = "Paired Student T-Test"

    @classmethod
    def compute(
        cls,
        before,
        after,
        alpha=0.05,
    ):

        before = StatisticsValidator.require_numeric(before)

        after = StatisticsValidator.require_numeric(after)

        statistic, pvalue = ttest_rel(

            before,

            after

        )

        return HypothesisResult(

            test_name="Paired Student T-Test",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(before),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Paired means differ."

                if pvalue < alpha

                else "No significant paired difference."

            )

        )


# ==========================================================
# ANOVA
# ==========================================================

class OneWayANOVA(ParametricTest):

    name = "One-Way ANOVA"

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

        statistic, pvalue = f_oneway(

            *samples

        )

        return HypothesisResult(

            test_name="One-Way ANOVA",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=sum(len(g) for g in samples),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "At least one group mean differs."

                if pvalue < alpha

                else "No significant difference."

            )

        )


# ==========================================================
# F TEST
# ==========================================================

class FTest(ParametricTest):

    name = "F-Test"

    @classmethod
    def compute(
        cls,
        group1,
        group2,
        alpha=0.05,
    ):

        g1 = StatisticsValidator.require_numeric(group1)

        g2 = StatisticsValidator.require_numeric(group2)

        var1 = np.var(

            g1,

            ddof=1

        )

        var2 = np.var(

            g2,

            ddof=1

        )

        statistic = var1 / var2

        dfn = len(g1) - 1

        dfd = len(g2) - 1

        pvalue = 2 * min(

            f.cdf(

                statistic,

                dfn,

                dfd

            ),

            1 - f.cdf(

                statistic,

                dfn,

                dfd

            )

        )

        return HypothesisResult(

            test_name="F-Test",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(g1) + len(g2),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Variances differ."

                if pvalue < alpha

                else "Variances are equal."

            )

        )


# ==========================================================
# SERVICE
# ==========================================================

class ParametricTests:

    @staticmethod
    def compute(
        group1,
        group2,
        alpha=0.05,
    ):

        return {

            "student":

                StudentTTest.compute(

                    group1,

                    group2,

                    alpha

                ),

            "welch":

                WelchTTest.compute(

                    group1,

                    group2,

                    alpha

                ),

            "f_test":

                FTest.compute(

                    group1,

                    group2,

                    alpha

                )

        }