"""
=========================================================
EMIDAF Framework v1.0
Profile Result
---------------------------------------------------------
Résultat complet du profilage d'un dataset.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .profile_metadata import ProfileMetadata
from .profile_summary import ProfileSummary


@dataclass(slots=True)
class ProfileResult:
    """
    Objet principal retourné par DatasetProfiler.

    Cette classe centralise tous les résultats produits
    par les analyzers du moteur de profilage.

    Aucun calcul n'est réalisé ici.

    Cette classe est uniquement un conteneur de données.
    """

    # =====================================================
    # Métadonnées
    # =====================================================

    metadata: ProfileMetadata = field(
        default_factory=ProfileMetadata
    )

    # =====================================================
    # Résumé
    # =====================================================

    summary: ProfileSummary = field(
        default_factory=ProfileSummary
    )

    # =====================================================
    # Analyse Structure
    # =====================================================

    structure: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Types de données
    # =====================================================

    datatypes: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Qualité
    # =====================================================

    quality: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Valeurs manquantes
    # =====================================================

    missing: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Doublons
    # =====================================================

    duplicates: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Cardinalité
    # =====================================================

    cardinality: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Variables numériques
    # =====================================================

    numerical: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Variables catégorielles
    # =====================================================

    categorical: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Variables temporelles
    # =====================================================

    datetime: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Variables texte
    # =====================================================

    text: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Mémoire
    # =====================================================

    memory: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Distributions
    # =====================================================

    distributions: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Corrélations
    # =====================================================

    correlations: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Multicolinéarité
    # =====================================================

    multicollinearity: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Valeurs aberrantes
    # =====================================================

    outliers: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Normalité
    # =====================================================

    normality: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Stationnarité
    # =====================================================

    stationarity: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Analyse temporelle
    # =====================================================

    temporal: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Analyse spatiale
    # =====================================================

    spatial: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Variable cible
    # =====================================================

    target: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Variables explicatives
    # =====================================================

    features: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Statistiques
    # =====================================================

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Tests statistiques
    # =====================================================

    statistical_tests: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Scores
    # =====================================================

    scores: dict[str, float] = field(
        default_factory=dict
    )

    # =====================================================
    # Recommandations
    # =====================================================

    recommendations: list[dict[str, Any]] = field(
        default_factory=list
    )

    # =====================================================
    # Alertes
    # =====================================================

    warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Erreurs
    # =====================================================

    errors: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Informations complémentaires
    # =====================================================

    extras: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Méthodes utilitaires
    # =====================================================

    def add_warning(
        self,
        message: str
    ) -> None:
        """
        Ajoute un avertissement.
        """

        self.warnings.append(message)

        self.summary.warning_count += 1

    def add_error(
        self,
        message: str
    ) -> None:
        """
        Ajoute une erreur.
        """

        self.errors.append(message)

        self.metadata.error_count += 1

    def add_recommendation(
        self,
        recommendation: dict[str, Any]
    ) -> None:
        """
        Ajoute une recommandation.
        """

        self.recommendations.append(
            recommendation
        )

        self.summary.recommendation_count += 1

    def set_score(
        self,
        name: str,
        value: float
    ) -> None:
        """
        Ajoute un score.
        """

        self.scores[name] = float(value)

    def get_score(
        self,
        name: str,
        default: float = 0.0
    ) -> float:
        """
        Retourne un score.
        """

        return self.scores.get(
            name,
            default
        )

    def register_analysis(
        self,
        name: str,
        result: dict[str, Any]
    ) -> None:
        """
        Enregistre dynamiquement
        un résultat d'analyse.
        """

        self.extras[name] = result

    def get_analysis(
        self,
        name: str
    ) -> dict[str, Any]:
        """
        Retourne une analyse.
        """

        return self.extras.get(
            name,
            {}
        )

    @property
    def is_valid(self) -> bool:
        """
        Le profil est valide
        s'il ne contient aucune erreur.
        """

        return len(self.errors) == 0

    @property
    def recommendation_count(self) -> int:
        """
        Nombre de recommandations.
        """

        return len(
            self.recommendations
        )

    @property
    def warning_count(self) -> int:
        """
        Nombre d'avertissements.
        """

        return len(
            self.warnings
        )

    @property
    def error_count(self) -> int:
        """
        Nombre d'erreurs.
        """

        return len(
            self.errors
        )

    def to_dict(self) -> dict:
        """
        Conversion vers dictionnaire.

        Utilisée pour l'export JSON.
        """

        return {

            "metadata": self.metadata.to_dict(),

            "summary": self.summary.to_dict(),

            "structure": self.structure,

            "datatypes": self.datatypes,

            "quality": self.quality,

            "missing": self.missing,

            "duplicates": self.duplicates,

            "cardinality": self.cardinality,

            "numerical": self.numerical,

            "categorical": self.categorical,

            "datetime": self.datetime,

            "text": self.text,

            "memory": self.memory,

            "distributions": self.distributions,

            "correlations": self.correlations,

            "multicollinearity": self.multicollinearity,

            "outliers": self.outliers,

            "normality": self.normality,

            "stationarity": self.stationarity,

            "temporal": self.temporal,

            "spatial": self.spatial,

            "target": self.target,

            "features": self.features,

            "statistics": self.statistics,

            "statistical_tests": self.statistical_tests,

            "scores": self.scores,

            "recommendations": self.recommendations,

            "warnings": self.warnings,

            "errors": self.errors,

            "extras": self.extras
        }