"""
=========================================================
EMIDAF Framework
Cleaning Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat des opérations de nettoyage des données.

Utilisé par

- Missing Value Imputer
- Duplicate Cleaner
- Outlier Cleaner
- Encoder
- Scaler
- Normalizer
- Transformer
- Feature Selector
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .base_result import BaseResult


@dataclass(slots=True)
class CleaningResult(BaseResult):
    """
    Résultat d'une opération de nettoyage.
    """

    category: str = "Cleaning"

    # =====================================================
    # Informations générales
    # =====================================================

    operation: str = ""

    strategy: str = ""

    success: bool = True

    # =====================================================
    # Dimensions
    # =====================================================

    initial_rows: int = 0

    final_rows: int = 0

    removed_rows: int = 0

    initial_columns: int = 0

    final_columns: int = 0

    removed_columns: int = 0

    # =====================================================
    # Valeurs manquantes
    # =====================================================

    missing_before: int = 0

    missing_after: int = 0

    missing_removed: int = 0

    # =====================================================
    # Doublons
    # =====================================================

    duplicates_before: int = 0

    duplicates_after: int = 0

    duplicates_removed: int = 0

    # =====================================================
    # Valeurs aberrantes
    # =====================================================

    outliers_before: int = 0

    outliers_after: int = 0

    outliers_removed: int = 0

    # =====================================================
    # Variables
    # =====================================================

    affected_columns: list[str] = field(
        default_factory=list
    )

    removed_columns_names: list[str] = field(
        default_factory=list
    )

    created_columns: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Paramètres
    # =====================================================

    parameters: dict = field(
        default_factory=dict
    )

    statistics: dict = field(
        default_factory=dict
    )

    diagnostics: dict = field(
        default_factory=dict
    )

    warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Validation
    # =====================================================

    def rows_removed(self) -> bool:

        return self.removed_rows > 0

    def columns_removed(self) -> bool:

        return self.removed_columns > 0

    def missing_corrected(self) -> bool:

        return self.missing_removed > 0

    def duplicates_corrected(self) -> bool:

        return self.duplicates_removed > 0

    def outliers_corrected(self) -> bool:

        return self.outliers_removed > 0

    # =====================================================
    # Taux
    # =====================================================

    @property
    def row_reduction_rate(self) -> float:

        if self.initial_rows == 0:

            return 0.0

        return round(

            self.removed_rows

            / self.initial_rows

            * 100,

            2

        )

    @property
    def column_reduction_rate(self) -> float:

        if self.initial_columns == 0:

            return 0.0

        return round(

            self.removed_columns

            / self.initial_columns

            * 100,

            2

        )

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Operation": self.operation,

            "Strategy": self.strategy,

            "Initial Rows": self.initial_rows,

            "Final Rows": self.final_rows,

            "Removed Rows": self.removed_rows,

            "Initial Columns": self.initial_columns,

            "Final Columns": self.final_columns,

            "Removed Columns": self.removed_columns,

            "Missing Removed": self.missing_removed,

            "Duplicates Removed": self.duplicates_removed,

            "Outliers Removed": self.outliers_removed

        }

    # =====================================================
    # Export
    # =====================================================

    def compact(self):

        return {

            "operation": self.operation,

            "strategy": self.strategy,

            "success": self.success

        }

    # =====================================================
    # Affichage
    # =====================================================

    def __repr__(self):

        return (

            f"CleaningResult("

            f"operation='{self.operation}', "

            f"rows={self.initial_rows}->{self.final_rows}, "

            f"columns={self.initial_columns}->{self.final_columns}"

            f")"

        )