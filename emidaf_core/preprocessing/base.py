"""
=========================================================
EMIDAF Framework
Base Preprocessing Component
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


# ==========================================================
# PREPROCESSING RESULT
# ==========================================================

@dataclass
class PreprocessingResult:
    """
    Résultat standard d'une opération de prétraitement.

    Attributes
    ----------
    step:
        Nom de l'étape exécutée.

    input_shape:
        Dimensions des données avant transformation.

    output_shape:
        Dimensions des données après transformation.

    variables:
        Variables présentes après transformation.

    statistics:
        Informations quantitatives produites par
        l'étape de prétraitement.

    metadata:
        Métadonnées complémentaires.
    """

    step: str = ""

    input_shape: tuple[int, ...] | None = None

    output_shape: tuple[int, ...] | None = None

    variables: list[str] = field(
        default_factory=list
    )

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Retourne une représentation sérialisable
        du résultat.
        """

        return {
            "step": self.step,
            "input_shape": self.input_shape,
            "output_shape": self.output_shape,
            "variables": list(self.variables),
            "statistics": dict(self.statistics),
            "metadata": dict(self.metadata),
        }

    def summary(self) -> dict[str, Any]:
        """
        Résumé synthétique du résultat.
        """

        return self.to_dict()


# ==========================================================
# MODERN BASE PREPROCESSOR
# ==========================================================

class BasePreprocessor(ABC):
    """
    Classe mère moderne des composants de prétraitement.

    Compatible avec l'architecture EMIDAF Pipeline.
    """

    name = "BasePreprocessor"

    def __init__(self):

        self.metadata: dict[str, Any] = {}

        self.fitted = False

    @abstractmethod
    def fit(
        self,
        X,
        y=None
    ):
        ...

    @abstractmethod
    def transform(
        self,
        X
    ):
        ...

    def fit_transform(
        self,
        X,
        y=None
    ):

        self.fit(
            X,
            y
        )

        return self.transform(
            X
        )

    def inverse_transform(
        self,
        X
    ):

        return X

    def get_params(self):

        return self.__dict__.copy()

    def set_params(
        self,
        **kwargs
    ):

        for key, value in kwargs.items():

            setattr(
                self,
                key,
                value
            )

        return self

    def summary(self):

        return {
            "name": self.name,
            "fitted": getattr(
                self,
                "fitted",
                False
            ),
            "parameters": self.get_params(),
        }


# ==========================================================
# COMPATIBILITY BASE
# ==========================================================

class BasePreprocessing(
    BasePreprocessor
):
    """
    Base compatible avec les composants historiques
    du moteur canonical de preprocessing.

    Cette classe maintient le contrat utilisé par les
    modules EMIDAF existants tout en reposant sur
    BasePreprocessor.

    Elle pourra être supprimée lors d'une future
    migration majeure lorsque tous les preprocessors
    utiliseront BasePreprocessor directement.
    """

    name = "BasePreprocessing"

    def __init__(
        self,
        verbose=True
    ):

        super().__init__()

        self.verbose = verbose

    def _validate_dataframe(
        self,
        X
    ) -> pd.DataFrame:
        """
        Vérifie que X est un DataFrame pandas.
        """

        if not isinstance(
            X,
            pd.DataFrame
        ):
            raise TypeError(
                "X must be a pandas DataFrame."
            )

        return X

    def _copy_dataframe(
        self,
        X
    ) -> pd.DataFrame:
        """
        Retourne une copie défensive des données.
        """

        self._validate_dataframe(X)

        return X.copy()
