"""
=========================================================
EMIDAF Framework
Inferential Summary Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from .one_sample import OneSample
from .two_samples import TwoSamples
from .paired import Paired
from .proportions import Proportions
from .variance import VarianceTests
from .confidence import Confidence
from .estimation import Estimator
from .bootstrap import Bootstrap
from .permutation import Permutation

# ==========================================================
# SUMMARY ENGINE
# ==========================================================

class InferentialSummary:

    """
    Automatic inferential analysis.
    """

    def __init__(

        self,

        dataframe,

    ):

        self.df=dataframe.copy()

    
    # ==========================================================
# VARIABLE TYPES
# ==========================================================

    def variable_type(

        self,

        variable,

    ):

        if pd.api.types.is_numeric_dtype(

            self.df[variable]

        ):

            return "numeric"

        return "categorical"
    
    # ==========================================================
# GROUPS
# ==========================================================

    def number_of_groups(

        self,

        group,

    ):

        return self.df[group].nunique()

    # ==========================================================
# TWO GROUPS
# ==========================================================

    def two_groups(

        self,

        target,

        group,

    ):

        groups=[]

        for g in self.df[group].unique():

            groups.append(

                self.df.loc[
                    self.df[group]==g,
                    target
                ].dropna()

            )

        return groups


    # ==========================================================
# AUTO TEST
# ==========================================================

    def automatic_test(

        self,

        target,

        group,

    ):

        groups=self.two_groups(

            target,

            group

        )

        levene=VarianceTests.compute(

            method="levene",

            *groups

        )

        if levene.reject_null:

            result=TwoSamples.compute(

                method="welch",

                x=groups[0],

                y=groups[1]

            )

        else:

            result=TwoSamples.compute(

                method="student",

                x=groups[0],

                y=groups[1]

            )

        return {

            "variance_test":

                levene,

            "inferential":

                result

        }

    # ==========================================================
# CONFIDENCE
# ==========================================================

    def confidence(

        self,

        variable,

    ):

        return Confidence.mean(

            self.df[variable]

        )
    
    # ==========================================================
# BOOTSTRAP
# ==========================================================

    def bootstrap(

        self,

        variable,

    ):

        engine=Bootstrap.Engine()

        return engine.compute(

            self.df[variable]

        )
    
    # ==========================================================
# ESTIMATION
# ==========================================================

    def estimation(

        self,

        variable,

    ):

        return Estimator.mean(

            self.df[variable]

        )
    
    # ==========================================================
# COMPLETE SUMMARY
# ==========================================================

    def summary(

        self,

        target,

        group,

    ):

        return {

            "automatic_test":

                self.automatic_test(

                    target,

                    group

                ),

            "confidence":

                self.confidence(

                    target

                ),

            "bootstrap":

                self.bootstrap(

                    target

                ),

            "estimation":

                self.estimation(

                    target

                )

        }

# ==========================================================
# SERVICE
# ==========================================================

class Inferential:

    @staticmethod

    def analyze(

        dataframe,

        target,

        group,

    ):

        engine=InferentialSummary(

            dataframe

        )

        return engine.summary(

            target,

            group

        )