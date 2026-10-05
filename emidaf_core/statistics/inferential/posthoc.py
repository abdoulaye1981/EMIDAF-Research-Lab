"""
=========================================================
EMIDAF Framework
Adaptive Post-Hoc Tests for Independent Groups
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import (
    pairwise_tukeyhsd,
)
from statsmodels.stats.multitest import (
    multipletests,
)


def _clean_groups(
    groups,
    labels=None,
):
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

    if labels is None:
        labels = [
            f"Groupe {index}"
            for index in range(
                1,
                len(clean) + 1,
            )
        ]

    if len(labels) != len(clean):
        raise ValueError(
            "Le nombre de labels doit correspondre "
            "au nombre de groupes."
        )

    labels = [
        str(label)
        for label in labels
    ]

    if len(set(labels)) != len(labels):
        raise ValueError(
            "Les labels des groupes doivent être uniques."
        )

    return clean, labels


def _flatten_groups(
    groups,
    labels,
):
    values = np.concatenate(
        groups
    )

    group_labels = np.concatenate(
        [
            np.repeat(
                label,
                len(group),
            )
            for label, group
            in zip(
                labels,
                groups,
            )
        ]
    )

    return values, group_labels


def _statsmodels_pairwise_records(
    result,
):
    groups_unique = [
        str(value)
        for value in (
            result._multicomp
            .groupsunique
        )
    ]

    pairs = list(
        combinations(
            range(
                len(groups_unique)
            ),
            2,
        )
    )

    records = []

    for index, (
        left_index,
        right_index,
    ) in enumerate(pairs):

        lower = float(
            result.confint[
                index,
                0,
            ]
        )

        upper = float(
            result.confint[
                index,
                1,
            ]
        )

        records.append(
            {
                "group_1":
                    groups_unique[
                        left_index
                    ],
                "group_2":
                    groups_unique[
                        right_index
                    ],
                "mean_difference":
                    float(
                        result.meandiffs[
                            index
                        ]
                    ),
                "p_value_adjusted":
                    float(
                        result.pvalues[
                            index
                        ]
                    ),
                "ci_lower":
                    lower,
                "ci_upper":
                    upper,
                "reject":
                    bool(
                        result.reject[
                            index
                        ]
                    ),
            }
        )

    return records


class TukeyHSD:
    """
    Comparaisons multiples de Tukey HSD.

    À utiliser après une ANOVA classique significative
    lorsque l'hypothèse d'homogénéité des variances
    est compatible avec les données.
    """

    name = "Tukey HSD"

    def compute(
        self,
        *groups,
        labels=None,
        alpha=0.05,
    ):
        samples, labels = (
            _clean_groups(
                groups,
                labels,
            )
        )

        values, group_labels = (
            _flatten_groups(
                samples,
                labels,
            )
        )

        result = pairwise_tukeyhsd(
            endog=values,
            groups=group_labels,
            alpha=alpha,
            use_var="equal",
        )

        return {
            "method":
                self.name,
            "alpha":
                alpha,
            "number_of_groups":
                len(samples),
            "comparisons":
                _statsmodels_pairwise_records(
                    result
                ),
        }


class GamesHowell:
    """
    Comparaisons multiples de Games-Howell.

    Utilise pairwise_tukeyhsd(use_var='unequal')
    de Statsmodels 0.15+.
    """

    name = "Games-Howell"

    def compute(
        self,
        *groups,
        labels=None,
        alpha=0.05,
    ):
        samples, labels = (
            _clean_groups(
                groups,
                labels,
            )
        )

        values, group_labels = (
            _flatten_groups(
                samples,
                labels,
            )
        )

        result = pairwise_tukeyhsd(
            endog=values,
            groups=group_labels,
            alpha=alpha,
            use_var="unequal",
        )

        return {
            "method":
                self.name,
            "alpha":
                alpha,
            "number_of_groups":
                len(samples),
            "comparisons":
                _statsmodels_pairwise_records(
                    result
                ),
        }


class DunnHolm:
    """
    Test post-hoc de Dunn avec correction de Holm.

    Adapté après un Kruskal-Wallis significatif.
    """

    name = "Dunn-Holm"

    def compute(
        self,
        *groups,
        labels=None,
        alpha=0.05,
    ):
        samples, labels = (
            _clean_groups(
                groups,
                labels,
            )
        )

        values = np.concatenate(
            samples
        )

        ranks = stats.rankdata(
            values,
            method="average",
        )

        n_total = len(values)

        _, tie_counts = np.unique(
            values,
            return_counts=True,
        )

        tie_sum = np.sum(
            tie_counts ** 3
            - tie_counts
        )

        denominator = (
            n_total ** 3
            - n_total
        )

        tie_correction = (
            1.0
            if denominator == 0
            else
            1.0
            - tie_sum
            / denominator
        )

        rank_variance = (
            n_total
            * (
                n_total + 1
            )
            / 12.0
            * tie_correction
        )

        mean_ranks = []

        start = 0

        for group in samples:
            stop = (
                start
                + len(group)
            )

            mean_ranks.append(
                float(
                    np.mean(
                        ranks[
                            start:stop
                        ]
                    )
                )
            )

            start = stop

        pair_indices = list(
            combinations(
                range(
                    len(samples)
                ),
                2,
            )
        )

        raw_p_values = []
        statistics = []

        for left, right in pair_indices:

            standard_error = np.sqrt(
                rank_variance
                * (
                    1.0
                    / len(
                        samples[left]
                    )
                    +
                    1.0
                    / len(
                        samples[right]
                    )
                )
            )

            if standard_error == 0:
                z_value = 0.0
            else:
                z_value = (
                    mean_ranks[left]
                    - mean_ranks[right]
                ) / standard_error

            p_value = (
                2.0
                * stats.norm.sf(
                    abs(z_value)
                )
            )

            statistics.append(
                float(z_value)
            )

            raw_p_values.append(
                float(p_value)
            )

        reject, adjusted, _, _ = (
            multipletests(
                raw_p_values,
                alpha=alpha,
                method="holm",
            )
        )

        comparisons = []

        for index, (
            left,
            right,
        ) in enumerate(
            pair_indices
        ):

            comparisons.append(
                {
                    "group_1":
                        labels[left],
                    "group_2":
                        labels[right],
                    "mean_rank_1":
                        mean_ranks[
                            left
                        ],
                    "mean_rank_2":
                        mean_ranks[
                            right
                        ],
                    "z":
                        statistics[
                            index
                        ],
                    "p_value":
                        raw_p_values[
                            index
                        ],
                    "p_value_adjusted":
                        float(
                            adjusted[
                                index
                            ]
                        ),
                    "reject":
                        bool(
                            reject[
                                index
                            ]
                        ),
                }
            )

        return {
            "method":
                self.name,
            "correction":
                "Holm",
            "alpha":
                alpha,
            "number_of_groups":
                len(samples),
            "tie_correction":
                float(
                    tie_correction
                ),
            "comparisons":
                comparisons,
        }


class AdaptivePostHoc:
    """
    Sélection du post-hoc à partir du résultat
    de GroupTestSelector.

    Aucun post-hoc n'est exécuté si :
    - il n'y a que deux groupes ;
    - le test global n'est pas significatif.
    """

    @staticmethod
    def compute(
        selection,
        *groups,
        labels=None,
    ):
        if not isinstance(
            selection,
            dict,
        ):
            raise TypeError(
                "selection doit être le dictionnaire "
                "renvoyé par GroupTestSelector."
            )

        if len(groups) <= 2:
            return {
                "performed": False,
                "reason":
                    "two_groups_no_posthoc",
                "method": None,
                "comparisons": [],
            }

        result = selection.get(
            "result"
        )

        if result is None:
            raise ValueError(
                "Résultat du test global absent."
            )

        if not result.reject_null:
            return {
                "performed": False,
                "reason":
                    "global_test_not_significant",
                "method": None,
                "comparisons": [],
            }

        selected_test = (
            selection.get(
                "selected_test"
            )
        )

        alpha = float(
            selection.get(
                "alpha",
                0.05,
            )
        )

        if selected_test == "anova":
            output = TukeyHSD().compute(
                *groups,
                labels=labels,
                alpha=alpha,
            )

        elif (
            selected_test
            == "welch_anova"
        ):
            output = GamesHowell().compute(
                *groups,
                labels=labels,
                alpha=alpha,
            )

        elif selected_test == "kruskal":
            output = DunnHolm().compute(
                *groups,
                labels=labels,
                alpha=alpha,
            )

        else:
            return {
                "performed": False,
                "reason":
                    "posthoc_not_applicable",
                "method": None,
                "comparisons": [],
            }

        output[
            "performed"
        ] = True

        output[
            "reason"
        ] = (
            "global_test_significant"
        )

        return output
