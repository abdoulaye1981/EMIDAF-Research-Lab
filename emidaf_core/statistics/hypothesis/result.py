"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Results
=========================================================
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HypothesisResult:

    test_name: str
    statistic: float | None = None
    p_value: float | None = None
    alpha: float = 0.05

    reject_null: bool | None = None

    null_hypothesis: str = ""
    alternative_hypothesis: str = ""

    conclusion: str = ""

    details: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self):

        if (
            self.reject_null is None
            and self.p_value is not None
        ):
            self.reject_null = (
                self.p_value < self.alpha
            )

        if not self.conclusion:

            if self.reject_null is True:

                self.conclusion = (
                    "Rejet de l'hypothèse nulle."
                )

            elif self.reject_null is False:

                self.conclusion = (
                    "Non-rejet de l'hypothèse nulle."
                )

    @property
    def significant(self):

        if self.p_value is None:
            return None

        return self.p_value < self.alpha

    def to_dict(self):

        return {
            "test_name": self.test_name,
            "statistic": self.statistic,
            "p_value": self.p_value,
            "alpha": self.alpha,
            "reject_null": self.reject_null,
            "null_hypothesis":
                self.null_hypothesis,
            "alternative_hypothesis":
                self.alternative_hypothesis,
            "conclusion": self.conclusion,
            "details": self.details
        }

    def summary(self):

        return {
            "test": self.test_name,
            "statistique": self.statistic,
            "p_value": self.p_value,
            "alpha": self.alpha,
            "significatif": self.significant,
            "conclusion": self.conclusion
        }

    def __repr__(self):

        return (
            f"HypothesisResult("
            f"test_name='{self.test_name}', "
            f"statistic={self.statistic}, "
            f"p_value={self.p_value}, "
            f"alpha={self.alpha}, "
            f"reject_null={self.reject_null})"
        )
