"""
=========================================================
EMIDAF Framework
Inferential Report Generator
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import json

import pandas as pd

from .summary import Inferential
from .interpretation import Interpretation

# ==========================================================
# REPORT
# ==========================================================

class InferentialReport:

    """
    Rapport complet
    d'inférence statistique.
    """

    def __init__(

        self,

        dataframe,

        target,

        group,

    ):

        self.analysis=Inferential.analyze(

            dataframe,

            target,

            group

        )

        self.target=target

        self.group=group

    # ==========================================================
# DICTIONARY
# ==========================================================

    def to_dict(

        self,

    ):

        report=dict(

            self.analysis

        )

        result=report[

            "automatic_test"

        ][

            "inferential"

        ]

        report[

            "interpretation"

        ]=(

            Interpretation.interpret(

                result

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

        result=self.analysis[

            "automatic_test"

        ][

            "inferential"

        ]

        rows=[

            {

                "Statistic":

                    result.statistic,

                "p-value":

                    result.p_value,

                "Reject H0":

                    result.reject_null

            }

        ]

        return pd.DataFrame(

            rows

        )


    # ==========================================================
# MARKDOWN
# ==========================================================

    def to_markdown(

        self,

    ):

        report=self.to_dict()

        test=report[

            "automatic_test"

        ][

            "inferential"

        ]

        interpretation=report[

            "interpretation"

        ]

        text=[]

        text.append(

            "# Inferential Report"

        )

        text.append("")

        text.append(

            f"Target : {self.target}"

        )

        text.append(

            f"Group : {self.group}"

        )

        text.append("")

        text.append(

            "## Test"

        )

        text.append("")

        text.append(

            f"- Statistic : {test.statistic}"

        )

        text.append(

            f"- p-value : {test.p_value}"

        )

        text.append(

            f"- Reject H0 : {test.reject_null}"

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

        report=self.to_dict()

        test=report[

            "automatic_test"

        ][

            "inferential"

        ]

        interpretation=report[

            "interpretation"

        ]

        lines=[]

        lines.append(

            "INFERENTIAL REPORT"

        )

        lines.append("")

        lines.append(

            f"Target : {self.target}"

        )

        lines.append(

            f"Group : {self.group}"

        )

        lines.append("")

        lines.append(

            f"Statistic : {test.statistic}"

        )

        lines.append(

            f"P-value : {test.p_value}"

        )

        lines.append(

            f"Reject H0 : {test.reject_null}"

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

        dataframe,

        target,

        group,

    ):

        return InferentialReport(

            dataframe,

            target,

            group

        )