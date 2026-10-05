"""
=========================================================
EMIDAF Framework
Adaptive Effect Sizes for Independent Groups
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from emidaf_core.statistics.effect_size.mean_difference import (
    MeanDifferenceEffectSize,
)
from emidaf_core.statistics.effect_size.nonparametric import (
    NonParametricEffectSize,
)
from emidaf_core.statistics.effect_size.anova import (
    AnovaEffectSize,
)


def _clean_groups(*groups):
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

    if len(clean) < 2:
        raise ValueError(
            "Au moins deux groupes sont nécessaires."
        )

    return clean


def _magnitude_standardized(value):
    value = abs(float(value))

    if value < 0.2:
        return "négligeable"

    if value < 0.5:
        return "faible"

    if value < 0.8:
        return "modérée"

    return "forte"


def _magnitude_r(value):
    value = abs(float(value))

    if value < 0.1:
        return "négligeable"

    if value < 0.3:
        return "faible"

    if value < 0.5:
        return "modérée"

    return "forte"


def _magnitude_eta_squared(value):
    value = max(
        0.0,
        float(value),
    )

    if value < 0.01:
        return "négligeable"

    if value < 0.06:
        return "faible"

    if value < 0.14:
        return "modérée"

    return "forte"


def _anova_components(groups):
    samples = _clean_groups(
        *groups
    )

    all_values = np.concatenate(
        samples
    )

    grand_mean = float(
        np.mean(all_values)
    )

    ss_between = float(
        sum(
            len(group)
            * (
                np.mean(group)
                - grand_mean
            ) ** 2
            for group in samples
        )
    )

    ss_within = float(
        sum(
            np.sum(
                (
                    group
                    - np.mean(group)
                ) ** 2
            )
            for group in samples
        )
    )

    ss_total = (
        ss_between
        + ss_within
    )

    k = len(samples)
    n = len(all_values)

    df_between = k - 1
    df_within = n - k

    ms_error = (
        ss_within
        / df_within
        if df_within > 0
        else np.nan
    )

    return {
        "samples": samples,
        "n": n,
        "k": k,
        "ss_between": ss_between,
        "ss_within": ss_within,
        "ss_total": ss_total,
        "df_between": df_between,
        "df_within": df_within,
        "ms_error": ms_error,
    }


class GroupEffectSize:
    """
    Taille d'effet adaptée au test sélectionné
    par GroupTestSelector.
    """

    @staticmethod
    def compute(
        selection,
        *groups,
    ):
        if not isinstance(
            selection,
            dict,
        ):
            raise TypeError(
                "selection doit être le dictionnaire "
                "renvoyé par GroupTestSelector."
            )

        selected_test = (
            selection.get(
                "selected_test"
            )
        )

        samples = _clean_groups(
            *groups
        )

        # ==================================================
        # 2 GROUPES : WELCH
        # ==================================================

        if selected_test == "welch":

            if len(samples) != 2:
                raise ValueError(
                    "Hedges g nécessite exactement "
                    "deux groupes."
                )

            effect = (
                MeanDifferenceEffectSize
                .hedges_g(
                    samples[0],
                    samples[1],
                )
            )

            value = float(
                effect.statistic
            )

            return {
                "name": "Hedges g",
                "value": value,
                "magnitude":
                    _magnitude_standardized(
                        value
                    ),
                "direction": (
                    "groupe_1_superieur"
                    if value > 0
                    else
                    "groupe_2_superieur"
                    if value < 0
                    else
                    "aucune"
                ),
                "basis":
                    "welch_two_groups",
                "descriptive_only":
                    False,
            }

        # ==================================================
        # 2 GROUPES : MANN-WHITNEY
        # ==================================================

        if selected_test == "mann_whitney":

            if len(samples) != 2:
                raise ValueError(
                    "La taille d'effet rank-biserial "
                    "nécessite exactement deux groupes."
                )

            result = selection.get(
                "result"
            )

            if result is None:
                raise ValueError(
                    "Résultat Mann-Whitney absent."
                )

            u = float(
                result.statistic
            )

            n1 = len(
                samples[0]
            )

            n2 = len(
                samples[1]
            )

            effect = (
                NonParametricEffectSize
                .rank_biserial(
                    u,
                    n1,
                    n2,
                )
            )

            value = float(
                effect.statistic
            )

            return {
                "name":
                    "Rank-biserial correlation",
                "value": value,
                "magnitude":
                    _magnitude_r(
                        value
                    ),
                "direction": (
                    "groupe_1_superieur"
                    if value > 0
                    else
                    "groupe_2_superieur"
                    if value < 0
                    else
                    "aucune"
                ),
                "basis":
                    "mann_whitney",
                "descriptive_only":
                    False,
            }

        # ==================================================
        # ANOVA CLASSIQUE
        # ==================================================

        if selected_test == "anova":

            components = (
                _anova_components(
                    samples
                )
            )

            eta = (
                AnovaEffectSize
                .eta_squared(
                    components[
                        "ss_between"
                    ],
                    components[
                        "ss_total"
                    ],
                )
            )

            omega = (
                AnovaEffectSize
                .omega_squared(
                    components[
                        "ss_between"
                    ],
                    components[
                        "df_between"
                    ],
                    components[
                        "ms_error"
                    ],
                    components[
                        "ss_total"
                    ],
                )
            )

            eta_value = float(
                eta.statistic
            )

            omega_value = float(
                omega.statistic
            )

            return {
                "name":
                    "Omega Squared",
                "value":
                    omega_value,
                "magnitude":
                    _magnitude_eta_squared(
                        omega_value
                    ),
                "secondary": {
                    "name":
                        "Eta Squared",
                    "value":
                        eta_value,
                },
                "basis":
                    "one_way_anova",
                "descriptive_only":
                    False,
            }

        # ==================================================
        # WELCH ANOVA
        # ==================================================

        if selected_test == "welch_anova":

            components = (
                _anova_components(
                    samples
                )
            )

            eta = (
                AnovaEffectSize
                .eta_squared(
                    components[
                        "ss_between"
                    ],
                    components[
                        "ss_total"
                    ],
                )
            )

            eta_value = float(
                eta.statistic
            )

            return {
                "name":
                    "Eta Squared (descriptive)",
                "value":
                    eta_value,
                "magnitude":
                    _magnitude_eta_squared(
                        eta_value
                    ),
                "basis":
                    "welch_anova_descriptive",
                "descriptive_only":
                    True,
                "note": (
                    "Taille d'effet descriptive calculée "
                    "à partir des sommes des carrés brutes. "
                    "Elle n'est pas une taille d'effet "
                    "spécifique au test de Welch."
                ),
            }

        # ==================================================
        # KRUSKAL-WALLIS
        # ==================================================

        if selected_test == "kruskal":

            result = selection.get(
                "result"
            )

            if result is None:
                raise ValueError(
                    "Résultat Kruskal-Wallis absent."
                )

            h = float(
                result.statistic
            )

            n = sum(
                len(group)
                for group in samples
            )

            k = len(
                samples
            )

            denominator = (
                n - k
            )

            if denominator <= 0:
                raise ValueError(
                    "Effectif insuffisant pour "
                    "epsilon squared."
                )

            epsilon_squared = (
                h - k + 1
            ) / denominator

            epsilon_squared = max(
                0.0,
                float(
                    epsilon_squared
                ),
            )

            return {
                "name":
                    "Kruskal-Wallis epsilon squared",
                "value":
                    epsilon_squared,
                "magnitude":
                    _magnitude_eta_squared(
                        epsilon_squared
                    ),
                "basis":
                    "kruskal_wallis",
                "descriptive_only":
                    False,
            }

        raise ValueError(
            "Test sélectionné non pris en charge : "
            f"{selected_test}"
        )
