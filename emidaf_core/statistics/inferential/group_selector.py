"""
=========================================================
EMIDAF Framework
Adaptive Group Test Selector
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from .two_samples import (
    WelchTTest,
    MannWhitneyTest,
)
from .k_samples import (
    OneWayANOVA,
    WelchANOVA,
    KruskalWallisTest,
)
from .variance import BrownForsytheTest


class GroupTestSelector:
    """
    Sélection adaptative d'un test pour groupes indépendants.

    La décision ne repose pas uniquement sur Shapiro-Wilk.
    Pour les groupes de taille suffisante, la compatibilité
    paramétrique est principalement évaluée par la forme
    de la distribution : skewness et kurtosis.
    """

    def __init__(
        self,
        alpha=0.05,
        small_sample_threshold=20,
        skewness_limit=1.0,
        kurtosis_limit=1.0,
    ):
        self.alpha = alpha
        self.small_sample_threshold = (
            small_sample_threshold
        )
        self.skewness_limit = (
            skewness_limit
        )
        self.kurtosis_limit = (
            kurtosis_limit
        )

    @staticmethod
    def _clean_group(group):
        values = np.asarray(
            group,
            dtype=float,
        )

        return values[
            np.isfinite(values)
        ]

    def _diagnose_group(
        self,
        group,
        index,
    ):
        values = self._clean_group(
            group
        )

        n = len(values)

        if n < 3:
            raise ValueError(
                "Chaque groupe doit contenir au moins "
                "trois observations valides pour la "
                "sélection adaptative."
            )

        skewness = float(
            stats.skew(
                values,
                bias=False,
            )
        )

        kurtosis = float(
            stats.kurtosis(
                values,
                fisher=True,
                bias=False,
            )
        )

        shapiro_statistic = None
        shapiro_p_value = None
        shapiro_normal = None

        if np.unique(values).size > 1:
            shapiro_result = (
                stats.shapiro(values)
            )

            shapiro_statistic = float(
                shapiro_result.statistic
            )

            shapiro_p_value = float(
                shapiro_result.pvalue
            )

            shapiro_normal = (
                shapiro_p_value
                > self.alpha
            )

        shape_compatible = (
            abs(skewness)
            < self.skewness_limit
            and
            abs(kurtosis)
            < self.kurtosis_limit
        )

        if n < self.small_sample_threshold:
            parametric_compatible = (
                shape_compatible
                and
                shapiro_normal is True
            )

            decision_basis = (
                "small_sample_shape_and_shapiro"
            )

        else:
            parametric_compatible = (
                shape_compatible
            )

            decision_basis = (
                "large_sample_shape_diagnostics"
            )

        return {
            "group_index": index,
            "n": n,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "shapiro_statistic":
                shapiro_statistic,
            "shapiro_p_value":
                shapiro_p_value,
            "shapiro_normal":
                shapiro_normal,
            "shape_compatible":
                shape_compatible,
            "parametric_compatible":
                parametric_compatible,
            "decision_basis":
                decision_basis,
        }

    def select(
        self,
        *groups,
        outcome_semantic=None,
    ):
        if len(groups) < 2:
            raise ValueError(
                "Au moins deux groupes sont nécessaires."
            )

        clean_groups = [
            self._clean_group(group)
            for group in groups
        ]

        diagnostics = [
            self._diagnose_group(
                group,
                index,
            )
            for index, group
            in enumerate(
                clean_groups,
                start=1,
            )
        ]

        parametric_compatible = all(
            item[
                "parametric_compatible"
            ]
            for item in diagnostics
        )

        number_of_groups = len(
            clean_groups
        )

        variance_test = None
        variance_p_value = None
        variance_homogeneous = None

        # ==================================================
        # PRIORITÉ AU TYPE SÉMANTIQUE
        # ==================================================
        #
        # Une variable ordinale doit être analysée avec
        # des méthodes fondées sur les rangs, même si sa
        # distribution numérique paraît compatible avec
        # une approche paramétrique.
        #
        # Cette règle évite de traiter automatiquement
        # une échelle ordinale (par exemple Likert 1–5)
        # comme une variable quantitative continue.
        # ==================================================

        if outcome_semantic == "ordinal":

            if number_of_groups == 2:
                selected_test = (
                    "mann_whitney"
                )

                reason = (
                    "ordinal_outcome_two_groups"
                )

                result = (
                    MannWhitneyTest()
                    .compute(
                        x=clean_groups[0],
                        y=clean_groups[1],
                        alpha=self.alpha,
                    )
                )

            else:
                selected_test = "kruskal"

                reason = (
                    "ordinal_outcome_k_groups"
                )

                result = (
                    KruskalWallisTest()
                    .compute(
                        *clean_groups,
                        alpha=self.alpha,
                    )
                )

            return {
                "selected_test":
                    selected_test,
                "test_name":
                    result.test,
                "number_of_groups":
                    number_of_groups,
                "alpha":
                    self.alpha,
                "outcome_semantic":
                    outcome_semantic,
                "parametric_compatible":
                    False,
                "variance_test":
                    None,
                "variance_p_value":
                    None,
                "variance_homogeneous":
                    None,
                "reason":
                    reason,
                "group_diagnostics":
                    diagnostics,
                "result":
                    result,
            }

        if number_of_groups == 2:

            if parametric_compatible:
                selected_test = "welch"
                reason = (
                    "parametric_compatible_two_groups"
                )

                result = WelchTTest().compute(
                    x=clean_groups[0],
                    y=clean_groups[1],
                    alpha=self.alpha,
                )

            else:
                selected_test = (
                    "mann_whitney"
                )
                reason = (
                    "parametric_incompatible_two_groups"
                )

                result = (
                    MannWhitneyTest()
                    .compute(
                        x=clean_groups[0],
                        y=clean_groups[1],
                        alpha=self.alpha,
                    )
                )

        else:

            if not parametric_compatible:
                selected_test = "kruskal"
                reason = (
                    "parametric_incompatible_k_groups"
                )

                result = (
                    KruskalWallisTest()
                    .compute(
                        *clean_groups,
                        alpha=self.alpha,
                    )
                )

            else:
                variance_result = (
                    BrownForsytheTest()
                    .compute(
                        *clean_groups,
                        alpha=self.alpha,
                    )
                )

                variance_test = (
                    "Brown-Forsythe"
                )

                variance_p_value = float(
                    variance_result.p_value
                )

                variance_homogeneous = (
                    not variance_result.reject_null
                )

                if variance_homogeneous:
                    selected_test = "anova"

                    reason = (
                        "parametric_compatible_"
                        "equal_variances"
                    )

                    result = (
                        OneWayANOVA()
                        .compute(
                            *clean_groups,
                            alpha=self.alpha,
                        )
                    )

                else:
                    selected_test = (
                        "welch_anova"
                    )

                    reason = (
                        "parametric_compatible_"
                        "unequal_variances"
                    )

                    result = (
                        WelchANOVA()
                        .compute(
                            *clean_groups,
                            alpha=self.alpha,
                        )
                    )

        return {
            "selected_test":
                selected_test,
            "test_name":
                result.test,
            "number_of_groups":
                number_of_groups,
            "alpha":
                self.alpha,
            "outcome_semantic":
                outcome_semantic,
            "parametric_compatible":
                parametric_compatible,
            "variance_test":
                variance_test,
            "variance_p_value":
                variance_p_value,
            "variance_homogeneous":
                variance_homogeneous,
            "reason":
                reason,
            "group_diagnostics":
                diagnostics,
            "result":
                result,
        }
