"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Normality
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .base import BaseHypothesisTest


class ShapiroTest(BaseHypothesisTest):

    name = "Shapiro-Wilk"

    def test(self, data):

        from scipy.stats import shapiro

        values = pd.Series(data).dropna()

        if len(values) < 3:
            raise ValueError(
                "Le test de Shapiro nécessite au moins 3 observations."
            )

        statistic, p_value = shapiro(values)

        return self._create_result(
            statistic=statistic,
            p_value=p_value,
            null_hypothesis=(
                "H0 : les données suivent une loi normale."
            ),
            alternative_hypothesis=(
                "H1 : les données ne suivent pas une loi normale."
            ),
            details={
                "n": len(values)
            }
        )


class NormalityTest(BaseHypothesisTest):

    name = "D'Agostino-Pearson"

    def test(self, data):

        from scipy.stats import normaltest

        values = pd.Series(data).dropna()

        if len(values) < 8:
            raise ValueError(
                "Le test de D'Agostino-Pearson nécessite "
                "au moins 8 observations."
            )

        statistic, p_value = normaltest(values)

        return self._create_result(
            statistic=statistic,
            p_value=p_value,
            null_hypothesis=(
                "H0 : les données suivent une loi normale."
            ),
            alternative_hypothesis=(
                "H1 : les données ne suivent pas une loi normale."
            ),
            details={
                "n": len(values)
            }
        )


class AndersonTest(BaseHypothesisTest):

    name = "Anderson-Darling"

    def test(self, data):

        from scipy.stats import anderson

        values = pd.Series(data).dropna()

        if len(values) < 3:
            raise ValueError(
                "Le test d'Anderson-Darling nécessite "
                "au moins 3 observations."
            )

        result = anderson(
            values,
            dist="norm"
        )

        statistic = float(
            result.statistic
        )

        significance_levels = (
            np.asarray(
                result.significance_level
            )
        )

        critical_values = (
            np.asarray(
                result.critical_values
            )
        )

        alpha_index = np.argmin(
            np.abs(
                significance_levels
                - self.alpha * 100
            )
        )

        critical_value = float(
            critical_values[alpha_index]
        )

        reject_null = (
            statistic > critical_value
        )

        output = self._create_result(
            statistic=statistic,
            p_value=None,
            null_hypothesis=(
                "H0 : les données suivent une loi normale."
            ),
            alternative_hypothesis=(
                "H1 : les données ne suivent pas une loi normale."
            ),
            details={
                "n": len(values),
                "critical_value": critical_value,
                "significance_level":
                    float(
                        significance_levels[
                            alpha_index
                        ]
                    )
            }
        )

        output.reject_null = reject_null

        if reject_null:
            output.conclusion = (
                "Rejet de l'hypothèse nulle."
            )
        else:
            output.conclusion = (
                "Non-rejet de l'hypothèse nulle."
            )

        return output


def shapiro_test(
    data,
    alpha=0.05
):

    return ShapiroTest(
        alpha=alpha
    ).test(data)


def normality_test(
    data,
    alpha=0.05
):

    return NormalityTest(
        alpha=alpha
    ).test(data)


def anderson_test(
    data,
    alpha=0.05
):

    return AndersonTest(
        alpha=alpha
    ).test(data)
