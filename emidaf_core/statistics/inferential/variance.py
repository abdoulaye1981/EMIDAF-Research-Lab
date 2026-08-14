"""
=========================================================
EMIDAF Framework
Variance Equality Tests
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
# FISHER F
# ==========================================================

class FisherVarianceTest(

    BaseInferentialTest

):

    name="Fisher Variance Test"

    def compute(

        self,

        x,

        y,

        alpha=0.05,

    ):

        var1=np.var(

            x,

            ddof=1

        )

        var2=np.var(

            y,

            ddof=1

        )

        statistic=var1/var2

        df1=len(x)-1

        df2=len(y)-1

        p=2*min(

            stats.f.cdf(

                statistic,

                df1,

                df2

            ),

            1-stats.f.cdf(

                statistic,

                df1,

                df2

            )

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# LEVENE
# ==========================================================

class LeveneTest(

    BaseInferentialTest

):

    name="Levene Test"

    def compute(

        self,

        *groups,

        alpha=0.05,

        center="median",

    ):

        statistic,p=stats.levene(

            *groups,

            center=center

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# BARTLETT
# ==========================================================

class BartlettTest(

    BaseInferentialTest

):

    name="Bartlett Test"

    def compute(

        self,

        *groups,

        alpha=0.05,

    ):

        statistic,p=stats.bartlett(

            *groups

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# FLIGNER
# ==========================================================

class FlignerKilleenTest(

    BaseInferentialTest

):

    name="Fligner-Killeen"

    def compute(

        self,

        *groups,

        alpha=0.05,

    ):

        statistic,p=stats.fligner(

            *groups

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# BROWN-FORSYTHE
# ==========================================================

class BrownForsytheTest(

    BaseInferentialTest

):

    name="Brown-Forsythe"

    def compute(

        self,

        *groups,

        alpha=0.05,

    ):

        statistic,p=stats.levene(

            *groups,

            center="median"

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# HARTLEY FMAX
# ==========================================================

class HartleyFMaxTest(

    BaseInferentialTest

):

    name="Hartley Fmax"

    def compute(

        self,

        *groups,

    ):

        variances=[

            np.var(

                g,

                ddof=1

            )

            for g in groups

        ]

        statistic=max(

            variances

        )/min(

            variances

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            metadata={

                "critical_value":

                    "À calculer"

            }

        )

# ==========================================================
# COCHRAN C
# ==========================================================

class CochranCTest(

    BaseInferentialTest

):

    name="Cochran C"

    def compute(

        self,

        *groups,

    ):

        variances=np.array([

            np.var(

                g,

                ddof=1

            )

            for g in groups

        ])

        statistic=np.max(

            variances

        )/np.sum(

            variances

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic)

        )

# ==========================================================
# O'BRIEN
# ==========================================================

class OBrienTest(

    BaseInferentialTest

):

    name="O'Brien"

    def compute(

        self,

        *groups,

    ):

        raise NotImplementedError(

            "À implémenter."

        )

# ==========================================================
# BOX M
# ==========================================================

class BoxMTest(

    BaseInferentialTest

):

    name="Box M"

    def compute(

        self,

        *groups,

    ):

        raise NotImplementedError(

            "À implémenter dans MANOVA."

        )

# ==========================================================
# SERVICE
# ==========================================================

# ==========================================================
# SERVICE
# ==========================================================

class VarianceTests:

    registry = {

        "fisher":
            FisherVarianceTest,

        "levene":
            LeveneTest,

        "bartlett":
            BartlettTest,

        "brown_forsythe":
            BrownForsytheTest,

        "fligner":
            FlignerKilleenTest,

        "hartley":
            HartleyFMaxTest,

        "cochran":
            CochranCTest,

        "obrien":
            OBrienTest,

        "box_m":
            BoxMTest

    }

    @classmethod
    def compute(
        cls,
        method,
        *args,
        **kwargs
    ):

        model = cls.registry[method]()

        return model.compute(
            *args,
            **kwargs
        )

