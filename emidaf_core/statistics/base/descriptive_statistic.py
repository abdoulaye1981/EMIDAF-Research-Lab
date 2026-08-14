"""
=========================================================
EMIDAF Framework
Descriptive Statistic
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe de base des statistiques descriptives.

Toutes les statistiques descriptives héritent de cette
classe.

Exemples
---------
Mean
Median
Mode
Variance
StandardDeviation
IQR
MAD
Skewness
Kurtosis
Entropy
=========================================================
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

import numpy as np
import pandas as pd

from .base_statistic import BaseStatistic


class DescriptiveStatistic(BaseStatistic):
    """
    Classe mère de toutes les statistiques descriptives.

    Cette classe ajoute plusieurs fonctionnalités :

    - calcul sécurisé
    - validation automatique
    - calcul dataframe
    - calcul colonne par colonne
    - conversion des résultats
    """

    category: str = "Descriptive"

    # =====================================================
    # API
    # =====================================================

    @classmethod
    @abstractmethod
    def compute(
        cls,
        values: Any,
    ):
        """
        Calcule une statistique descriptive.

        Parameters
        ----------
        values :
            pandas Series
            numpy array
            list

        Returns
        -------
        float | dict
        """

        raise NotImplementedError

    # =====================================================
    # DataFrame
    # =====================================================

    @classmethod
    def compute_dataframe(
        cls,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calcule la statistique sur toutes les colonnes
        numériques d'un DataFrame.

        Returns
        -------
        dict
        """

        results = {}

        numeric = dataframe.select_dtypes(
            include="number"
        )

        for column in numeric.columns:

            results[column] = cls.compute(

                numeric[column]

            )

        return results

    # =====================================================
    # Multiple Series
    # =====================================================

    @classmethod
    def compute_many(
        cls,
        series: dict[str, pd.Series],
    ) -> dict:
        """
        Calcule plusieurs séries.

        Parameters
        ----------
        series : dict

        Returns
        -------
        dict
        """

        results = {}

        for name, values in series.items():

            results[name] = cls.compute(values)

        return results

    # =====================================================
    # Summary
    # =====================================================

    @classmethod
    def summary(
        cls,
        values: Any,
    ) -> dict:
        """
        Retourne un résumé complet.
        """

        values = cls.validate(values)

        return {

            "statistic": cls.name,

            "category": cls.category,

            "count": cls.size(values),

            "unique": cls.unique(values),

            "missing": cls.missing(values),

            "value": cls.compute(values)

        }

    # =====================================================
    # Safe Compute
    # =====================================================

    @classmethod
    def safe_compute(
        cls,
        values: Any,
        default=np.nan,
    ):
        """
        Calcul sécurisé.

        En cas d'erreur, retourne default.
        """

        try:

            return cls.compute(values)

        except Exception:

            return default

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def require_variance(
        cls,
        values: Any,
    ) -> pd.Series:
        """
        Vérifie qu'une variance peut être calculée.
        """

        values = cls.validate(values)

        if cls.is_empty(values):

            raise ValueError(

                "Empty series."

            )

        if not cls.has_variance(values):

            raise ValueError(

                "Series has zero variance."

            )

        return values

    @classmethod
    def require_non_empty(
        cls,
        values: Any,
    ) -> pd.Series:
        """
        Vérifie que la série n'est pas vide.
        """

        values = cls.validate(values)

        if cls.is_empty(values):

            raise ValueError(

                "Empty series."

            )

        return values

    # =====================================================
    # Information
    # =====================================================

    @classmethod
    def info(cls) -> dict:
        """
        Informations sur la statistique.
        """

        return {

            "name": cls.name,

            "description": cls.description,

            "category": cls.category,

            "version": cls.version

        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"category='{self.category}')"

        )

    def __str__(self):

        return self.__repr__()