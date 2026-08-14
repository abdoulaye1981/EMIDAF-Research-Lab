"""
=========================================================
EMIDAF Framework
Feature Extraction
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Extraction et création de nouvelles variables.

=========================================================
"""

from __future__ import annotations

from abc import ABC

import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from sklearn.decomposition import TruncatedSVD

from sklearn.random_projection import (
    GaussianRandomProjection,
    SparseRandomProjection
)

from sklearn.preprocessing import PolynomialFeatures

from .base import BasePreprocessor

# ==========================================================
# BASE
# ==========================================================

class BaseFeatureExtractor(BasePreprocessor):

    """
    Classe mère.
    """

    name = "Base Feature Extractor"

    def __init__(self):

        super().__init__()

        self.extractor = None

    def fit(

        self,

        X,

        y=None,

    ):

        self.extractor.fit(

            X,

            y

        )

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        values = self.extractor.transform(

            X

        )

        columns = [

            f"{self.name}_{i+1}"

            for i

            in range(

                values.shape[1]

            )

        ]

        return pd.DataFrame(

            values,

            columns=columns,

            index=X.index

        )

    def fit_transform(

        self,

        X,

        y=None,

    ):

        self.fit(X, y)

        return self.transform(X)
    
# ==========================================================
# POLYNOMIAL
# ==========================================================

class PolynomialExtraction(

    BasePreprocessor

):

    name = "Polynomial"

    def __init__(

        self,

        degree=2,

        include_bias=False,

    ):

        super().__init__()

        self.extractor = PolynomialFeatures(

            degree=degree,

            include_bias=include_bias

        )

    def fit(

        self,

        X,

        y=None,

    ):

        self.extractor.fit(X)

        self.columns = (

            self.extractor

            .get_feature_names_out(

                X.columns

            )

        )

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        values = self.extractor.transform(X)

        return pd.DataFrame(

            values,

            columns=self.columns,

            index=X.index

        )
# ==========================================================
# PCA
# ==========================================================

class PCAExtraction(

    BaseFeatureExtractor

):

    name = "PCA"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.extractor = PCA(

            n_components=n_components

        )

# ==========================================================
# ICA
# ==========================================================

class ICAExtraction(

    BaseFeatureExtractor

):

    name = "ICA"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.extractor = FastICA(

            n_components=n_components,

            random_state=42

        )

# ==========================================================
# SVD
# ==========================================================

class SVDExtraction(

    BaseFeatureExtractor

):

    name = "SVD"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.extractor = TruncatedSVD(

            n_components=n_components,

            random_state=42

        )

# ==========================================================
# GAUSSIAN PROJECTION
# ==========================================================

class GaussianProjection(

    BaseFeatureExtractor

):

    name = "Gaussian Projection"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.extractor = (

            GaussianRandomProjection(

                n_components=n_components,

                random_state=42

            )

        )

# ==========================================================
# SPARSE PROJECTION
# ==========================================================

class SparseProjection(

    BaseFeatureExtractor

):

    name = "Sparse Projection"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.extractor = (

            SparseRandomProjection(

                n_components=n_components,

                random_state=42

            )

        )

# ==========================================================
# AUTO
# ==========================================================

class AutoFeatureExtraction(

    BasePreprocessor

):

    """
    Choix automatique.

    Peu de variables
        -> Polynomial

    Forte corrélation
        -> PCA

    Variables indépendantes
        -> ICA

    Très haute dimension
        -> Random Projection
    """

# ==========================================================
# SERVICE
# ==========================================================

class FeatureExtraction:

    registry = {

        "polynomial":

            PolynomialExtraction,

        "pca":

            PCAExtraction,

        "ica":

            ICAExtraction,

        "svd":

            SVDExtraction,

        "gaussian":

            GaussianProjection,

        "sparse":

            SparseProjection,

        "auto":

            AutoFeatureExtraction

    }

    @classmethod
    def get(

        cls,

        method,

        **kwargs,

    ):

        return cls.registry[method](

            **kwargs

        )

    @classmethod
    def fit_transform(

        cls,

        X,

        method="auto",

        **kwargs,

    ):

        extractor = cls.get(

            method,

            **kwargs

        )

        return extractor.fit_transform(

            X

        )