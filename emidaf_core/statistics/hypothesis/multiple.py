"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Multiple Comparisons
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .result import HypothesisResult


class MultipleTesting:

    METHODS = [
        "bonferroni",
        "holm",
        "fdr_bh",
        "fdr_by",
        "sidak"
    ]

    def __init__(
        self,
        alpha=0.05
    ):

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha doit être compris entre 0 et 1."
            )

        self.alpha = alpha
        self.results = None

    def adjust(
        self,
        p_values,
        method="holm"
    ):

        from statsmodels.stats.multitest import (
            multipletests
        )

        if method not in self.METHODS:
            raise ValueError(
                f"Méthode inconnue : {method}. "
                f"Choisir parmi {self.METHODS}."
            )

        p_values = np.asarray(
            p_values,
            dtype=float
        )

        if p_values.ndim != 1:
            raise ValueError(
                "p_values doit être un vecteur."
            )

        if len(p_values) == 0:
            raise ValueError(
                "p_values ne peut pas être vide."
            )

        if np.any(
            (p_values < 0)
            | (p_values > 1)
        ):
            raise ValueError(
                "Les p-values doivent être comprises "
                "entre 0 et 1."
            )

        reject, p_adjusted, _, _ = (
            multipletests(
                p_values,
                alpha=self.alpha,
                method=method
            )
        )

        self.results = pd.DataFrame({
            "p_value": p_values,
            "p_value_adjusted": p_adjusted,
            "reject_null": reject,
            "significant": reject
        })

        return self.results

    def summary(self):

        if self.results is None:
            return None

        return self.results.copy()

    def to_dict(self):

        if self.results is None:
            return None

        return self.results.to_dict(
            orient="records"
        )


def adjust_pvalues(
    p_values,
    method="holm",
    alpha=0.05
):

    tester = MultipleTesting(
        alpha=alpha
    )

    return tester.adjust(
        p_values,
        method=method
    )


def bonferroni_correction(
    p_values,
    alpha=0.05
):

    return adjust_pvalues(
        p_values,
        method="bonferroni",
        alpha=alpha
    )


def holm_correction(
    p_values,
    alpha=0.05
):

    return adjust_pvalues(
        p_values,
        method="holm",
        alpha=alpha
    )


def fdr_bh_correction(
    p_values,
    alpha=0.05
):

    return adjust_pvalues(
        p_values,
        method="fdr_bh",
        alpha=alpha
    )


def fdr_by_correction(
    p_values,
    alpha=0.05
):

    return adjust_pvalues(
        p_values,
        method="fdr_by",
        alpha=alpha
    )


def sidak_correction(
    p_values,
    alpha=0.05
):

    return adjust_pvalues(
        p_values,
        method="sidak",
        alpha=alpha
    )


def compare_methods(
    p_values,
    alpha=0.05
):

    p_values = np.asarray(
        p_values,
        dtype=float
    )

    output = pd.DataFrame({
        "p_value": p_values
    })

    for method in MultipleTesting.METHODS:

        result = adjust_pvalues(
            p_values,
            method=method,
            alpha=alpha
        )

        output[
            f"{method}_adjusted"
        ] = result[
            "p_value_adjusted"
        ]

        output[
            f"{method}_reject"
        ] = result[
            "reject_null"
        ]

    return output
