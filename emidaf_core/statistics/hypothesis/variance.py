"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Variance
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base import BaseHypothesisTest


class LeveneTest(BaseHypothesisTest):

    name = "Levene"

    def test(self, *groups):

        from scipy.stats import levene

        if len(groups) < 2:
            raise ValueError(
                "Le test de Levene nécessite au moins deux groupes."
            )

        clean_groups = [
            pd.Series(group).dropna().to_numpy()
            for group in groups
        ]

        statistic, p_value = levene(
            *clean_groups
        )

        return self._create_result(
            statistic=statistic,
            p_value=p_value,
            null_hypothesis=(
                "H0 : les variances des groupes sont égales."
            ),
            alternative_hypothesis=(
                "H1 : au moins une variance diffère."
            ),
            details={
                "number_of_groups": len(clean_groups),
                "group_sizes": [
                    len(group)
                    for group in clean_groups
                ]
            }
        )


class BartlettTest(BaseHypothesisTest):

    name = "Bartlett"

    def test(self, *groups):

        from scipy.stats import bartlett

        if len(groups) < 2:
            raise ValueError(
                "Le test de Bartlett nécessite au moins deux groupes."
            )

        clean_groups = [
            pd.Series(group).dropna().to_numpy()
            for group in groups
        ]

        statistic, p_value = bartlett(
            *clean_groups
        )

        return self._create_result(
            statistic=statistic,
            p_value=p_value,
            null_hypothesis=(
                "H0 : les variances des groupes sont égales."
            ),
            alternative_hypothesis=(
                "H1 : au moins une variance diffère."
            ),
            details={
                "number_of_groups": len(clean_groups),
                "group_sizes": [
                    len(group)
                    for group in clean_groups
                ]
            }
        )


def levene_test(
    *groups,
    alpha=0.05
):

    return LeveneTest(
        alpha=alpha
    ).test(*groups)


def bartlett_test(
    *groups,
    alpha=0.05
):

    return BartlettTest(
        alpha=alpha
    ).test(*groups)
