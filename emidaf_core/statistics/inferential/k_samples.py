"""
=========================================================
EMIDAF Framework
K Independent Samples Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np
from scipy import stats
from statsmodels.stats.oneway import anova_oneway

from .base import (
    BaseInferentialTest,
    InferentialResult,
)


def _clean_groups(*groups):
    """
    Nettoie et valide des groupes indépendants numériques.
    """

    if len(groups) < 2:
        raise ValueError(
            "Au moins deux groupes sont nécessaires."
        )

    clean = []

    for group in groups:
        values = np.asarray(
            group,
            dtype=float,
        )

        values = values[
            np.isfinite(values)
        ]

        if len(values) < 2:
            raise ValueError(
                "Chaque groupe doit contenir au moins "
                "deux observations valides."
            )

        clean.append(values)

    return clean


class OneWayANOVA(
    BaseInferentialTest
):
    """
    ANOVA classique à un facteur.

    Hypothèse d'égalité des variances requise.
    """

    name = "One-Way ANOVA"

    def compute(
        self,
        *groups,
        alpha=0.05,
    ):
        samples = _clean_groups(
            *groups
        )

        statistic, p_value = (
            stats.f_oneway(
                *samples
            )
        )

        return InferentialResult(
            test=self.name,
            statistic=float(
                statistic
            ),
            p_value=float(
                p_value
            ),
            alpha=alpha,
            reject_null=(
                p_value < alpha
            ),
            metadata={
                "number_of_groups":
                    len(samples),
                "group_sizes": [
                    len(group)
                    for group in samples
                ],
                "variance_assumption":
                    "equal",
            },
        )


class WelchANOVA(
    BaseInferentialTest
):
    """
    ANOVA de Welch à un facteur.

    Adaptée aux variances inégales.
    """

    name = "Welch ANOVA"

    def compute(
        self,
        *groups,
        alpha=0.05,
    ):
        samples = _clean_groups(
            *groups
        )

        result = anova_oneway(
            samples,
            use_var="unequal",
            welch_correction=True,
        )

        statistic = float(
            result.statistic
        )

        p_value = float(
            result.pvalue
        )

        metadata = {
            "number_of_groups":
                len(samples),
            "group_sizes": [
                len(group)
                for group in samples
            ],
            "variance_assumption":
                "unequal",
            "welch_correction":
                True,
        }

        if hasattr(
            result,
            "df",
        ):
            try:
                df = result.df

                metadata[
                    "df_num"
                ] = float(df[0])

                metadata[
                    "df_denom"
                ] = float(df[1])

            except (
                TypeError,
                ValueError,
                IndexError,
            ):
                pass

        return InferentialResult(
            test=self.name,
            statistic=statistic,
            p_value=p_value,
            alpha=alpha,
            reject_null=(
                p_value < alpha
            ),
            metadata=metadata,
        )


class KruskalWallisTest(
    BaseInferentialTest
):
    """
    Test non paramétrique de Kruskal-Wallis.
    """

    name = "Kruskal-Wallis"

    def compute(
        self,
        *groups,
        alpha=0.05,
    ):
        samples = _clean_groups(
            *groups
        )

        statistic, p_value = (
            stats.kruskal(
                *samples
            )
        )

        return InferentialResult(
            test=self.name,
            statistic=float(
                statistic
            ),
            p_value=float(
                p_value
            ),
            alpha=alpha,
            reject_null=(
                p_value < alpha
            ),
            metadata={
                "number_of_groups":
                    len(samples),
                "group_sizes": [
                    len(group)
                    for group in samples
                ],
                "method":
                    "rank_based",
            },
        )


class KSamples:
    """
    Façade des tests pour k groupes indépendants.
    """

    registry = {
        "anova":
            OneWayANOVA,
        "welch_anova":
            WelchANOVA,
        "kruskal":
            KruskalWallisTest,
    }

    @classmethod
    def compute(
        cls,
        method,
        *groups,
        **kwargs,
    ):
        if method not in cls.registry:
            raise ValueError(
                "Méthode inconnue : "
                f"{method}. "
                "Méthodes disponibles : "
                f"{list(cls.registry.keys())}"
            )

        model = cls.registry[
            method
        ]()

        return model.compute(
            *groups,
            **kwargs,
        )
