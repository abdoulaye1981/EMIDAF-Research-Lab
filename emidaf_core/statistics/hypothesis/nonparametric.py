"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Nonparametric Tests
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .base import BaseHypothesisTest


class MannWhitneyTest(BaseHypothesisTest):

    name = "Mann-Whitney U"

    def test(
        self,
        group1,
        group2,
        alternative="two-sided"
    ):

        from scipy.stats import mannwhitneyu

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

        if alternative not in (
            "two-sided",
            "less",
            "greater"
        ):
            raise ValueError(
                "alternative doit être "
                "'two-sided', 'less' ou 'greater'."
            )

        statistic, p_value = mannwhitneyu(
            values1,
            values2,
            alternative=alternative
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : les deux distributions "
                "sont identiques."
            ),
            alternative_hypothesis=(
                "H1 : les deux distributions "
                "diffèrent."
            ),
            details={
                "n_group1": len(values1),
                "n_group2": len(values2),
                "median_group1":
                    float(np.median(values1)),
                "median_group2":
                    float(np.median(values2)),
                "alternative": alternative
            }
        )


class WilcoxonTest(BaseHypothesisTest):

    name = "Wilcoxon Signed-Rank"

    def test(
        self,
        before,
        after,
        alternative="two-sided"
    ):

        from scipy.stats import wilcoxon

        values1 = pd.Series(
            before
        ).reset_index(drop=True)

        values2 = pd.Series(
            after
        ).reset_index(drop=True)

        if len(values1) != len(values2):
            raise ValueError(
                "Les deux échantillons doivent "
                "avoir la même taille."
            )

        mask = (
            values1.notna()
            & values2.notna()
        )

        values1 = values1[mask].to_numpy()
        values2 = values2[mask].to_numpy()

        if len(values1) < 2:
            raise ValueError(
                "Au moins deux paires sont nécessaires."
            )

        if alternative not in (
            "two-sided",
            "less",
            "greater"
        ):
            raise ValueError(
                "alternative doit être "
                "'two-sided', 'less' ou 'greater'."
            )

        statistic, p_value = wilcoxon(
            values1,
            values2,
            alternative=alternative
        )

        differences = values2 - values1

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : la différence médiane "
                "entre les deux mesures est nulle."
            ),
            alternative_hypothesis=(
                "H1 : la différence médiane "
                "entre les deux mesures n'est pas nulle."
            ),
            details={
                "n_pairs": len(values1),
                "median_before":
                    float(np.median(values1)),
                "median_after":
                    float(np.median(values2)),
                "median_difference":
                    float(np.median(differences)),
                "alternative": alternative
            }
        )


class KruskalWallisTest(BaseHypothesisTest):

    name = "Kruskal-Wallis"

    def test(self, *groups):

        from scipy.stats import kruskal

        if len(groups) < 2:
            raise ValueError(
                "Le test de Kruskal-Wallis nécessite "
                "au moins deux groupes."
            )

        clean_groups = [
            pd.Series(group)
            .dropna()
            .to_numpy()
            for group in groups
        ]

        for group in clean_groups:

            if len(group) < 2:
                raise ValueError(
                    "Chaque groupe doit contenir "
                    "au moins deux observations."
                )

        statistic, p_value = kruskal(
            *clean_groups
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : les distributions des groupes "
                "sont identiques."
            ),
            alternative_hypothesis=(
                "H1 : au moins un groupe "
                "diffère des autres."
            ),
            details={
                "number_of_groups":
                    len(clean_groups),
                "group_sizes": [
                    len(group)
                    for group in clean_groups
                ],
                "group_medians": [
                    float(np.median(group))
                    for group in clean_groups
                ]
            }
        )


class FriedmanTest(BaseHypothesisTest):

    name = "Friedman"

    def test(self, *groups):

        from scipy.stats import friedmanchisquare

        if len(groups) < 3:
            raise ValueError(
                "Le test de Friedman nécessite "
                "au moins trois mesures."
            )

        clean_groups = [
            pd.Series(group)
            .dropna()
            .to_numpy()
            for group in groups
        ]

        sizes = [
            len(group)
            for group in clean_groups
        ]

        if len(set(sizes)) != 1:
            raise ValueError(
                "Toutes les mesures doivent "
                "avoir la même taille."
            )

        if sizes[0] < 2:
            raise ValueError(
                "Au moins deux observations "
                "sont nécessaires."
            )

        statistic, p_value = friedmanchisquare(
            *clean_groups
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : les distributions des mesures "
                "sont identiques."
            ),
            alternative_hypothesis=(
                "H1 : au moins une mesure "
                "diffère des autres."
            ),
            details={
                "number_of_measurements":
                    len(clean_groups),
                "n_subjects":
                    sizes[0],
                "medians": [
                    float(np.median(group))
                    for group in clean_groups
                ]
            }
        )


class SpearmanTest(BaseHypothesisTest):

    name = "Spearman Rank Correlation"

    def test(
        self,
        x,
        y
    ):

        from scipy.stats import spearmanr

        values = pd.DataFrame({
            "x": x,
            "y": y
        }).dropna()

        if len(values) < 3:
            raise ValueError(
                "Au moins trois observations "
                "sont nécessaires."
            )

        statistic, p_value = spearmanr(
            values["x"],
            values["y"]
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : il n'existe pas de "
                "corrélation monotone."
            ),
            alternative_hypothesis=(
                "H1 : il existe une corrélation "
                "monotone."
            ),
            details={
                "n": len(values),
                "correlation":
                    float(statistic),
                "correlation_type":
                    "Spearman"
            }
        )


def mann_whitney_test(
    group1,
    group2,
    alpha=0.05,
    alternative="two-sided"
):

    return MannWhitneyTest(
        alpha=alpha
    ).test(
        group1,
        group2,
        alternative
    )


def wilcoxon_test(
    before,
    after,
    alpha=0.05,
    alternative="two-sided"
):

    return WilcoxonTest(
        alpha=alpha
    ).test(
        before,
        after,
        alternative
    )


def kruskal_wallis_test(
    *groups,
    alpha=0.05
):

    return KruskalWallisTest(
        alpha=alpha
    ).test(*groups)


def friedman_test(
    *groups,
    alpha=0.05
):

    return FriedmanTest(
        alpha=alpha
    ).test(*groups)


def spearman_test(
    x,
    y,
    alpha=0.05
):

    return SpearmanTest(
        alpha=alpha
    ).test(
        x,
        y
    )
