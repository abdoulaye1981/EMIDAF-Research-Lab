"""
=========================================================
EMIDAF Framework
Logistic Regression Result
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
class LogisticResult(ModelResult):
    """
    Résultat spécialisé d'une régression logistique.
    """

    category: str = "Machine Learning"

    classes: list = field(
        default_factory=list
    )

    odds_ratios: dict = field(
        default_factory=dict
    )

    n_classes: int = 0

    is_binary: bool = False

    threshold: float | None = None

    def summary(self):

        return {
            "Model": self.model_name,
            "Task": self.task,
            "Accuracy": self.accuracy,
            "Precision": self.precision,
            "Recall": self.recall,
            "F1": self.f1_score,
            "ROC-AUC": self.roc_auc,
            "Log-loss": self.log_loss,
            "Classes": self.n_classes,
            "Features": len(self.features),
        }
