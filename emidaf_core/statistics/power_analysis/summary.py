"""
=========================================================
EMIDAF Framework
Power Analysis Summary Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .interpretation import Interpretation

# ==========================================================
# SUMMARY
# ==========================================================

class PowerSummary:

    """
    Central summary engine for
    power analyses.
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

        self.results.append(

            {

                "result":result,

                "interpretation":

                Interpretation.interpret(

                    result

                )

            }

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

    def n_analyses(

        self,

    ):

        return len(

            self.results

        )

    # ==========================================================
# TABLE
# ==========================================================

    def table(

        self,

    ):

        rows=[]

        for item in self.results:

            result=item["result"]

            interpretation=item[

                "interpretation"

            ]

            rows.append(

                {

                    "Test":

                        result.test,

                    "Effect Size":

                        result.effect_size,

                    "Alpha":

                        result.alpha,

                    "Power":

                        result.power,

                    "Sample Size":

                        result.sample_size,

                    "Power Interpretation":

                        interpretation.get(

                            "power"

                        ),

                    "Effect Interpretation":

                        interpretation.get(

                            "effect_size"

                        )

                }

            )

        return pd.DataFrame(

            rows

        )

    # ==========================================================
# RESULTS
# ==========================================================

    def values(

        self,

    ):

        return [

            item["result"]

            for item

            in self.results

        ]

    # ==========================================================
# INTERPRETATIONS
# ==========================================================

    def interpretations(

        self,

    ):

        return [

            item["interpretation"]

            for item

            in self.results

        ]

    # ==========================================================
# BEST POWER
# ==========================================================

    def best_power(

        self,

    ):

        candidates=[

            item["result"]

            for item

            in self.results

            if item["result"].power

            is not None

        ]

        if not candidates:

            return None

        return max(

            candidates,

            key=lambda x:

            x.power

        )

    # ==========================================================
# MIN SAMPLE
# ==========================================================

    def smallest_sample(

        self,

    ):

        candidates=[

            item["result"]

            for item

            in self.results

            if item["result"].sample_size

            is not None

        ]

        if not candidates:

            return None

        return min(

            candidates,

            key=lambda x:

            x.sample_size

        )

    # ==========================================================
# SUMMARY
# ==========================================================

    def summary(

        self,

    ):

        return {

            "number_of_analyses":

                self.n_analyses,

            "best_power":

                self.best_power(),

            "smallest_sample":

                self.smallest_sample(),

            "table":

                self.table()

        }

# ==========================================================
# SERVICE
# ==========================================================

class Summary:

    @staticmethod

    def create():

        return PowerSummary()