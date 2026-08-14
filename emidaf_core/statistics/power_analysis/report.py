"""
=========================================================
EMIDAF Framework
Power Analysis Report Generator
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

class PowerAnalysisReport:

    """
    Report generator for
    power analyses.
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

        best=self.summary.best_power()

        smallest=self.summary.smallest_sample()

        return {

            "number_of_analyses":

                self.summary.n_analyses,

            "best_power":

                None if best is None else {

                    "test":best.test,

                    "power":best.power,

                    "sample_size":best.sample_size

                },

            "smallest_sample":

                None if smallest is None else {

                    "test":smallest.test,

                    "sample_size":smallest.sample_size

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

        return self.summary.table().to_markdown(

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

        return PowerAnalysisReport(

            summary

        )