"""
=========================================================
EMIDAF Framework
Statistic Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe de base de tous les résultats statistiques.

Toutes les statistiques EMIDAF retournent une classe
héritant de StatisticResult.

Classes dérivées

- DescriptiveResult
- CorrelationResult
- HypothesisResult
- OutlierResult

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

import numpy as np
import pandas as pd

from .base_result import BaseResult


@dataclass(slots=True)
class StatisticResult(BaseResult):
    """
    Classe de base de tous les résultats statistiques.
    """

    # =====================================================
    # Information générale
    # =====================================================

    statistic_name: str = ""

    variable: str = ""

    variables: list[str] = field(default_factory=list)

    statistic: float | None = None

    value: float | int | str | dict | None = None

    # =====================================================
    # Dataset
    # =====================================================

    sample_size: int = 0

    missing_values: int = 0

    missing_rate: float = 0.0

    unique_values: int = 0

    duplicated_values: int = 0

    dtype: str = ""

    # =====================================================
    # Metadata scientifique
    # =====================================================

    library: str = "EMIDAF"

    algorithm: str = ""

    version: str = "1.0.0"

    references: list[str] = field(

        default_factory=list

    )

    warnings: list[str] = field(

        default_factory=list

    )

    notes: list[str] = field(

        default_factory=list

    )

    # =====================================================
    # Validation
    # =====================================================

    def is_valid(self):

        return self.success

    # =====================================================

    def has_missing(self):

        return self.missing_values > 0

    # =====================================================

    def has_warning(self):

        return len(self.warnings) > 0

    # =====================================================

    def has_notes(self):

        return len(self.notes) > 0

    # =====================================================
    # Warning
    # =====================================================

    def add_warning(

        self,

        message: str,

    ):

        self.warnings.append(message)

    # =====================================================

    def add_note(

        self,

        message: str,

    ):

        self.notes.append(message)

    # =====================================================

    def add_reference(

        self,

        citation: str,

    ):

        self.references.append(citation)

    # =====================================================
    # Scientific summary
    # =====================================================

    def scientific_summary(self):

        return {

            "Statistic":

                self.statistic_name,

            "Variable":

                self.variable,

            "Value":

                self.value,

            "Sample":

                self.sample_size,

            "Missing":

                self.missing_values,

            "Success":

                self.success

        }

    # =====================================================
    # Export
    # =====================================================

    def to_markdown(self):

        rows = [

            "| Property | Value |",

            "|----------|-------|",

        ]

        for key, value in self.to_dict().items():

            rows.append(

                f"| {key} | {value} |"

            )

        return "\n".join(rows)

    # =====================================================

    def to_html(self):

        return self.to_dataframe().to_html(

            index=False

        )

    # =====================================================

    def to_csv(self):

        return self.to_dataframe().to_csv(

            index=False

        )

    # =====================================================

    def to_numpy(self):

        return np.array(

            list(

                self.to_dict().values()

            ),

            dtype=object

        )

    # =====================================================

    def describe(self):

        return pd.Series(

            self.to_dict()

        )

    # =====================================================
    # Merge
    # =====================================================

    def merge(

        self,

        other: "StatisticResult",

    ):

        data = self.to_dict()

        data.update(

            other.to_dict()

        )

        return StatisticResult(

            **data

        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.success = True

        self.execution_time = 0.0

        self.metadata.clear()

        self.references.clear()

        self.notes.clear()

        self.warnings.clear()

    # =====================================================
    # Display
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"("

            f"statistic='{self.statistic_name}', "

            f"value={self.value}, "

            f"sample={self.sample_size}"

            f")"

        )