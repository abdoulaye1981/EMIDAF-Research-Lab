"""
=========================================================
EMIDAF Framework
Statistics Validator
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Validation des données pour toutes les statistiques
descriptives.

Toutes les statistiques descriptives passent
obligatoirement par ce validateur.

Fonctionnalités
---------------
✓ Conversion automatique
✓ Validation des types
✓ Suppression des NaN
✓ Suppression des infinis
✓ Conversion numérique
✓ Validation DataFrame
✓ Validation Series
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


class StatisticsValidator:
    """
    Validation centralisée des données statistiques.
    """

    # =====================================================
    # SERIES
    # =====================================================

    @classmethod
    def series(
        cls,
        values: Any,
        drop_na: bool = True,
        drop_infinite: bool = True,
        numeric_only: bool = False,
    ) -> pd.Series:
        """
        Convertit une structure en Series valide.
        """

        if values is None:

            raise ValueError(
                "Values cannot be None."
            )

        if isinstance(values, pd.Series):

            series = values.copy()

        elif isinstance(values, np.ndarray):

            series = pd.Series(values)

        elif isinstance(values, list):

            series = pd.Series(values)

        elif isinstance(values, tuple):

            series = pd.Series(values)

        else:

            raise TypeError(
                f"Unsupported type: {type(values)}"
            )

        if numeric_only:

            series = pd.to_numeric(

                series,

                errors="coerce"

            )

        if drop_infinite:

            series = series.replace(

                [np.inf, -np.inf],

                np.nan

            )

        if drop_na:

            series = series.dropna()

        return series

    # =====================================================
    # DATAFRAME
    # =====================================================

    @classmethod
    def dataframe(
        cls,
        dataframe: pd.DataFrame,
        numeric_only: bool = False,
    ) -> pd.DataFrame:
        """
        Validation DataFrame.
        """

        if not isinstance(

            dataframe,

            pd.DataFrame

        ):

            raise TypeError(

                "Expected pandas DataFrame."

            )

        if dataframe.empty:

            raise ValueError(

                "Empty DataFrame."

            )

        if numeric_only:

            dataframe = dataframe.select_dtypes(

                include="number"

            )

        return dataframe.copy()

    # =====================================================
    # NUMERIC
    # =====================================================

    @classmethod
    def numeric_series(
        cls,
        values: Any,
    ) -> pd.Series:
        """
        Retourne uniquement des valeurs numériques.
        """

        return cls.series(

            values,

            numeric_only=True

        )

    # =====================================================
    # CHECKS
    # =====================================================

    @staticmethod
    def is_empty(
        values: pd.Series,
    ) -> bool:

        return len(values) == 0

    @staticmethod
    def has_missing(
        values: pd.Series,
    ) -> bool:

        return bool(

            values.isna().sum()

        )

    @staticmethod
    def has_infinite(
        values: pd.Series,
    ) -> bool:

        return bool(

            np.isinf(values).any()

        )

    @staticmethod
    def has_variance(
        values: pd.Series,
    ) -> bool:

        return values.nunique() > 1

    # =====================================================
    # INFORMATIONS
    # =====================================================

    @staticmethod
    def information(
        values: pd.Series,
    ) -> dict:

        return {

            "count": len(values),

            "missing":

                int(values.isna().sum()),

            "unique":

                int(values.nunique()),

            "dtype":

                str(values.dtype),

            "memory":

                int(

                    values.memory_usage(

                        deep=True

                    )

                )

        }

    # =====================================================
    # ASSERTIONS
    # =====================================================

    @classmethod
    def require_non_empty(
        cls,
        values: pd.Series,
    ) -> pd.Series:

        if cls.is_empty(values):

            raise ValueError(

                "Series is empty."

            )

        return values

    @classmethod
    def require_variance(
        cls,
        values: pd.Series,
    ) -> pd.Series:

        if not cls.has_variance(values):

            raise ValueError(

                "Zero variance."

            )

        return values

    @classmethod
    def require_numeric(
        cls,
        values: Any,
    ) -> pd.Series:

        values = cls.numeric_series(values)

        return cls.require_non_empty(values)