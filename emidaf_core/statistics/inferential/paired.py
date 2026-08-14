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

    ):

        raise NotImplementedError(

            "À implémenter dans bootstrap.py"

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

    ):

        raise NotImplementedError(

            "À implémenter dans bootstrap.py"

        )
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