"""
=========================================================
EMIDAF Framework
Distribution Report Generator
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import json

import pandas as pd

from .summary import DistributionAnalysis

from .interpretation import Interpretation

# ==========================================================
# REPORT
# ==========================================================

class DistributionReport:

    """
    Distribution report.
    """

    def __init__(

        self,

        data,

    ):

        self.summary=(

            DistributionAnalysis.analyze(

                data

            )

        )

    # ==========================================================
# DICTIONARY
# ==========================================================

    def to_dict(

        self,

    ):

        report=dict(

            self.summary

        )

        report[

            "interpretation"

        ]=(

            Interpretation.interpret(

                self.summary

            )

        )

        return report

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

        best=self.summary[

            "best_distribution"

        ]

        row={

            "Distribution":

                best["Distribution"],

            "AIC":

                best["AIC"],

            "BIC":

                best["BIC"],

            "LogLikelihood":

                best["LogLikelihood"]

        }

        return pd.DataFrame(

            [row]

        )

    # ==========================================================
# MARKDOWN
# ==========================================================

    def to_markdown(

        self,

    ):

        report=self.to_dict()

        best=report[

            "best_distribution"

        ]

        interpretation=report[

            "interpretation"

        ]

        text=[]

        text.append(

            "# Distribution Report"

        )

        text.append("")

        text.append(

            "## Best Distribution"

        )

        text.append("")

        text.append(

            f"- Distribution : {best['Distribution']}"

        )

        text.append(

            f"- AIC : {best['AIC']}"

        )

        text.append(

            f"- BIC : {best['BIC']}"

        )

        text.append(

            f"- LogLikelihood : {best['LogLikelihood']}"

        )

        text.append("")

        text.append(

            "## Interpretation"

        )

        text.append("")

        for key,value in interpretation.items():

            if isinstance(

                value,

                list

            ):

                text.append(

                    f"### {key}"

                )

                for item in value:

                    text.append(

                        f"- {item}"

                    )

            else:

                text.append(

                    f"- {value}"

                )

        return "\n".join(

            text

        )

    # ==========================================================
# HTML
# ==========================================================

    def to_html(

        self,

    ):

        return (

            self.to_dataframe()

            .to_html(

                index=False

            )

        )

    # ==========================================================
# LATEX
# ==========================================================

    def to_latex(

        self,

    ):

        return (

            self.to_dataframe()

            .to_latex(

                index=False

            )

        )

    # ==========================================================
# TEXT
# ==========================================================

    def to_text(

        self,

    ):

        best=self.summary[

            "best_distribution"

        ]

        interpretation=(

            Interpretation.interpret(

                self.summary

            )

        )

        lines=[]

        lines.append(

            "DISTRIBUTION REPORT"

        )

        lines.append("")

        lines.append(

            f"Distribution : {best['Distribution']}"

        )

        lines.append(

            f"AIC : {best['AIC']}"

        )

        lines.append(

            f"BIC : {best['BIC']}"

        )

        lines.append(

            f"LogLikelihood : {best['LogLikelihood']}"

        )

        lines.append("")

        lines.append(

            "INTERPRETATION"

        )

        for key,value in interpretation.items():

            if isinstance(

                value,

                list

            ):

                for item in value:

                    lines.append(

                        "- "+item

                    )

            else:

                lines.append(

                    value

                )

        return "\n".join(

            lines

        )

# ==========================================================
# SERVICE
# ==========================================================

class Report:

    @staticmethod

    def generate(

        data,

    ):

        return DistributionReport(

            data

        )