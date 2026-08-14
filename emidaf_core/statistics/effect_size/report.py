"""
=========================================================
EMIDAF Framework
Effect Size Report Generator
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import json

import pandas as pd

from .summary import Summary

# ==========================================================
# REPORT
# ==========================================================

class EffectSizeReport:

    """
    Report generator for effect sizes.
    """

    def __init__(

        self,

        summary,

    ):

        self.summary=summary

    # ==========================================================
# TO DICT
# ==========================================================

    def to_dict(

        self,

    ):

        table=self.summary.table()

        return {

            "number_of_effect_sizes":

                self.summary.n_effects,

            "largest":

                {

                    "name":

                        self.summary.largest().name,

                    "value":

                        self.summary.largest().statistic,

                    "magnitude":

                        self.summary.largest().magnitude

                },

            "smallest":

                {

                    "name":

                        self.summary.smallest().name,

                    "value":

                        self.summary.smallest().statistic,

                    "magnitude":

                        self.summary.smallest().magnitude

                },

            "results":

                table.to_dict(

                    orient="records"

                )

        }
    # ==========================================================
# JSON
# ==========================================================

    def to_json(

        self,

        indent=4,

    ):

        return json.dumps(

            self.to_dict(),

            indent=indent,

            default=str

        )

    # ==========================================================
# DATAFRAME
# ==========================================================

    def to_dataframe(

        self,

    ):

        return self.summary.table()

    # ==========================================================
# MARKDOWN
# ==========================================================

    def to_markdown(

        self,

    ):

        table=self.summary.table()

        return table.to_markdown(

            index=False

        )

    # ==========================================================
# HTML
# ==========================================================

    def to_html(

        self,

    ):

        return self.summary.table().to_html(

            index=False

        )

    # ==========================================================
# LATEX
# ==========================================================

    def to_latex(

        self,

    ):

        return self.summary.table().to_latex(

            index=False

        )
    # ==========================================================
# TEXT
# ==========================================================

    def to_text(

        self,

    ):

        lines=[]

        lines.append(

            "EFFECT SIZE REPORT"

        )

        lines.append("")

        lines.append(

            f"Nombre de tailles d'effet : "

            f"{self.summary.n_effects}"

        )

        lines.append("")

        for result in self.summary.results:

            lines.append(

                f"{result.name}"

            )

            lines.append(

                f"Valeur : {result.statistic:.4f}"

            )

            lines.append(

                f"Importance : {result.magnitude}"

            )

            lines.append(

                result.interpretation

            )

            lines.append("")

        return "\n".join(

            lines

        )

    # ==========================================================
# CSV
# ==========================================================

    def to_csv(

        self,

        filename,

        **kwargs,

    ):

        self.summary.table().to_csv(

            filename,

            index=False,

            **kwargs

        )

        return filename

    # ==========================================================
# EXCEL
# ==========================================================

    def to_excel(

        self,

        filename,

        **kwargs,

    ):

        self.summary.table().to_excel(

            filename,

            index=False,

            **kwargs

        )

        return filename

# ==========================================================
# SERVICE
# ==========================================================

class Report:

    @staticmethod

    def generate(

        summary,

    ):

        return EffectSizeReport(

            summary

        )