"""
=========================================================
EMIDAF Framework
Superiority Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from statsmodels.stats.proportion import (

    proportions_ztest

)

from .base import (

    BaseInferentialTest,

    InferentialResult

)

# ==========================================================
# SUPERIORITY T TEST
# ==========================================================

class SuperiorityTTest(

    BaseInferentialTest

):

    name="Superiority T Test"

    def compute(

        self,

        treatment,

        control,

        margin=0,

        alpha=0.05,

    ):

        treatment=np.asarray(treatment)

        control=np.asarray(control)

        diff=np.mean(treatment)-np.mean(control)

        nt=len(treatment)

        nc=len(control)

        vt=np.var(

            treatment,

            ddof=1

        )

        vc=np.var(

            control,

            ddof=1

        )

        se=np.sqrt(

            vt/nt+

            vc/nc

        )

        statistic=(

            diff-margin

        )/se

        df=nt+nc-2

        p=1-stats.t.cdf(

            statistic,

            df

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha,

            metadata={

                "difference":

                    diff,

                "margin":

                    margin

            }

        )

# ==========================================================
# WELCH
# ==========================================================

class WelchSuperiority(

    BaseInferentialTest

):

    name="Welch Superiority"

    def compute(

        self,

        treatment,

        control,

        margin=0,

        alpha=0.05,

    ):

        treatment=np.asarray(treatment)

        control=np.asarray(control)

        diff=np.mean(treatment)-np.mean(control)

        nt=len(treatment)

        nc=len(control)

        vt=np.var(treatment,ddof=1)

        vc=np.var(control,ddof=1)

        se=np.sqrt(

            vt/nt+

            vc/nc

        )

        statistic=(

            diff-margin

        )/se

        numerator=(

            vt/nt+

            vc/nc

        )**2

        denominator=(

            (vt/nt)**2/(nt-1)

            +

            (vc/nc)**2/(nc-1)

        )

        df=numerator/denominator

        p=1-stats.t.cdf(

            statistic,

            df

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# PROPORTIONS
# ==========================================================

class SuperiorityProportion(

    BaseInferentialTest

):

    name="Superiority Proportion"

    def compute(

        self,

        successes,

        observations,

        margin=0,

        alpha=0.05,

    ):

        statistic,p=proportions_ztest(

            successes,

            observations,

            value=margin

        )

        p=p/2

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=(

                statistic>0

                and

                p<alpha

            )

        )



# ==========================================================
# SERVICE
# ==========================================================

class Superiority:

    registry={

        "student":
            SuperiorityTTest,

        "welch":
            WelchSuperiority,

        "proportion":
            SuperiorityProportion

    }

    @classmethod
    def compute(
        cls,
        method,
        **kwargs,
    ):

        model = cls.registry[method]()

        return model.compute(
            **kwargs
        )
