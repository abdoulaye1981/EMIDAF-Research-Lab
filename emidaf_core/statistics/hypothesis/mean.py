"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Means
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .base import BaseHypothesisTest


class OneSampleTTest(BaseHypothesisTest):

    name = "One-Sample t-test"

    def test(
        self,
        data,
        population_mean=0
    ):

        from scipy.stats import ttest_1samp

        values = (
            pd.Series(data)
            .dropna()
            .to_numpy()
        )

        if len(values) < 2:
            raise ValueError(
                "Au moins deux observations sont nécessaires."
            )

        statistic, p_value = ttest_1samp(
            values,
            population_mean
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                f"H0 : μ = {population_mean}"
            ),
            alternative_hypothesis=(
                f"H1 : μ ≠ {population_mean}"
            ),
            details={
                "n": len(values),
                "sample_mean": float(np.mean(values)),
                "population_mean": population_mean
            }
        )


class IndependentTTest(BaseHypothesisTest):

    name = "Independent Two-Sample t-test"

    def __init__(
        self,
        alpha=0.05,
        equal_var=True
    ):

        super().__init__(
            alpha=alpha
        )

        self.equal_var = equal_var

    def test(
        self,
        group1,
        group2
    ):

        from scipy.stats import ttest_ind

        values1 = (
            pd.Series(group1)
            .dropna()
            .to_numpy()
        )

        values2 = (
            pd.Series(group2)
            .dropna()
            .to_numpy()
        )

        if len(values1) < 2 or len(values2) < 2:
            raise ValueError(
                "Chaque groupe doit contenir au moins "
                "deux observations."
            )

        statistic, p_value = ttest_ind(
            values1,
            values2,
            equal_var=self.equal_var
        )

        test_type = (
            "Student"
            if self.equal_var
            else "Welch"
        )

        self.name = (
            f"Independent Two-Sample "
            f"t-test ({test_type})"
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : les deux moyennes sont égales."
            ),
            alternative_hypothesis=(
                "H1 : les deux moyennes sont différentes."
            ),
            details={
                "test_type": test_type,
                "equal_var": self.equal_var,
                "n_group1": len(values1),
                "n_group2": len(values2),
                "mean_group1": float(
                    np.mean(values1)
                ),
                "mean_group2": float(
                    np.mean(values2)
                ),
                "mean_difference": float(
                    np.mean(values1)
                    - np.mean(values2)
                )
            }
        )


class PairedTTest(BaseHypothesisTest):

    name = "Paired t-test"

    def test(
        self,
        before,
        after
    ):

        from scipy.stats import ttest_rel

        values1 = (
            pd.Series(before)
            .dropna()
        )

        values2 = (
            pd.Series(after)
            .dropna()
        )

        if len(values1) != len(values2):
            raise ValueError(
                "Les deux échantillons appariés "
                "doivent avoir la même taille."
            )

        if len(values1) < 2:
            raise ValueError(
                "Au moins deux paires sont nécessaires."
            )

        statistic, p_value = ttest_rel(
            values1,
            values2
        )

        differences = (
            values2.to_numpy()
            - values1.to_numpy()
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : la différence moyenne entre "
                "les deux mesures est nulle."
            ),
            alternative_hypothesis=(
                "H1 : la différence moyenne entre "
                "les deux mesures n'est pas nulle."
            ),
            details={
                "n_pairs": len(values1),
                "mean_before": float(
                    values1.mean()
                ),
                "mean_after": float(
                    values2.mean()
                ),
                "mean_difference": float(
                    differences.mean()
                )
            }
        )


def one_sample_t_test(
    data,
    population_mean=0,
    alpha=0.05
):

    return OneSampleTTest(
        alpha=alpha
    ).test(
        data,
        population_mean
    )


def independent_t_test(
    group1,
    group2,
    alpha=0.05,
    equal_var=True
):

    return IndependentTTest(
        alpha=alpha,
        equal_var=equal_var
    ).test(
        group1,
        group2
    )


def welch_t_test(
    group1,
    group2,
    alpha=0.05
):

    return IndependentTTest(
        alpha=alpha,
        equal_var=False
    ).test(
        group1,
        group2
    )


def paired_t_test(
    before,
    after,
    alpha=0.05
):

    return PairedTTest(
        alpha=alpha
    ).test(
        before,
        after
    )
