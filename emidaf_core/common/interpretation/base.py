"""
=========================================================
EMIDAF
Scientific Interpretation Base Classes
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)

class ScientificInterpretation:

    ##################################################
    # GENERAL
    ##################################################

    title:str=""

    statistic:str=""

    value=None

    ##################################################
    # SCIENTIFIC
    ##################################################

    interpretation:str=""

    conclusion:str=""

    recommendation:str=""

    ##################################################
    # EDUCATIONAL
    ##################################################

    explanation:str=""

    ##################################################
    # RESEARCH
    ##################################################

    reporting_text:str=""

    ##################################################
    # REFERENCES
    ##################################################

    bibliography:list=field(

        default_factory=list

    )

    ##################################################
    # VISUALIZATION
    ##################################################

    suggested_plots:list=field(

        default_factory=list
    )