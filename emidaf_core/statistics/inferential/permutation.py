"""
=========================================================
EMIDAF Framework
Permutation Test Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    InferentialResult

)

# ==========================================================
# ENGINE
# ==========================================================

class PermutationEngine:

    """
    Generic permutation engine.
    """

    def __init__(

        self,

        statistic,

        n_permutations=10000,

        random_state=None,

    ):

        self.statistic=statistic

        self.n_permutations=n_permutations

        self.random_state=random_state

        self.rng=np.random.default_rng(

            random_state

        )

    # ==========================================================
# DISTRIBUTION
# ==========================================================

    def permutation_distribution(

        self,

        x,

        y,

    ):

        observed=self.statistic(

            x,

            y

        )

        pooled=np.concatenate(

            [

                x,

                y

            ]

        )

        nx=len(x)

        estimates=[]

        for _ in range(

            self.n_permutations

        ):

            self.rng.shuffle(

                pooled

            )

            x_perm=pooled[:nx]

            y_perm=pooled[nx:]

            estimates.append(

                self.statistic(

                    x_perm,

                    y_perm

                )

            )

        return observed,np.asarray(

            estimates

        )

    # ==========================================================
# COMPUTE
# ==========================================================

    def compute(

        self,

        x,

        y,

    ):

        observed,distribution=(

            self.permutation_distribution(

                x,

                y

            )

        )

        p=np.mean(

            np.abs(

                distribution

            )

            >=

            abs(

                observed

            )

        )

        return InferentialResult(

            test="Permutation Test",

            statistic=float(

                observed

            ),

            p_value=float(

                p

            ),

            metadata={

                "distribution":

                    distribution,

                "permutations":

                    self.n_permutations

            }

        )
# ==========================================================
# MEAN DIFFERENCE
# ==========================================================

class MeanDifferencePermutation:

    """
    Permutation test
    for mean difference.
    """

    def __init__(

        self,

        n_permutations=10000,

        random_state=None,

    ):

        self.engine=PermutationEngine(

            statistic=lambda a,b:

                np.mean(a)-np.mean(b),

            n_permutations=n_permutations,

            random_state=random_state

        )

    def compute(

        self,

        x,

        y,

    ):

        return self.engine.compute(

            x,

            y

        )
    
# ==========================================================
# MEDIAN DIFFERENCE
# ==========================================================

class MedianDifferencePermutation:

    def __init__(

        self,

        n_permutations=10000,

        random_state=None,

    ):

        self.engine=PermutationEngine(

            statistic=lambda a,b:

                np.median(a)-np.median(b),

            n_permutations=n_permutations,

            random_state=random_state

        )

    def compute(

        self,

        x,

        y,

    ):

        return self.engine.compute(

            x,

            y

        )
    
# ==========================================================
# CORRELATION
# ==========================================================

class CorrelationPermutation:

    def __init__(

        self,

        n_permutations=10000,

        random_state=None,

    ):

        self.n_permutations=n_permutations

        self.random_state=random_state

        self.rng=np.random.default_rng(

            random_state

        )

    def compute(

        self,

        x,

        y,

    ):

        observed=np.corrcoef(

            x,

            y

        )[0,1]

        estimates=[]

        for _ in range(

            self.n_permutations

        ):

            yp=self.rng.permutation(

                y

            )

            estimates.append(

                np.corrcoef(

                    x,

                    yp

                )[0,1]

            )

        estimates=np.asarray(

            estimates

        )

        p=np.mean(

            np.abs(

                estimates

            )

            >=

            abs(

                observed

            )

        )

        return InferentialResult(

            test="Permutation Correlation",

            statistic=float(

                observed

            ),

            p_value=float(

                p

            ),

            metadata={

                "distribution":

                    estimates

            }

        )

# ==========================================================
# SERVICE
# ==========================================================

class Permutation:

    Engine = PermutationEngine

    MeanDifference = MeanDifferencePermutation

    MedianDifference = MedianDifferencePermutation

    Correlation = CorrelationPermutation

    registry = {
        "mean": MeanDifferencePermutation,
        "median": MedianDifferencePermutation,
        "correlation": CorrelationPermutation,
    }

    @classmethod
    def compute(cls, method, **kwargs):

        model = cls.registry[method]()

        return model.compute(**kwargs)
