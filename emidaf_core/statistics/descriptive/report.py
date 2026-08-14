"""
=========================================================
EMIDAF Framework
Descriptive Statistics Report
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import json
import pandas as pd

from .summary import Summary
from .interpretation import Interpretation

# ==========================================================
# REPORT
# ==========================================================

class DescriptiveReport:

    """
    Générateur de rapports
    statistiques descriptifs.
    """

    def __init__(

        self,

        x,

        variable=None,

    ):

        self.variable=variable

        self.summary=Summary.describe(

            x,

            name=variable

        ).compute()

        self.interpretation=(

            Interpretation.interpret(

                self.summary

            )

        )

    # ==========================================================
# DICTIONARY
# ==========================================================

    def to_dict(

        self,

    ):

        return {

            "variable":

                self.variable,

            "summary":

                self.summary,

            "interpretation":

                self.interpretation

        }
    
    # ==========================================================
# DATAFRAME
# ==========================================================

    def to_dataframe(

        self,

    ):

        rows=[]

        for category,data in self.summary.items():

            for statistic,value in data.items():

                rows.append({

                    "Category":

                        category,

                    "Statistic":

                        statistic,

                    "Value":

                        value

                })

        return pd.DataFrame(

            rows

        )
    
    # ==========================================================
# DATAFRAME
# ==========================================================

    def to_dataframe(

        self,

    ):

        rows=[]

        for category,data in self.summary.items():

            for statistic,value in data.items():

                rows.append({

                    "Category":

                        category,

                    "Statistic":

                        statistic,

                    "Value":

                        value

                })

        return pd.DataFrame(

            rows

        )

    # ==========================================================
# MARKDOWN
# ==========================================================

    def to_markdown(

        self,

    ):

        text=[]

        text.append(

            "# Descriptive Statistics Report"

        )

        text.append("")

        if self.variable:

            text.append(

                f"## Variable : {self.variable}"

            )

            text.append("")

        for category,data in self.summary.items():

            text.append(

                f"### {category.title()}"

            )

            text.append("")

            for statistic,value in data.items():

                text.append(

                    f"- **{statistic}** : {value}"

                )

            text.append("")

        text.append(

            "## Interpretation"

        )

        text.append("")

        for k,v in self.interpretation[

            "interpretation"

        ].items():

            text.append(

                f"- {v}"

            )

        text.append("")

        text.append(

            "## Recommendations"

        )

        text.append("")

        for rec in self.interpretation[

            "recommendations"

        ]:

            text.append(

                f"- {rec}"

            )

        return "\n".join(text)
    
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
# HTML
# ==========================================================

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

        lines=[]

        if self.variable:

            lines.append(

                f"Variable : {self.variable}"

            )

            lines.append("")

        for category,data in self.summary.items():

            lines.append(

                category.upper()

            )

            for statistic,value in data.items():

                lines.append(

                    f"{statistic:<30} {value}"

                )

            lines.append("")

        lines.append(

            "INTERPRETATION"

        )

        for value in self.interpretation[

            "interpretation"

        ].values():

            lines.append(

                "- "+value

            )

        lines.append("")

        lines.append(

            "RECOMMENDATIONS"

        )

        for rec in self.interpretation[

            "recommendations"

        ]:

            lines.append(

                "- "+rec

            )

        return "\n".join(lines)

    # ==========================================================
# SERVICE
# ==========================================================

class Report:

    @staticmethod

    def generate(

        x,

        variable=None,

    ):

        return DescriptiveReport(

            x,

            variable

        )