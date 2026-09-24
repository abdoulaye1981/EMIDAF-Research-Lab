"""
=========================================================
EMIDAF Framework
Multilevel Model Result
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
class MultilevelResult(ModelResult):
    """
    Résultat spécialisé d'un modèle multiniveau.
    """

    category: str = "Statistical Modeling"

    fixed_effects: dict = field(
        default_factory=dict
    )

    standard_errors: dict = field(
        default_factory=dict
    )

    z_statistics: dict = field(
        default_factory=dict
    )

    p_values: dict = field(
        default_factory=dict
    )

    confidence_intervals: dict = field(
        default_factory=dict
    )

    group_column: str = ""

    n_groups: int = 0

    group_variance: float | None = None

    residual_variance: float | None = None

    icc: float | None = None

    log_likelihood: float | None = None

    aic: float | None = None

    bic: float | None = None

    converged: bool = False

    def summary(self):

        return {
            "Model": self.model_name,
            "Task": self.task,
            "Groups": self.n_groups,
            "ICC": self.icc,
            "AIC": self.aic,
            "BIC": self.bic,
            "Converged": self.converged,
            "Features": len(self.features),
        }
