"""
=========================================================
EMIDAF Framework
Correlation Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat d'une analyse de corrélation.

Utilisé par :

- Pearson
- Spearman
- Kendall
- Phi
- Cramer's V
- PointBiserial
- MutualInformation
- DistanceCorrelation
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .statistic_result import StatisticResult


@dataclass(slots=True)
class CorrelationResult(StatisticResult):
    """
    Résultat d'une corrélation.
    """

    category: str = "Correlation"

    # =====================================================
    # Variables
    # =====================================================

    variable_x: str = ""

    variable_y: str = ""

    method: str = ""

    # =====================================================
    # Résultats
    # =====================================================

    coefficient: float | None = None

    p_value: float | None = None

    statistic: float | None = None

    alpha: float = 0.05

    confidence_interval: tuple[float, float] | None = None

    # =====================================================
    # Interprétation
    # =====================================================

    strength: str = ""

    direction: str = ""

    interpretation: str = ""

    reject_null: bool = False

    significant: bool = False

    # =====================================================
    # Métadonnées
    # =====================================================

    degrees_of_freedom: int | None = None

    sample_size: int = 0

    effect_size: float | None = None

    # =====================================================
    # Validation
    # =====================================================

    def is_significant(self) -> bool:

        return self.significant

    def is_positive(self) -> bool:

        return (

            self.coefficient is not None

            and

            self.coefficient > 0

        )

    def is_negative(self) -> bool:

        return (

            self.coefficient is not None

            and

            self.coefficient < 0

        )

    def is_perfect(self) -> bool:

        if self.coefficient is None:

            return False

        return abs(self.coefficient) == 1

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Method": self.method,

            "Variable X": self.variable_x,

            "Variable Y": self.variable_y,

            "Coefficient": self.coefficient,

            "P-Value": self.p_value,

            "Strength": self.strength,

            "Direction": self.direction,

            "Significant": self.significant

        }

    # =====================================================
    # Export compact
    # =====================================================

    def compact(self):

        return {

            "method": self.method,

            "coefficient": self.coefficient,

            "p_value": self.p_value

        }

    # =====================================================
    # Représentation
    # =====================================================

    def __repr__(self):

        return (

            f"CorrelationResult("

            f"method='{self.method}', "

            f"coefficient={self.coefficient}, "

            f"p_value={self.p_value}"

            f")"

        )