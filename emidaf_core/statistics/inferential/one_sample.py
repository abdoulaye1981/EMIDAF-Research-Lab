"""
=========================================================
One Sample Tests
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    BaseInferentialTest,

    InferentialResult

)

class OneSampleTTest(

    BaseInferentialTest

):

    name="One Sample Student"

    def compute(

        self,

        x,

        mu,

        alpha=0.05,

    ):

        statistic,p=stats.ttest_1samp(

            x,

            mu

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=

                p<alpha

        )

class OneSampleWilcoxon(

    BaseInferentialTest

):

    name="Wilcoxon Signed Rank"

    def compute(

        self,

        x,

        mu=0,

        alpha=0.05,

    ):

        statistic,p=stats.wilcoxon(

            x-mu

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=

                p<alpha

        )
    
class OneSampleSignTest(

    BaseInferentialTest

):

    name="Sign Test"

    def compute(

        self,

        x,

        median,

        alpha=0.05,

    ):

        positive=np.sum(

            x>median

        )

        n=len(x)

        p=stats.binomtest(

            positive,

            n,

            0.5

        ).pvalue

        return InferentialResult(

            test=self.name,

            statistic=float(

                positive

            ),

            p_value=float(p),

            alpha=alpha,

            reject_null=

                p<alpha

        )

class OneSample:

    registry={

        "student":

            OneSampleTTest,

        "wilcoxon":

            OneSampleWilcoxon,

        "sign":

            OneSampleSignTest

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