"""
=========================================================
EMIDAF Framework
Proportion Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from statsmodels.stats.proportion import (

    proportions_ztest,

    proportion_confint,

    proportions_chisquare

)

from .base import (

    BaseInferentialTest,

    InferentialResult

)

# ==========================================================
# ONE PROPORTION Z TEST
# ==========================================================

class OneProportionZTest(

    BaseInferentialTest

):

    name="One Proportion Z Test"

    def compute(

        self,

        successes,

        n,

        p0,

        alpha=0.05,

    ):

        statistic,p=proportions_ztest(

            successes,

            n,

            value=p0

        )

        ci=proportion_confint(

            successes,

            n,

            alpha=alpha,

            method="wilson"

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha,

            confidence_interval=ci

        )

# ==========================================================
# TWO PROPORTIONS
# ==========================================================

class TwoProportionZTest(

    BaseInferentialTest

):

    name="Two Proportion Z Test"

    def compute(

        self,

        successes,

        observations,

        alpha=0.05,

    ):

        statistic,p=proportions_ztest(

            successes,

            observations

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# BINOMIAL EXACT
# ==========================================================

class ExactBinomialTest(

    BaseInferentialTest

):

    name="Exact Binomial Test"

    def compute(

        self,

        successes,

        n,

        p0=0.5,

        alpha=0.05,

    ):

        result=stats.binomtest(

            successes,

            n,

            p0

        )

        return InferentialResult(

            test=self.name,

            statistic=float(successes),

            p_value=float(result.pvalue),

            alpha=alpha,

            reject_null=result.pvalue<alpha,

            confidence_interval=result.proportion_ci()

        )

# ==========================================================
# FISHER EXACT
# ==========================================================

class FisherExactTest(

    BaseInferentialTest

):

    name="Fisher Exact Test"

    def compute(

        self,

        table,

        alpha=0.05,

    ):

        odds,p=stats.fisher_exact(

            table

        )

        return InferentialResult(

            test=self.name,

            statistic=float(odds),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )

# ==========================================================
# MCNEMAR
# ==========================================================

from statsmodels.stats.contingency_tables import (

    mcnemar

)

class McNemarTest(

    BaseInferentialTest

):

    name="McNemar Test"

    def compute(

        self,

        table,

        alpha=0.05,

        exact=True,

    ):

        result=mcnemar(

            table,

            exact=exact

        )

        return InferentialResult(

            test=self.name,

            statistic=float(result.statistic),

            p_value=float(result.pvalue),

            alpha=alpha,

            reject_null=result.pvalue<alpha

        )

# ==========================================================
# COCHRAN Q
# ==========================================================

from statsmodels.stats.contingency_tables import (

    cochrans_q

)

class CochranQTest(

    BaseInferentialTest

):

    name="Cochran Q"

    def compute(

        self,

        data,

        alpha=0.05,

    ):

        result=cochrans_q(

            data

        )

        return InferentialResult(

            test=self.name,

            statistic=float(result.statistic),

            p_value=float(result.pvalue),

            alpha=alpha,

            reject_null=result.pvalue<alpha

        )

# ==========================================================
# CHI² PROPORTIONS
# ==========================================================

class ProportionChiSquare(

    BaseInferentialTest

):

    name="Chi² Proportions"

    def compute(

        self,

        counts,

        nobs,

        alpha=0.05,

    ):

        statistic,p,_=proportions_chisquare(

            counts,

            nobs

        )

        return InferentialResult(

            test=self.name,

            statistic=float(statistic),

            p_value=float(p),

            alpha=alpha,

            reject_null=p<alpha

        )
    
# ==========================================================
# SERVICE
# ==========================================================

class Proportions:

    registry={

        "one":

            OneProportionZTest,

        "two":

            TwoProportionZTest,

        "binomial":

            ExactBinomialTest,

        "fisher":

            FisherExactTest,

        "mcnemar":

            McNemarTest,

        "cochran_q":

            CochranQTest,

        "chisquare":

            ProportionChiSquare

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