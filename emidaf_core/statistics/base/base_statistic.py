"""
=========================================================
EMIDAF Framework
Base Statistic
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe mère de toutes les statistiques EMIDAF.

Toutes les statistiques du framework héritent de cette
classe.

Exemple :

    class Mean(BaseStatistic):
        ...

    class Pearson(BaseStatistic):
        ...

    class Shapiro(BaseStatistic):
        ...
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Iterable

import numpy as np
import pandas as pd


class BaseStatistic(ABC):
    """
    Classe abstraite représentant une statistique.

    Toutes les statistiques EMIDAF héritent de cette classe.

    Elle fournit :

    - validation des données
    - nettoyage
    - conversion automatique
    - suppression des NaN
    - suppression des infinis
    - méthodes utilitaires
    """

    # =====================================================
    # Metadata
    # =====================================================

    name: str = ""

    description: str = ""

    category: str = ""

    version: str = "1.0.0"

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def validate(
        cls,
        values: Any,
        drop_na: bool = True,
        drop_infinite: bool = True,
    ) -> pd.Series:
        """
        Valide une série de données.

        Parameters
        ----------
        values :
            pandas Series
            numpy array
            list
            tuple

        Returns
        -------
        pandas.Series
        """

        if values is None:

            raise ValueError(

                "Values cannot be None."

            )

        if isinstance(values, pd.Series):

            series = values.copy()

        elif isinstance(values, np.ndarray):

            series = pd.Series(values)

        elif isinstance(values, (list, tuple)):

            series = pd.Series(values)

        else:

            raise TypeError(

                f"Unsupported type : {type(values)}"

            )

        if drop_na:

            series = series.dropna()

        if drop_infinite:

            series = series.replace(

                [np.inf, -np.inf],

                np.nan

            ).dropna()

        return series

    # =====================================================
    # Utilities
    # =====================================================

    @classmethod
    def is_empty(
        cls,
        values: pd.Series,
    ) -> bool:
        """
        Vérifie si la série est vide.
        """

        return len(values) == 0

    @classmethod
    def size(
        cls,
        values: pd.Series,
    ) -> int:
        """
        Taille.
        """

        return len(values)

    @classmethod
    def unique(
        cls,
        values: pd.Series,
    ) -> int:
        """
        Nombre de valeurs uniques.
        """

        return int(

            values.nunique()

        )

    @classmethod
    def missing(
        cls,
        values: pd.Series,
    ) -> int:
        """
        Nombre de valeurs manquantes.
        """

        return int(

            values.isna().sum()

        )

    @classmethod
    def has_missing(
        cls,
        values: pd.Series,
    ) -> bool:
        """
        Présence de valeurs manquantes.
        """

        return cls.missing(values) > 0

    @classmethod
    def has_infinite(
        cls,
        values: pd.Series,
    ) -> bool:
        """
        Présence de valeurs infinies.
        """

        return bool(

            np.isinf(values).any()

        )

    @classmethod
    def has_variance(
        cls,
        values: pd.Series,
    ) -> bool:
        """
        Vérifie que la variance existe.
        """

        return values.nunique() > 1

    @classmethod
    def as_numpy(
        cls,
        values: pd.Series,
    ) -> np.ndarray:
        """
        Conversion numpy.
        """

        return values.to_numpy()

    @classmethod
    def nan(cls):

        return np.nan

    # =====================================================
    # Compute
    # =====================================================

    @classmethod
    @abstractmethod
    def compute(
        cls,
        values: Any,
    ):
        """
        Calcul principal.

        Toutes les statistiques doivent
        implémenter cette méthode.
        """

        raise NotImplementedError

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"category='{self.category}', "

            f"version='{self.version}')"

        )

    def __str__(self):

        return self.__repr__()