"""
=========================================================
EMIDAF Framework
Non-Inferiority Tests
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
# NON INFERIORITY T TEST
# ==========================================================

class NonInferiorityTTest(

    BaseInferentialTest

):

    name="Non Inferiority T Test"

    def compute(

        self,

        treatment,

        control,

        margin,

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

            diff+margin

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
# WELCH NON INFERIORITY
# ==========================================================

class WelchNonInferiority(

    BaseInferentialTest

):

    name="Welch Non Inferiority"

    def compute(

        self,

        treatment,

        control,

        margin,

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

            diff+margin

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
# PROPORTION
# ==========================================================

from statsmodels.stats.proportion import (

    proportions_ztest

)

class NonInferiorityProportion(

    BaseInferentialTest

):

    name="Non Inferiority Proportion"

    def compute(

        self,

        successes,

        observations,

        margin,

        alpha=0.05,

    ):

        statistic,p=proportions_ztest(

            successes,

            observations,

            value=-margin

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# BOOTSTRAP
# ==========================================================

class BootstrapNonInferiority(

    BaseInferentialTest

):

    name="Bootstrap Non Inferiority"

    def compute(

        self,

        treatment,

        control,

        margin,

        n_bootstrap=5000,

    ):

        treatment=np.asarray(treatment)

        control=np.asarray(control)

        estimates=[]

        nt=len(treatment)

        nc=len(control)

        for _ in range(

            n_bootstrap

        ):

            t=np.random.choice(

                treatment,

                nt,

                replace=True

            )

            c=np.random.choice(

                control,

                nc,

                replace=True

            )

            estimates.append(

                np.mean(t)-np.mean(c)

            )

        lower=np.percentile(

            estimates,

            2.5

        )

        reject=lower>-margin

        return InferentialResult(

            test=self.name,

            statistic=float(

                np.mean(estimates)

            ),

            reject_null=reject,

            metadata={

                "bootstrap_ci":(

                    float(lower),

                    float(

                        np.percentile(

                            estimates,

                            97.5

                        )

                    )

                )

            }

        )

# ==========================================================
# SERVICE
# ==========================================================

class NonInferiority:

    registry={

        "student":

            NonInferiorityTTest,

        "welch":

            WelchNonInferiority,

        "proportion":

            NonInferiorityProportion,

        "bootstrap":

            BootstrapNonInferiority

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