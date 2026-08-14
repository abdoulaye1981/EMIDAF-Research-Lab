"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Proportions
=========================================================
"""

from __future__ import annotations

import numpy as np

from .base import BaseHypothesisTest


class OneSampleProportionTest(BaseHypothesisTest):

    name = "One-Sample Proportion Test"

    def test(
        self,
        successes,
        n,
        population_proportion=0.5,
        alternative="two-sided"
    ):

        if n <= 0:
            raise ValueError(
                "n doit être strictement positif."
            )

        if successes < 0 or successes > n:
            raise ValueError(
                "successes doit être compris entre 0 et n."
            )

        if not 0 < population_proportion < 1:
            raise ValueError(
                "La proportion théorique doit être comprise entre 0 et 1."
            )

        if alternative not in [
            "two-sided",
            "less",
            "greater"
        ]:
            raise ValueError(
                "alternative doit être 'two-sided', "
                "'less' ou 'greater'."
            )

        from scipy.stats import norm

        sample_proportion = successes / n

        standard_error = np.sqrt(
            population_proportion
            * (1 - population_proportion)
            / n
        )

        if standard_error == 0:
            raise ValueError(
                "L'erreur standard est nulle."
            )

        statistic = (
            sample_proportion
            - population_proportion
        ) / standard_error

        if alternative == "two-sided":

            p_value = 2 * norm.sf(
                abs(statistic)
            )

        elif alternative == "greater":

            p_value = norm.sf(
                statistic
            )

        else:

            p_value = norm.cdf(
                statistic
            )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                f"H0 : p = {population_proportion}"
            ),
            alternative_hypothesis=(
                f"H1 : p {self._alternative_symbol(alternative)} "
                f"{population_proportion}"
            ),
            details={
                "successes": successes,
                "n": n,
                "sample_proportion":
                    float(sample_proportion),
                "population_proportion":
                    population_proportion,
                "alternative": alternative
            }
        )

    @staticmethod
    def _alternative_symbol(
        alternative
    ):

        if alternative == "greater":
            return ">"

        if alternative == "less":
            return "<"

        return "≠"


class TwoSampleProportionTest(BaseHypothesisTest):

    name = "Two-Sample Proportion Test"

    def test(
        self,
        successes1,
        n1,
        successes2,
        n2,
        alternative="two-sided"
    ):

        if n1 <= 0 or n2 <= 0:
            raise ValueError(
                "Les tailles des deux échantillons "
                "doivent être strictement positives."
            )

        if successes1 < 0 or successes1 > n1:
            raise ValueError(
                "successes1 doit être compris entre 0 et n1."
            )

        if successes2 < 0 or successes2 > n2:
            raise ValueError(
                "successes2 doit être compris entre 0 et n2."
            )

        if alternative not in [
            "two-sided",
            "less",
            "greater"
        ]:
            raise ValueError(
                "alternative doit être 'two-sided', "
                "'less' ou 'greater'."
            )

        from scipy.stats import norm

        p1 = successes1 / n1
        p2 = successes2 / n2

        pooled_proportion = (
            successes1 + successes2
        ) / (
            n1 + n2
        )

        standard_error = np.sqrt(
            pooled_proportion
            * (1 - pooled_proportion)
            * (
                1 / n1
                + 1 / n2
            )
        )

        if standard_error == 0:
            raise ValueError(
                "L'erreur standard est nulle."
            )

        statistic = (
            p1 - p2
        ) / standard_error

        if alternative == "two-sided":

            p_value = 2 * norm.sf(
                abs(statistic)
            )

        elif alternative == "greater":

            p_value = norm.sf(
                statistic
            )

        else:

            p_value = norm.cdf(
                statistic
            )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : p1 = p2"
            ),
            alternative_hypothesis=(
                f"H1 : p1 "
                f"{self._alternative_symbol(alternative)} "
                f"p2"
            ),
            details={
                "successes1": successes1,
                "n1": n1,
                "successes2": successes2,
                "n2": n2,
                "proportion1": float(p1),
                "proportion2": float(p2),
                "difference": float(p1 - p2),
                "pooled_proportion":
                    float(pooled_proportion),
                "alternative": alternative
            }
        )

    @staticmethod
    def _alternative_symbol(
        alternative
    ):

        if alternative == "greater":
            return ">"

        if alternative == "less":
            return "<"

        return "≠"


def one_sample_proportion_test(
    successes,
    n,
    population_proportion=0.5,
    alpha=0.05,
    alternative="two-sided"
):

    return OneSampleProportionTest(
        alpha=alpha
    ).test(
        successes,
        n,
        population_proportion,
        alternative
    )


def two_sample_proportion_test(
    successes1,
    n1,
    successes2,
    n2,
    alpha=0.05,
    alternative="two-sided"
):

    return TwoSampleProportionTest(
        alpha=alpha
    ).test(
        successes1,
        n1,
        successes2,
        n2,
        alternative
    )
