"""
=========================================================
EMIDAF Framework v1.0
Profile Summary
---------------------------------------------------------
Résumé global d'un profil de dataset.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProfileSummary:
    """
    Résumé général d'un dataset.

    Cette classe est utilisée par l'interface graphique,
    les tableaux de bord et les rapports.
    """

    # ======================================================
    # Structure
    # ======================================================

    rows: int = 0

    columns: int = 0

    cells: int = 0

    memory_usage: int = 0

    # ======================================================
    # Types de variables
    # ======================================================

    numeric_columns: int = 0

    categorical_columns: int = 0

    datetime_columns: int = 0

    boolean_columns: int = 0

    text_columns: int = 0

    unknown_columns: int = 0

    # ======================================================
    # Qualité
    # ======================================================

    missing_values: int = 0

    missing_percentage: float = 0.0

    duplicate_rows: int = 0

    duplicate_percentage: float = 0.0

    constant_columns: int = 0

    empty_columns: int = 0

    # ======================================================
    # Outliers
    # ======================================================

    outlier_columns: int = 0

    outlier_values: int = 0

    # ======================================================
    # Corrélations
    # ======================================================

    high_correlations: int = 0

    multicollinear_variables: int = 0

    # ======================================================
    # Statistiques
    # ======================================================

    analyzed_variables: int = 0

    analyzed_numeric: int = 0

    analyzed_categorical: int = 0

    analyzed_datetime: int = 0

    # ======================================================
    # Scores
    # ======================================================

    quality_score: float = 100.0

    completeness_score: float = 100.0

    consistency_score: float = 100.0

    uniqueness_score: float = 100.0

    validity_score: float = 100.0

    overall_score: float = 100.0

    # ======================================================
    # Recommandations
    # ======================================================

    recommendation_count: int = 0

    warning_count: int = 0

    critical_count: int = 0

    # ======================================================
    # Analyse
    # ======================================================

    ready_for_statistics: bool = False

    ready_for_visualization: bool = False

    ready_for_machine_learning: bool = False

    ready_for_reporting: bool = False

    # ======================================================
    # Informations complémentaires
    # ======================================================

    quality_level: str = "Excellent"

    profile_status: str = "READY"

    messages: list[str] = field(
        default_factory=list
    )

    # ======================================================
    # Méthodes
    # ======================================================

    @property
    def shape(self) -> tuple[int, int]:
        """
        Dimensions du dataset.
        """
        return (
            self.rows,
            self.columns
        )

    @property
    def total_types(self) -> int:
        """
        Nombre total de types détectés.
        """
        return (

            self.numeric_columns +

            self.categorical_columns +

            self.datetime_columns +

            self.boolean_columns +

            self.text_columns +

            self.unknown_columns

        )

    def add_message(
        self,
        message: str
    ) -> None:
        """
        Ajoute un message.
        """

        self.messages.append(message)

    def add_warning(
        self,
        message: str
    ) -> None:
        """
        Ajoute un avertissement.
        """

        self.warning_count += 1

        self.messages.append(

            f"WARNING : {message}"

        )

    def add_critical(
        self,
        message: str
    ) -> None:
        """
        Ajoute une erreur critique.
        """

        self.critical_count += 1

        self.messages.append(

            f"CRITICAL : {message}"

        )

    def compute_quality_level(self) -> None:
        """
        Détermine le niveau de qualité.
        """

        score = self.overall_score

        if score >= 90:

            self.quality_level = "Excellent"

        elif score >= 80:

            self.quality_level = "Very Good"

        elif score >= 70:

            self.quality_level = "Good"

        elif score >= 60:

            self.quality_level = "Average"

        elif score >= 40:

            self.quality_level = "Poor"

        else:

            self.quality_level = "Critical"

    def update_readiness(self) -> None:
        """
        Détermine les traitements possibles.
        """

        self.ready_for_statistics = (

            self.overall_score >= 60

        )

        self.ready_for_visualization = (

            self.overall_score >= 50

        )

        self.ready_for_machine_learning = (

            self.overall_score >= 70

        )

        self.ready_for_reporting = True

    def finalize(self) -> None:
        """
        Finalise le résumé.
        """

        self.cells = self.rows * self.columns

        self.compute_quality_level()

        self.update_readiness()

    def to_dict(self) -> dict:
        """
        Conversion dictionnaire.
        """

        return {

            key: getattr(self, key)

            for key in self.__dataclass_fields__

        }

    @classmethod
    def from_dict(
        cls,
        values: dict
    ):

        return cls(**values)