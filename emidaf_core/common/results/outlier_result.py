"""
=========================================================
EMIDAF Framework
Outlier Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat des détecteurs d'anomalies.

Utilisé par

- ZScore
- ModifiedZScore
- IQR
- Mahalanobis
- IsolationForest
- LocalOutlierFactor
- DBSCAN
- HBOS
- OneClassSVM
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .statistic_result import StatisticResult


@dataclass(slots=True)
class OutlierResult(StatisticResult):
    """
    Résultat d'un détecteur d'anomalies.
    """

    category: str = "Outliers"

    # =====================================================
    # Informations générales
    # =====================================================

    method: str = ""

    variable: str = ""

    threshold: float | None = None

    contamination: float | None = None

    # =====================================================
    # Résultats
    # =====================================================

    total_observations: int = 0

    outlier_count: int = 0

    inlier_count: int = 0

    outlier_percentage: float = 0.0

    inlier_percentage: float = 0.0

    # =====================================================
    # Indices
    # =====================================================

    outlier_indices: list[int] = field(
        default_factory=list
    )

    inlier_indices: list[int] = field(
        default_factory=list
    )

    # =====================================================
    # Valeurs
    # =====================================================

    outlier_values: list = field(
        default_factory=list
    )

    scores: list[float] = field(
        default_factory=list
    )

    labels: list[int] = field(
        default_factory=list
    )
    # =====================================================

    # Métadonnées scientifiques de détection

    # =====================================================

    score_type: str = ""

    score_direction: str = "none"

    method_family: str = ""

    scaling_sensitive: bool = False

    # =====================================================

    # Paramètres

    # =====================================================

    parameters: dict = field(
        default_factory=dict
    )

    diagnostics: dict = field(
        default_factory=dict
    )

    # =====================================================
    # Validation
    # =====================================================

    def has_outliers(self) -> bool:

        return self.outlier_count > 0

    def has_scores(self) -> bool:

        return len(self.scores) > 0

    def has_labels(self) -> bool:

        return len(self.labels) > 0

    # =====================================================
    # Pourcentages
    # =====================================================

    def compute_percentages(self):

        if self.total_observations == 0:

            return

        self.outlier_percentage = round(

            self.outlier_count

            /

            self.total_observations

            * 100,

            2

        )

        self.inlier_percentage = round(

            self.inlier_count

            /

            self.total_observations

            * 100,

            2

        )

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Method": self.method,

            "Variable": self.variable,

            "Observations": self.total_observations,

            "Outliers": self.outlier_count,

            "Inliers": self.inlier_count,

            "Outlier %": self.outlier_percentage

        }

    # =====================================================
    # Export compact
    # =====================================================

    def compact(self):

        return {

            "method": self.method,

            "outliers": self.outlier_count,

            "percentage": self.outlier_percentage

        }

    # =====================================================
    # Affichage
    # =====================================================

    def __repr__(self):

        return (

            f"OutlierResult("

            f"method='{self.method}', "

            f"outliers={self.outlier_count}, "

            f"percentage={self.outlier_percentage}"

            f")"

        )
