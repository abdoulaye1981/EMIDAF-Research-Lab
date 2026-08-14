"""
=========================================================
EMIDAF Framework
Effect Size Summary Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from .interpretation import Interpretation

# ==========================================================
# SUMMARY
# ==========================================================

class EffectSizeSummary:

    """
    Central effect size summary engine.
    """

    def __init__(

        self,

    ):

        self.results=[]

    # ==========================================================
# ADD
# ==========================================================

    def add(

        self,

        result,

    ):

        result=Interpretation.interpret(

            result

        )

        self.results.append(

            result

        )

        return self

    # ==========================================================
# EXTEND
# ==========================================================

    def extend(

        self,

        results,

    ):

        for result in results:

            self.add(

                result

            )

        return self

    # ==========================================================
# COUNT
# ==========================================================

    @property

    def n_effects(

        self,

    ):

        return len(

            self.results

        )

    # ==========================================================
# RESULTS
# ==========================================================

    def values(

        self,

    ):

        return [

            result.statistic

            for result

            in self.results

        ]

    # ==========================================================
# MAGNITUDES
# ==========================================================

    def magnitudes(

        self,

    ):

        return [

            result.magnitude

            for result

            in self.results

        ]
    # ==========================================================
# NAMES
# ==========================================================

    def names(

        self,

    ):

        return [

            result.name

            for result

            in self.results

        ]

    # ==========================================================
# TABLE
# ==========================================================

    def table(

        self,

    ):

        import pandas as pd

        rows=[]

        for result in self.results:

            rows.append(

                {

                    "Effect Size":

                        result.name,

                    "Value":

                        result.statistic,

                    "Magnitude":

                        result.magnitude,

                    "Interpretation":

                        result.interpretation

                }

            )

        return pd.DataFrame(

            rows

        )
    # ==========================================================
# LARGEST
# ==========================================================

    def largest(

        self,

    ):

        return max(

            self.results,

            key=lambda x:

            abs(

                x.statistic

            )

        )
    # ==========================================================
# SMALLEST
# ==========================================================

    def smallest(

        self,

    ):

        return min(

            self.results,

            key=lambda x:

            abs(

                x.statistic

            )

        )
    # ==========================================================
# SUMMARY
# ==========================================================

    def summary(

        self,

    ):

        return {

            "n_effect_sizes":

                self.n_effects,

            "largest":

                self.largest(),

            "smallest":

                self.smallest(),

            "table":

                self.table()

        }

# ==========================================================
# SERVICE
# ==========================================================

class Summary:

    @staticmethod

    def create():

        return EffectSizeSummary()