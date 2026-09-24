"""
=========================================================
EMIDAF Framework
OLS Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .model_result import ModelResult


@dataclass(slots=True)
class OLSResult(ModelResult):
    """
    Résultat statistique d'une régression OLS.
    """

    category: str = "Statistical Modeling"

    adjusted_r2: float | None = None

    aic: float | None = None
    bic: float | None = None
    log_likelihood: float | None = None

    f_statistic: float | None = None
    f_pvalue: float | None = None

    standard_errors: dict = field(
        default_factory=dict
    )

    t_statistics: dict = field(
        default_factory=dict
    )

    p_values: dict = field(
        default_factory=dict
    )

    confidence_intervals: dict = field(
        default_factory=dict
    )

    n_observations: int = 0

    degrees_freedom_model: float | None = None

    degrees_freedom_residual: float | None = None

    condition_number: float | None = None

    def summary(self):

        return {
            "Model": self.model_name,
            "Task": self.task,
            "R²": self.r2,
            "Adjusted R²": self.adjusted_r2,
            "F statistic": self.f_statistic,
            "F p-value": self.f_pvalue,
            "AIC": self.aic,
            "BIC": self.bic,
            "Observations": self.n_observations,
            "Features": len(self.features),
        }
