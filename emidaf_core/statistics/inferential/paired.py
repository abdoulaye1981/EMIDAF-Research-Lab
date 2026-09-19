"""
=========================================================
EMIDAF Framework
Paired Samples Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    BaseInferentialTest,

    InferentialResult

)

# ==========================================================
# PAIRED STUDENT
# ==========================================================

class PairedStudentTTest(

    BaseInferentialTest

):

    name="Paired Student"

    def compute(

        self,

        before,

        after,

        alpha=0.05,

    ):

        statistic,p=stats.ttest_rel(

            before,

            after,

            nan_policy="omit"

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# WILCOXON
# ==========================================================

class WilcoxonSignedRankTest(

    BaseInferentialTest

):

    name="Wilcoxon Signed Rank"

    def compute(

        self,

        before,

        after,

        alpha=0.05,

        alternative="two-sided",

    ):

        statistic,p=stats.wilcoxon(

            before,

            after,

            alternative=alternative

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# SIGN TEST
# ==========================================================

class PairedSignTest(

    BaseInferentialTest

):

    name="Paired Sign Test"

    def compute(

        self,

        before,

        after,

        alpha=0.05,

    ):

        diff=np.asarray(after)-np.asarray(before)

        positive=np.sum(diff>0)

        negative=np.sum(diff<0)

        n=positive+negative

        result=stats.binomtest(

            positive,

            n,

            p=0.5

        )

        return InferentialResult(

            test=self.name,

            statistic=float(positive),

            p_value=float(result.pvalue),

            alpha=alpha,

            reject_null=result.pvalue<alpha

        )

# ==========================================================
# PAIRED PERMUTATION
# ==========================================================

class PairedPermutationTest(

    BaseInferentialTest

):

    name="Paired Permutation"

    def compute(
        self,
        before,
        after,
        alpha=0.05,
        n_resamples=10000,
        random_state=None,
    ):
        """
        Paired permutation test based on random
        sign flips of within-pair differences.
        """

        before = np.asarray(
            before,
            dtype=float,
        )

        after = np.asarray(
            after,
            dtype=float,
        )

        if before.shape != after.shape:
            raise ValueError(
                "before and after must have "
                "the same shape."
            )

        mask = (
            np.isfinite(before)
            & np.isfinite(after)
        )

        before = before[mask]
        after = after[mask]

        if before.size < 2:
            raise ValueError(
                "At least two valid paired "
                "observations are required."
            )

        if (
            not isinstance(n_resamples, int)
            or n_resamples <= 0
        ):
            raise ValueError(
                "n_resamples must be a positive integer."
            )

        differences = (
            after - before
        )

        observed = float(
            np.mean(differences)
        )

        rng = np.random.default_rng(
            random_state
        )

        extreme = 0

        for _ in range(
            n_resamples
        ):
            signs = rng.choice(
                (-1.0, 1.0),
                size=differences.size,
            )

            permuted = float(
                np.mean(
                    differences * signs
                )
            )

            if (
                abs(permuted)
                >= abs(observed)
            ):
                extreme += 1

        p_value = (
            extreme + 1
        ) / (
            n_resamples + 1
        )

        return InferentialResult(
            test=self.name,
            statistic=observed,
            p_value=float(p_value),
            alpha=alpha,
            reject_null=(
                p_value < alpha
            ),
            metadata={
                "n_resamples":
                    n_resamples,
                "n_pairs":
                    int(differences.size),
                "random_state":
                    random_state,
                "statistic":
                    "mean paired difference",
                "permutation_scheme":
                    "sign flip",
            },
        )

# ==========================================================
# PAIRED PERMUTATION
# ==========================================================

# ==========================================================
# SERVICE
# ==========================================================

class Paired:

    registry={

        "student":

            PairedStudentTTest,

        "wilcoxon":

            WilcoxonSignedRankTest,

        "sign":

            PairedSignTest,

        "permutation":

            PairedPermutationTest

    }

    @classmethod

    def compute(

        cls,

        method,

        **kwargs,

    ):

        model=cls.registry[method]()

        return model.compute(

            **kwargs

        )