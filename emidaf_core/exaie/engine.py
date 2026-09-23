"""
=========================================================
EMIDAF Framework
EXAIE Engine
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from .importance import GlobalImportance
from .local import LocalExplanation
from .interpretation import ExplainabilityInterpreter


class EXAIEEngine:
    """
    Moteur principal d'explicabilité EMIDAF.
    """

    def __init__(
        self,
        estimator: Any,
        X: pd.DataFrame,
        y=None,
    ):
        self.estimator = estimator
        self.X = X.copy()
        self.y = y

        self.native_importance_ = None
        self.permutation_importance_ = None

    def global_importance(
        self,
    ) -> pd.DataFrame | None:
        """
        Importance native du modèle.
        """

        self.native_importance_ = (
            GlobalImportance.native(
                self.estimator,
                self.X,
            )
        )

        return self.native_importance_

    def permutation_importance(
        self,
        *,
        n_repeats: int = 10,
        random_state: int = 42,
        scoring: str | None = None,
    ) -> pd.DataFrame:
        """
        Importance globale par permutation.
        """

        if self.y is None:
            raise ValueError(
                "La variable cible y est nécessaire "
                "pour l'importance par permutation."
            )

        self.permutation_importance_ = (
            GlobalImportance.permutation(
                self.estimator,
                self.X,
                self.y,
                n_repeats=n_repeats,
                random_state=random_state,
                scoring=scoring,
            )
        )

        return self.permutation_importance_

    def local_explanation(
        self,
        row: int = 0,
    ) -> dict:
        """
        Explication locale lorsque le modèle
        le permet.
        """

        return LocalExplanation.linear(
            self.estimator,
            self.X,
            row=row,
        )

    def summary(
        self,
    ) -> dict:
        """
        Synthèse EXAIE.

        Réutilise les importances déjà calculées
        lorsqu'elles sont disponibles afin d'éviter
        des calculs coûteux redondants.
        """

        native = self.native_importance_

        if native is None:
            native = self.global_importance()

        summary = {
            "native_available": (
                native is not None
                and not native.empty
            ),
            "native_interpretation":
                ExplainabilityInterpreter
                .global_importance(
                    native
                ),
        }

        if self.y is not None:

            permutation = (
                self.permutation_importance_
            )

            if permutation is None:
                permutation = (
                    self.permutation_importance()
                )

            summary[
                "permutation_available"
            ] = not permutation.empty

            summary[
                "permutation_interpretation"
            ] = (
                ExplainabilityInterpreter
                .permutation(
                    permutation
                )
            )

        return summary


class EXAIE(EXAIEEngine):
    """
    Façade publique EXAIE.
    """

    pass
