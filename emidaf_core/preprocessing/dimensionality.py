"""
=========================================================
EMIDAF Framework
Dimensionality Reduction Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Réduction de dimension.

=========================================================
"""

from __future__ import annotations

from abc import ABC

import pandas as pd

from sklearn.decomposition import (
    PCA,
    IncrementalPCA,
    KernelPCA,
    SparsePCA,
    MiniBatchSparsePCA,
    TruncatedSVD,
    FastICA,
    FactorAnalysis,
    NMF
)

from sklearn.manifold import (
    Isomap,
    LocallyLinearEmbedding,
    MDS,
    SpectralEmbedding,
    TSNE
)

from .base import BasePreprocessor

# ==========================================================
# BASE
# ==========================================================

class BaseDimensionalityReduction(BasePreprocessor):

    """
    Classe mère.
    """

    name = "BaseDimensionality"

    def __init__(self):

        super().__init__()

        self.model = None

    def fit(self, X, y=None):

        self.model.fit(X)

        self.fitted = True

        return self

    def transform(self, X):

        values = self.model.transform(X)

        columns = [

            f"{self.name}_{i+1}"

            for i in range(values.shape[1])

        ]

        return pd.DataFrame(

            values,

            columns=columns,

            index=X.index

        )

    def fit_transform(self, X, y=None):

        self.fit(X)

        return self.transform(X)
    
# ==========================================================
# PCA
# ==========================================================

class PCAReduction(BaseDimensionalityReduction):

    name = "PCA"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.model = PCA(

            n_components=n_components

        )

# ==========================================================
# INCREMENTAL PCA
# ==========================================================

class IncrementalPCAReduction(

    BaseDimensionalityReduction

):

    name = "Incremental PCA"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.model = IncrementalPCA(

            n_components=n_components

        )

# ==========================================================
# KERNEL PCA
# ==========================================================

class KernelPCAReduction(

    BaseDimensionalityReduction

):

    name = "Kernel PCA"

    def __init__(

        self,

        n_components=2,

        kernel="rbf",

    ):

        super().__init__()

        self.model = KernelPCA(

            n_components=n_components,

            kernel=kernel

        )

# ==========================================================
# ICA
# ==========================================================

class ICAReduction(

    BaseDimensionalityReduction

):

    name = "ICA"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.model = FastICA(

            n_components=n_components,

            random_state=42

        )

# ==========================================================
# SVD
# ==========================================================

class SVDReduction(

    BaseDimensionalityReduction

):

    name = "Truncated SVD"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.model = TruncatedSVD(

            n_components=n_components,

            random_state=42

        )

# ==========================================================
# FACTOR ANALYSIS
# ==========================================================

class FactorAnalysisReduction(

    BaseDimensionalityReduction

):

    name = "Factor Analysis"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.model = FactorAnalysis(

            n_components=n_components

        )

# ==========================================================
# NMF
# ==========================================================

class NMFReduction(

    BaseDimensionalityReduction

):

    name = "NMF"

    def __init__(

        self,

        n_components=2,

    ):

        super().__init__()

        self.model = NMF(

            n_components=n_components,

            init="nndsvda",

            random_state=42

        )

# ==========================================================
# TSNE
# ==========================================================

class TSNEReduction(

    BasePreprocessor

):

    """
    t-SNE n'accepte pas transform().
    """

    name = "t-SNE"

    def __init__(

        self,

        n_components=2,
        perplexity=30.0,

    ):

        self.model = TSNE(

            n_components=n_components,
            perplexity=float(perplexity),

            random_state=42

        )

    def fit(

        self,

        X,

        y=None,

    ):

        self.embedding = self.model.fit_transform(X)

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        return pd.DataFrame(

            self.embedding,

            columns=[

                "TSNE1",

                "TSNE2"

            ],

            index=X.index

        )

# ==========================================================
# AUTO
# ==========================================================

class AutoDimensionalityReduction(

    BasePreprocessor

):

    """
    Choix automatique.

    <100 variables
        -> PCA

    >1000 variables
        -> TruncatedSVD

    Données non linéaires
        -> Kernel PCA

    Visualisation
        -> t-SNE
    """

# ==========================================================
# SERVICE
# ==========================================================

class Dimensionality:

    registry = {

        "pca": PCAReduction,

        "incremental_pca": IncrementalPCAReduction,

        "kernel_pca": KernelPCAReduction,

        "ica": ICAReduction,

        "svd": SVDReduction,

        "factor_analysis": FactorAnalysisReduction,

        "nmf": NMFReduction,

        "tsne": TSNEReduction,

        "auto": AutoDimensionalityReduction

    }

    @classmethod
    def get(

        cls,

        method,

        **kwargs,

    ):

        return cls.registry[method](**kwargs)

    @classmethod
    def fit_transform(

        cls,

        X,

        method="auto",

        **kwargs,

    ):

        model = cls.get(

            method,

            **kwargs

        )

        return model.fit_transform(X)
