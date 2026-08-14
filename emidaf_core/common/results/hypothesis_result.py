"""
=========================================================
EMIDAF Framework
Hypothesis Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat standard de tous les tests d'hypothèses.

Utilisé par :

- ShapiroWilk
- AndersonDarling
- KolmogorovSmirnov
- JarqueBera
- DAgostinoPearson
- StudentTTest
- WelchTTest
- ANOVA
- MannWhitney
- Wilcoxon
- KruskalWallis
- Friedman
- ChiSquare
- FisherExact
- McNemar
- Levene
- Bartlett
- LittleMCAR
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .statistic_result import StatisticResult


@dataclass(slots=True)
class HypothesisResult(StatisticResult):
    """
    Résultat d'un test statistique.
    """

    category: str = "Hypothesis"

    # =====================================================
    # Test
    # =====================================================

    test_name: str = ""

    hypothesis: str = ""

    null_hypothesis: str = ""

    alternative_hypothesis: str = ""

    # =====================================================
    # Résultat
    # =====================================================

    statistic: float | None = None

    p_value: float | None = None

    alpha: float = 0.05

    reject_null: bool = False

    significant: bool = False

    decision: str = ""

    interpretation: str = ""

    # =====================================================
    # Informations statistiques
    # =====================================================

    sample_size: int = 0

    degrees_of_freedom: int | None = None

    effect_size: float | None = None

    confidence_interval: tuple[float, float] | None = None

    power: float | None = None

    # =====================================================
    # Informations complémentaires
    # =====================================================

    assumptions: dict = field(default_factory=dict)

    diagnostics: dict = field(default_factory=dict)

    extra: dict = field(default_factory=dict)

    # =====================================================
    # Validation
    # =====================================================

    def accepted(self) -> bool:
        """
        H0 est conservée.
        """

        return not self.reject_null

    def rejected(self) -> bool:
        """
        H0 est rejetée.
        """

        return self.reject_null

    def is_significant(self) -> bool:
        """
        Test significatif.
        """

        return self.significant

    # =====================================================
    # Significativité
    # =====================================================

    def significance_code(self) -> str:

        if self.p_value is None:
            return ""

        if self.p_value < 0.001:
            return "***"

        if self.p_value < 0.01:
            return "**"

        if self.p_value < 0.05:
            return "*"

        return "ns"

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Test": self.test_name,

            "Statistic": self.statistic,

            "P-value": self.p_value,

            "Alpha": self.alpha,

            "Reject H0": self.reject_null,

            "Decision": self.decision,

            "Interpretation": self.interpretation

        }

    # =====================================================
    # Export
    # =====================================================

    def compact(self):

        return {

            "test": self.test_name,

            "statistic": self.statistic,

            "p_value": self.p_value,

            "decision": self.decision

        }

    # =====================================================
    # Affichage
    # =====================================================

    def __repr__(self):

        return (

            f"HypothesisResult("

            f"test='{self.test_name}', "

            f"statistic={self.statistic}, "

            f"p_value={self.p_value}, "

            f"reject_null={self.reject_null}"

            f")"

        )