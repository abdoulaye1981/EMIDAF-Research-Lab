from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .statistic_result import StatisticResult


@dataclass(slots=True)
class HypothesisResult(StatisticResult):
    """
    Résultat standard d'un test d'hypothèse.
    """

    category: str = "Hypothesis"

    test_name: str = ""

    hypothesis: str = ""

    null_hypothesis: str = ""

    alternative_hypothesis: str = ""

    statistic: float | None = None

    p_value: float | None = None

    alpha: float = 0.05

    reject_null: bool = False

    significant: bool = False

    decision: str = ""

    interpretation: str = ""

    sample_size: int = 0

    degrees_of_freedom: int | None = None

    effect_size: float | None = None

    confidence_interval: tuple[float, float] | None = None

    power: float | None = None

    assumptions: dict[str, Any] = field(
        default_factory=dict
    )

    diagnostics: dict[str, Any] = field(
        default_factory=dict
    )

    extra: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self):
        """
        Initialise automatiquement la décision statistique.
        """

        if self.p_value is not None:
            self.reject_null = (
                self.p_value < self.alpha
            )

            self.significant = self.reject_null

        if not self.decision:

            if self.reject_null:
                self.decision = (
                    "Rejet de l'hypothèse nulle."
                )

            else:
                self.decision = (
                    "Non-rejet de l'hypothèse nulle."
                )

        if not self.interpretation:
            self.interpretation = self.decision

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
        Indique si le test est statistiquement significatif.
        """

        return self.significant

    def significance_code(self) -> str:
        """
        Retourne le code de significativité.
        """

        if self.p_value is None:
            return ""

        if self.p_value < 0.001:
            return "***"

        if self.p_value < 0.01:
            return "**"

        if self.p_value < 0.05:
            return "*"

        return "ns"

    def summary(self) -> dict[str, Any]:
        """
        Résumé du résultat.
        """

        return {
            "Test": self.test_name,
            "Statistic": self.statistic,
            "P-value": self.p_value,
            "Alpha": self.alpha,
            "Reject H0": self.reject_null,
            "Decision": self.decision,
            "Interpretation": self.interpretation,
        }

    def compact(self) -> dict[str, Any]:
        """
        Version compacte du résultat.
        """

        return {
            "test": self.test_name,
            "statistic": self.statistic,
            "p_value": self.p_value,
            "decision": self.decision,
        }

    def __repr__(self) -> str:

        return (
            f"HypothesisResult("
            f"test='{self.test_name}', "
            f"statistic={self.statistic}, "
            f"p_value={self.p_value}, "
            f"reject_null={self.reject_null}"
            f")"
        )
