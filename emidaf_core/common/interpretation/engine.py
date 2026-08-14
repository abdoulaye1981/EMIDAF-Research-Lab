from .base import ScientificInterpretation

from .rules import MEAN_RULES


class InterpretationEngine:

    @staticmethod

    def mean(

        result,

    ):

        rule=MEAN_RULES["default"]

        return ScientificInterpretation(

            title="Arithmetic Mean",

            statistic="Mean",

            value=result,

            interpretation=

                rule["interpretation"],

            recommendation=

                rule["recommendation"],

            suggested_plots=

                rule["plots"]

        )