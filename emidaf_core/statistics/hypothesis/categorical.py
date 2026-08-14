"""
=========================================================
EMIDAF Framework
Categorical Hypothesis Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Tests d'hypothèses pour variables catégorielles.

Contient

- Chi-Square Independence
- Fisher Exact
- McNemar
- Cochran's Q

=========================================================
"""

from __future__ import annotations

from abc import ABC

import pandas as pd

from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact

from statsmodels.stats.contingency_tables import (
    mcnemar,
    cochrans_q,
)

from ...common.results import HypothesisResult
from ..base.hypothesis_test import HypothesisTest


# ==========================================================
# BASE
# ==========================================================

class CategoricalTest(HypothesisTest, ABC):

    category = "Categorical"


# ==========================================================
# CHI SQUARE
# ==========================================================

class ChiSquare(CategoricalTest):

    name = "Chi-Square"

    @classmethod
    def compute(
        cls,
        x,
        y,
        alpha=0.05,
    ):

        table = pd.crosstab(

            x,

            y

        )

        statistic, pvalue, dof, expected = (

            chi2_contingency(

                table

            )

        )

        return HypothesisResult(

            test_name="Chi-Square",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=int(table.values.sum()),

            degrees_of_freedom=int(dof),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Variables are associated."

                if pvalue < alpha

                else "Variables are independent."

            ),

            extra={

                "observed":

                    table.values.tolist(),

                "expected":

                    expected.tolist()

            }

        )


# ==========================================================
# FISHER EXACT
# ==========================================================

class FishersExact(CategoricalTest):

    name = "Fisher Exact"

    @classmethod
    def compute(
        cls,
        table,
        alpha=0.05,
    ):

        if isinstance(

            table,

            pd.DataFrame

        ):

            contingency = table.values

        else:

            contingency = table

        odds_ratio, pvalue = fisher_exact(

            contingency

        )

        return HypothesisResult(

            test_name="Fisher Exact",

            statistic=float(odds_ratio),

            p_value=float(pvalue),

            alpha=alpha,

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Variables are associated."

                if pvalue < alpha

                else "Variables are independent."

            )

        )


# ==========================================================
# MCNEMAR
# ==========================================================

class McNemar(CategoricalTest):

    name = "McNemar"

    @classmethod
    def compute(
        cls,
        table,
        alpha=0.05,
    ):

        if isinstance(

            table,

            pd.DataFrame

        ):

            contingency = table.values

        else:

            contingency = table

        result = mcnemar(

            contingency,

            exact=False,

            correction=True

        )

        statistic = result.statistic

        pvalue = result.pvalue

        return HypothesisResult(

            test_name="McNemar",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "Marginal proportions differ."

                if pvalue < alpha

                else "No significant difference."

            )

        )


# ==========================================================
# COCHRAN Q
# ==========================================================

class CochranQ(CategoricalTest):

    name = "Cochran Q"

    @classmethod
    def compute(
        cls,
        dataframe,
        alpha=0.05,
    ):

        result = cochrans_q(

            dataframe

        )

        statistic = result.statistic

        pvalue = result.pvalue

        return HypothesisResult(

            test_name="Cochran Q",

            statistic=float(statistic),

            p_value=float(pvalue),

            alpha=alpha,

            sample_size=len(dataframe),

            reject_null=pvalue < alpha,

            significant=pvalue < alpha,

            decision=(

                "Reject H0"

                if pvalue < alpha

                else "Fail to Reject H0"

            ),

            interpretation=(

                "At least one treatment differs."

                if pvalue < alpha

                else "No treatment difference."

            )

        )


# ==========================================================
# SERVICE
# ==========================================================

class CategoricalTests:

    @staticmethod
    def chi_square(
        x,
        y,
        alpha=0.05,
    ):

        return ChiSquare.compute(

            x,

            y,

            alpha

        )

    @staticmethod
    def fisher(
        table,
        alpha=0.05,
    ):

        return FishersExact.compute(

            table,

            alpha

        )

    @staticmethod
    def mcnemar(
        table,
        alpha=0.05,
    ):

        return McNemar.compute(

            table,

            alpha

        )

    @staticmethod
    def cochran_q(
        dataframe,
        alpha=0.05,
    ):

        return CochranQ.compute(

            dataframe,

            alpha

        )

    @staticmethod
    def compute(
        x,
        y,
        alpha=0.05,
    ):

        return {

            "chi_square":

                ChiSquare.compute(

                    x,

                    y,

                    alpha

                )

        }