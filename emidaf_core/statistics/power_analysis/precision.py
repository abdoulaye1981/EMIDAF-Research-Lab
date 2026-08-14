"""
=========================================================
EMIDAF Framework
Precision Based Sample Size Analysis
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import math

from scipy.stats import norm
from scipy.stats import t

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# PRECISION ANALYSIS
# ==========================================================

class PrecisionAnalysis(

    BasePowerAnalysis

):

    """
    Precision-based sample size analysis.
    """

    name="Precision Analysis"

    # ==========================================================
# MEAN
# ==========================================================

    @staticmethod

    def mean(

        standard_deviation,

        margin_error,

        confidence=0.95,

    ):

        z=norm.ppf(

            1-(1-confidence)/2

        )

        n=(

            (

                z*

                standard_deviation

            )

            /

            margin_error

        )**2

        return PowerResult(

            test="Mean Precision",

            sample_size=math.ceil(n),

            metadata={

                "confidence":confidence,

                "margin_error":margin_error

            }

        )

    # ==========================================================
# PROPORTION
# ==========================================================

    @staticmethod
    def proportion(
        proportion,
        margin_error,
        confidence=0.95,
    ):

        z = norm.ppf(
            1 - (1 - confidence) / 2
        )

        n = (
            z**2
            * proportion
            * (1 - proportion)
            / margin_error**2
        )

        return PowerResult(
            test="Proportion Precision",
            sample_size=math.ceil(n),
            metadata={
                "confidence": confidence,
                "margin_error": margin_error
            }
        )

      
    # ==========================================================
# CORRELATION
# ==========================================================

    @staticmethod

    def correlation(

        correlation,

        width,

        confidence=0.95,

    ):

        z=norm.ppf(

            1-(1-confidence)/2

        )

        n=3+(

            4*

            (

                z/width

            )**2

        )

        return PowerResult(

            test="Correlation Precision",

            effect_size=correlation,

            sample_size=math.ceil(n),

            metadata={

                "confidence":confidence,

                "width":width

            }

        )

    # ==========================================================
# VARIANCE
# ==========================================================

    @staticmethod

    def variance(

        coefficient_variation,

        relative_error,

    ):

        n=(

            2/

            (

                relative_error**2

            )

        )*(

            coefficient_variation**2

        )

        return PowerResult(

            test="Variance Precision",

            sample_size=math.ceil(n)

        )

    # ==========================================================
# CONFIDENCE INTERVAL WIDTH
# ==========================================================

    @staticmethod

    def confidence_interval_width(

        sample_size,

        standard_deviation,

        confidence=0.95,

    ):

        z=norm.ppf(

            1-(1-confidence)/2

        )

        width=2*(

            z*

            standard_deviation/

            math.sqrt(

                sample_size

            )

        )

        return float(width)

    # ==========================================================
# MARGIN OF ERROR
# ==========================================================

    @staticmethod

    def margin_of_error(

        sample_size,

        standard_deviation,

        confidence=0.95,

    ):

        z=norm.ppf(

            1-(1-confidence)/2

        )

        margin=(

            z*

            standard_deviation/

            math.sqrt(

                sample_size

            )

        )

        return float(margin)

    # ==========================================================
# SOLVER
# ==========================================================

    @staticmethod

    def solve(

        method,

        **kwargs,

    ):

        methods={

            "mean":

                PrecisionAnalysis.mean,

            "proportion":

                PrecisionAnalysis.proportion,

            "correlation":

                PrecisionAnalysis.correlation,

            "variance":

                PrecisionAnalysis.variance

        }

        return methods[

            method

        ](

            **kwargs

        )
# ==========================================================
# SERVICE
# ==========================================================

class Precision:

    mean=PrecisionAnalysis.mean

    proportion=PrecisionAnalysis.proportion

    correlation=PrecisionAnalysis.correlation

    variance=PrecisionAnalysis.variance

    confidence_interval_width=(

        PrecisionAnalysis.confidence_interval_width

    )

    margin_of_error=(

        PrecisionAnalysis.margin_of_error

    )

    solve=PrecisionAnalysis.solve
