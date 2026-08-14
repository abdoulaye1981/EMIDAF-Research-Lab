"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Independence
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .base import BaseHypothesisTest


class ChiSquareIndependenceTest(BaseHypothesisTest):

    name = "Chi-Square Independence Test"

    def test(
        self,
        data,
        row,
        column
    ):

        from scipy.stats import chi2_contingency

        if row not in data.columns:
            raise ValueError(
                f"Variable inconnue : {row}"
            )

        if column not in data.columns:
            raise ValueError(
                f"Variable inconnue : {column}"
            )

        subset = data[
            [row, column]
        ].dropna()

        contingency = pd.crosstab(
            subset[row],
            subset[column]
        )

        if contingency.empty:
            raise ValueError(
                "Le tableau de contingence est vide."
            )

        statistic, p_value, dof, expected = (
            chi2_contingency(
                contingency
            )
        )

        expected_df = pd.DataFrame(
            expected,
            index=contingency.index,
            columns=contingency.columns
        )

        cramers_v = self._cramers_v(
            statistic,
            contingency
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                f"H0 : {row} et {column} "
                "sont indépendantes."
            ),
            alternative_hypothesis=(
                f"H1 : {row} et {column} "
                "ne sont pas indépendantes."
            ),
            details={
                "row": row,
                "column": column,
                "n": int(contingency.to_numpy().sum()),
                "degrees_of_freedom": int(dof),
                "contingency_table": contingency,
                "expected_table": expected_df,
                "cramers_v": float(cramers_v)
            }
        )

    @staticmethod
    def _cramers_v(
        statistic,
        contingency
    ):

        n = contingency.to_numpy().sum()

        rows, columns = contingency.shape

        minimum_dimension = min(
            rows - 1,
            columns - 1
        )

        if minimum_dimension <= 0:
            return 0.0

        return np.sqrt(
            statistic
            / (
                n
                * minimum_dimension
            )
        )


class ChiSquareGoodnessOfFitTest(
    BaseHypothesisTest
):

    name = "Chi-Square Goodness-of-Fit Test"

    def test(
        self,
        observed,
        expected_proportions=None
    ):

        from scipy.stats import chisquare

        observed = np.asarray(
            observed,
            dtype=float
        )

        if observed.ndim != 1:
            raise ValueError(
                "observed doit être un vecteur."
            )

        if np.any(observed < 0):
            raise ValueError(
                "Les effectifs observés doivent être positifs."
            )

        if observed.sum() == 0:
            raise ValueError(
                "La somme des effectifs doit être positive."
            )

        if expected_proportions is None:

            expected = np.repeat(
                observed.sum() / len(observed),
                len(observed)
            )

            proportions = np.repeat(
                1 / len(observed),
                len(observed)
            )

        else:

            proportions = np.asarray(
                expected_proportions,
                dtype=float
            )

            if len(proportions) != len(observed):
                raise ValueError(
                    "Le nombre de proportions attendues "
                    "doit correspondre au nombre de catégories."
                )

            if np.any(proportions < 0):
                raise ValueError(
                    "Les proportions attendues doivent être positives."
                )

            if not np.isclose(
                proportions.sum(),
                1
            ):
                raise ValueError(
                    "Les proportions attendues doivent "
                    "sommmer à 1."
                )

            expected = (
                observed.sum()
                * proportions
            )

        statistic, p_value = chisquare(
            f_obs=observed,
            f_exp=expected
        )

        return self._create_result(
            statistic=float(statistic),
            p_value=float(p_value),
            null_hypothesis=(
                "H0 : les proportions observées "
                "correspondent aux proportions théoriques."
            ),
            alternative_hypothesis=(
                "H1 : les proportions observées "
                "diffèrent des proportions théoriques."
            ),
            details={
                "observed": observed,
                "expected": expected,
                "expected_proportions": proportions,
                "n": int(observed.sum()),
                "degrees_of_freedom":
                    len(observed) - 1
            }
        )


def chi_square_independence_test(
    data,
    row,
    column,
    alpha=0.05
):

    return ChiSquareIndependenceTest(
        alpha=alpha
    ).test(
        data,
        row,
        column
    )


def chi_square_goodness_of_fit_test(
    observed,
    expected_proportions=None,
    alpha=0.05
):

    return ChiSquareGoodnessOfFitTest(
        alpha=alpha
    ).test(
        observed,
        expected_proportions
    )


def cramers_v(
    data,
    row,
    column
):

    result = ChiSquareIndependenceTest(
        alpha=0.05
    ).test(
        data,
        row,
        column
    )

    return result.details[
        "cramers_v"
    ]
