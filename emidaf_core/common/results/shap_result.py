"""
=========================================================
EMIDAF Framework
SHAP Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .base_result import BaseResult


@dataclass(slots=True)
class ShapResult(BaseResult):
    """
    Résultat standard d'une explication SHAP.
    """

    category: str = "Explainability"

    model_name: str = ""

    explainer_type: str = ""

    task: str = ""

    features: list[str] = field(
        default_factory=list
    )

    n_observations: int = 0

    shap_values: list = field(
        default_factory=list
    )

    base_values: list = field(
        default_factory=list
    )

    feature_importance: dict = field(
        default_factory=dict
    )

    local_explanations: list = field(
        default_factory=list
    )

    output_names: list = field(
        default_factory=list
    )

    def summary(self):

        return {
            "Model": self.model_name,
            "Explainer": self.explainer_type,
            "Task": self.task,
            "Observations": self.n_observations,
            "Features": len(self.features),
            "Importance": self.feature_importance,
        }
