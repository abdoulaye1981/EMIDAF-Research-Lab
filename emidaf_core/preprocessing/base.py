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

from abc import ABC
from abc import abstractmethod

import pandas as pd


class BasePreprocessor(ABC):
    """
    Classe mère de tous les composants de prétraitement.
    Compatible avec l'architecture EMIDAF Pipeline.
    """

    name = "BasePreprocessor"

    fitted = False

    def __init__(self):

        self.metadata = {}

    @abstractmethod
    def fit(self, X, y=None):
        ...

    @abstractmethod
    def transform(self, X):
        ...

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)

    def inverse_transform(self, X):

        return X

    def get_params(self):

        return self.__dict__

    def set_params(self, **kwargs):

        for key, value in kwargs.items():

            setattr(self, key, value)

        return self

    def summary(self):

        return {

            "name": self.name,

            "fitted": self.fitted,

            "parameters": self.get_params()

        }