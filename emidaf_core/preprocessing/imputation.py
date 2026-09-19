"""
=========================================================
EMIDAF Framework
Missing Values Imputation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Toutes les méthodes d'imputation.

=========================================================
"""
from __future__ import annotations
from abc import ABC
from abc import abstractmethod
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.experimental import enable_iterative_imputer
from ..common.results import CleaningResult
from .base import BasePreprocessor

class BaseImputer(BasePreprocessor, ABC):
    """
    Classe mère de tous les imputeurs.
    """
    name = 'BaseImputer'
    strategy = ''

    def __init__(self):
        super().__init__()
        self.imputer = None

    def fit(self, X, y=None):
        self.imputer.fit(X)
        self.fitted = True
        return self

    def transform(self, X):
        values = self.imputer.transform(X)
        return pd.DataFrame(values, columns=X.columns, index=X.index)

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def report(self, before, after):
        return CleaningResult(operation='Imputation', strategy=self.strategy, initial_rows=len(before), final_rows=len(after), initial_columns=before.shape[1], final_columns=after.shape[1], affected_columns=list(before.columns))

class MeanImputer(BaseImputer):
    name = 'Mean'
    strategy = 'mean'

    def __init__(self):
        super().__init__()
        self.imputer = SimpleImputer(strategy='mean')

class MedianImputer(BaseImputer):
    name = 'Median'
    strategy = 'median'

    def __init__(self):
        super().__init__()
        self.imputer = SimpleImputer(strategy='median')

class ModeImputer(BaseImputer):
    name = 'Most Frequent'
    strategy = 'most_frequent'

    def __init__(self):
        super().__init__()
        self.imputer = SimpleImputer(strategy='most_frequent')

class ConstantImputer(BaseImputer):
    name = 'Constant'
    strategy = 'constant'

    def __init__(self, value=0):
        super().__init__()
        self.imputer = SimpleImputer(strategy='constant', fill_value=value)

class KNNMissingImputer(BaseImputer):
    name = 'KNN'
    strategy = 'knn'

    def __init__(self, n_neighbors=5):
        super().__init__()
        self.imputer = KNNImputer(n_neighbors=n_neighbors)

class MICEImputer(BaseImputer):
    name = 'MICE'
    strategy = 'iterative'

    def __init__(self, random_state=42):
        super().__init__()
        self.imputer = IterativeImputer(random_state=random_state)
import numpy as np

class RandomSampleImputer(BasePreprocessor):
    name = 'Random Sample'

    def fit(self, X, y=None):
        self.statistics = {}
        for column in X.columns:
            self.statistics[column] = X[column].dropna().values
        self.fitted = True
        return self

    def transform(self, X):
        X = X.copy()
        rng = np.random.default_rng()
        for column in X.columns:
            mask = X[column].isna()
            if mask.any():
                X.loc[mask, column] = rng.choice(self.statistics[column], size=mask.sum(), replace=True)
        return X

class EMImputer(BasePreprocessor):
    """
    EM Algorithm.

    Version 1.0 :
    wrapper futur.
    """
    name = 'Expectation Maximization'

    def fit(self, X, y=None):
        raise NotImplementedError('Disponible dans EMIDAF 2.0')

class Imputation:
    """
    API publique.
    """
    registry = {'mean': MeanImputer, 'median': MedianImputer, 'mode': ModeImputer, 'constant': ConstantImputer, 'knn': KNNMissingImputer, 'mice': MICEImputer, 'random': RandomSampleImputer, 'em': EMImputer}

    @classmethod
    def get(cls, strategy, **kwargs):
        return cls.registry[strategy](**kwargs)

    @classmethod
    def fit_transform(cls, dataframe, strategy='mean', **kwargs):
        model = cls.get(strategy, **kwargs)
        return model.fit_transform(dataframe)
