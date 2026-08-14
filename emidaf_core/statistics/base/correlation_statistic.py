"""
=========================================================
EMIDAF Framework
Correlation Statistic
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe de base de toutes les corrélations EMIDAF.

Exemples
---------
Pearson
Spearman
Kendall
PointBiserial
Biserial
CorrelationRatio
CramerV
PhiCoefficient
MutualInformation
DistanceCorrelation
=========================================================
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

import pandas as pd

from .base_statistic import BaseStatistic


class CorrelationStatistic(BaseStatistic):
    """
    Classe abstraite de toutes les corrélations.

    Fournit :

    - validation automatique
    - validation de deux variables
    - validation DataFrame
    - calcul sécurisé
    - création standardisée des résultats
    """

    category: str = "Correlation"

    # =====================================================
    # API
    # =====================================================

    @classmethod
    @abstractmethod
    def compute(
        cls,
        x: Any,
        y: Any,
        **kwargs,
    ) -> dict:
        """
        Calcule une corrélation.

        Returns
        -------
        dict
        """

        raise NotImplementedError

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def validate_pair(
        cls,
        x: Any,
        y: Any,
    ) -> tuple[pd.Series, pd.Series]:
        """
        Valide deux variables.
        """

        x = cls.validate(x)
        y = cls.validate(y)

        if len(x) != len(y):

            raise ValueError(

                "Variables must have the same length."

            )

        if len(x) == 0:

            raise ValueError(

                "Empty variables."

            )

        return x, y

    @classmethod
    def validate_dataframe(
        cls,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Valide un DataFrame.
        """

        if dataframe.empty:

            raise ValueError(

                "Empty DataFrame."

            )

        return dataframe

    # =====================================================
    # Matrix
    # =====================================================

    @classmethod
    def compute_matrix(
        cls,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcule une matrice de corrélations.

        Cette méthode doit être redéfinie
        si nécessaire.
        """

        dataframe = cls.validate_dataframe(

            dataframe

        )

        matrix = pd.DataFrame(

            index=dataframe.columns,

            columns=dataframe.columns,

            dtype=float

        )

        columns = dataframe.columns.tolist()

        for i, col1 in enumerate(columns):

            for j, col2 in enumerate(columns):

                if j < i:

                    matrix.loc[col1, col2] = matrix.loc[col2, col1]

                    continue

                result = cls.compute(

                    dataframe[col1],

                    dataframe[col2]

                )

                matrix.loc[col1, col2] = result["coefficient"]

        return matrix

    # =====================================================
    # Result
    # =====================================================

    @classmethod
    def build_result(
        cls,
        coefficient: float,
        p_value: float | None = None,
        method: str | None = None,
        **extra,
    ) -> dict:
        """
        Construit un résultat standard.
        """

        result = {

            "method": method or cls.name,

            "category": cls.category,

            "coefficient": float(coefficient)

        }

        if p_value is not None:

            result["p_value"] = float(

                p_value

            )

        result.update(extra)

        return result

    # =====================================================
    # Safe Compute
    # =====================================================

    @classmethod
    def safe_compute(
        cls,
        x,
        y,
        default=None,
        **kwargs,
    ):
        """
        Calcul sécurisé.
        """

        try:

            return cls.compute(

                x,

                y,

                **kwargs

            )

        except Exception:

            return default

    # =====================================================
    # Strength
    # =====================================================

    @classmethod
    def strength(
        cls,
        coefficient: float,
    ) -> str:
        """
        Interprétation de la force
        de corrélation.
        """

        value = abs(coefficient)

        if value < 0.20:

            return "Very Weak"

        if value < 0.40:

            return "Weak"

        if value < 0.60:

            return "Moderate"

        if value < 0.80:

            return "Strong"

        return "Very Strong"

    # =====================================================
    # Direction
    # =====================================================

    @classmethod
    def direction(
        cls,
        coefficient: float,
    ) -> str:
        """
        Direction de la corrélation.
        """

        if coefficient > 0:

            return "Positive"

        if coefficient < 0:

            return "Negative"

        return "Null"

    # =====================================================
    # Information
    # =====================================================

    @classmethod
    def info(cls) -> dict:
        """
        Métadonnées.
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