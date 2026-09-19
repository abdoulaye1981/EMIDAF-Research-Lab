"""
=========================================================
EMIDAF Framework v1.0
Base Imputer
---------------------------------------------------------
Classe abstraite commune aux stratégies d'imputation.
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(slots=True)
class ImputationResult:
    """
    Résultat standardisé d'une opération d'imputation.
    """

    dataframe: pd.DataFrame
    strategy: str
    columns: list[str]
    values_imputed: int
    success: bool
    message: str
    details: dict[str, Any]


class BaseImputer(ABC):
    """
    Classe abstraite de base pour toutes les méthodes
    d'imputation EMIDAF.
    """

    name: str = "BaseImputer"

    # =====================================================
    # PUBLIC
    # =====================================================

    def execute(
        self,
        dataframe: pd.DataFrame,
        columns: list[str] | None = None,
        **kwargs,
    ) -> ImputationResult:
        """
        Valide les entrées puis exécute l'imputation.
        """

        self._validate_dataframe(
            dataframe
        )

        selected_columns = self._resolve_columns(
            dataframe=dataframe,
            columns=columns,
        )

        before_missing = int(
            dataframe[
                selected_columns
            ].isna().sum().sum()
        ) if selected_columns else 0

        result_dataframe = self.impute(
            dataframe=dataframe.copy(),
            columns=selected_columns,
            **kwargs,
        )

        after_missing = int(
            result_dataframe[
                selected_columns
            ].isna().sum().sum()
        ) if selected_columns else 0

        values_imputed = max(
            0,
            before_missing - after_missing,
        )

        return ImputationResult(
            dataframe=result_dataframe,
            strategy=self.name,
            columns=selected_columns,
            values_imputed=values_imputed,
            success=True,
            message=(
                f"{values_imputed} missing value(s) imputed "
                f"using {self.name}."
            ),
            details={
                "missing_before": before_missing,
                "missing_after": after_missing,
            },
        )

    # =====================================================
    # ABSTRACT
    # =====================================================

    @abstractmethod
    def impute(
        self,
        dataframe: pd.DataFrame,
        columns: list[str],
        **kwargs,
    ) -> pd.DataFrame:
        """
        Implémente la stratégie d'imputation.
        """

        raise NotImplementedError

    # =====================================================
    # VALIDATION
    # =====================================================

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

    @staticmethod
    def _resolve_columns(
        dataframe: pd.DataFrame,
        columns: list[str] | None,
    ) -> list[str]:

        if columns is None:

            return [
                column
                for column in dataframe.columns
                if dataframe[column].isna().any()
            ]

        if not isinstance(
            columns,
            list,
        ):
            raise TypeError(
                "columns must be a list or None."
            )

        unknown_columns = [
            column
            for column in columns
            if column not in dataframe.columns
        ]

        if unknown_columns:

            raise ValueError(
                "Unknown column(s): "
                + ", ".join(
                    map(
                        str,
                        unknown_columns,
                    )
                )
            )

        return list(
            columns
        )
