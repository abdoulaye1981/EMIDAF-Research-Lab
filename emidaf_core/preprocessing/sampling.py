"""
=========================================================
EMIDAF Framework
Sampling Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Méthodes d'échantillonnage.

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from sklearn.utils import resample

from .base import BasePreprocessor

# ==========================================================
# BASE
# ==========================================================

class BaseSampler(BasePreprocessor):

    """
    Classe mère.
    """

    name = "Base Sampler"

    def sample(

        self,

        X,

        y=None,

    ):

        raise NotImplementedError()
    
# ==========================================================
# RANDOM
# ==========================================================

class RandomSampling(

    BaseSampler

):

    name = "Random"

    def __init__(

        self,

        fraction=1.0,

        replace=False,

        random_state=42,

    ):

        self.fraction = fraction

        self.replace = replace

        self.random_state = random_state

    def sample(

        self,

        X,

        y=None,

    ):

        X_sample = X.sample(

            frac=self.fraction,

            replace=self.replace,

            random_state=self.random_state

        )

        if y is None:

            return X_sample

        return X_sample, y.loc[X_sample.index]

# ==========================================================
# BOOTSTRAP
# ==========================================================

class BootstrapSampling(

    BaseSampler

):

    name = "Bootstrap"

    def __init__(

        self,

        n_samples=None,

        random_state=42,

    ):

        self.n_samples = n_samples

        self.random_state = random_state

    def sample(

        self,

        X,

        y=None,

    ):

        X_boot = resample(

            X,

            replace=True,

            n_samples=self.n_samples,

            random_state=self.random_state

        )

        if y is None:

            return X_boot

        y_boot = y.loc[X_boot.index]

        return X_boot, y_boot

# ==========================================================
# BOOTSTRAP
# ==========================================================

class BootstrapSampling(

    BaseSampler

):

    name = "Bootstrap"

    def __init__(

        self,

        n_samples=None,

        random_state=42,

    ):

        self.n_samples = n_samples

        self.random_state = random_state

    def sample(

        self,

        X,

        y=None,

    ):

        X_boot = resample(

            X,

            replace=True,

            n_samples=self.n_samples,

            random_state=self.random_state

        )

        if y is None:

            return X_boot

        y_boot = y.loc[X_boot.index]

        return X_boot, y_boot

# ==========================================================
# STRATIFIED
# ==========================================================

class StratifiedSampling(

    BaseSampler

):

    name = "Stratified"

    def __init__(

        self,

        fraction=0.5,

        random_state=42,

    ):

        self.fraction = fraction

        self.random_state = random_state

    def sample(

        self,

        X,

        y,

    ):

        dataframe = X.copy()

        dataframe["_target_"] = y

        sample = (

            dataframe

            .groupby("_target_")

            .sample(

                frac=self.fraction,

                random_state=self.random_state

            )

        )

        target = sample.pop(

            "_target_"

        )

        return sample, target

# ==========================================================
# SYSTEMATIC
# ==========================================================

class SystematicSampling(

    BaseSampler

):

    name = "Systematic"

    def __init__(

        self,

        step=2,

    ):

        self.step = step

    def sample(

        self,

        X,

        y=None,

    ):

        X_sample = X.iloc[::self.step]

        if y is None:

            return X_sample

        return X_sample, y.iloc[::self.step]

# ==========================================================
# CLUSTER
# ==========================================================

class ClusterSampling(

    BaseSampler

):

    name = "Cluster"

    def sample(

        self,

        X,

        clusters,

        y=None,

    ):

        selected = np.random.choice(

            clusters.unique()

        )

        mask = clusters == selected

        if y is None:

            return X[mask]

        return X[mask], y[mask]

# ==========================================================
# WEIGHTED
# ==========================================================

class WeightedSampling(

    BaseSampler

):

    name = "Weighted"

    def sample(

        self,

        X,

        weights,

        y=None,

        fraction=1.0,

    ):

        sample = X.sample(

            frac=fraction,

            weights=weights

        )

        if y is None:

            return sample

        return sample, y.loc[sample.index]

# ==========================================================
# PERMUTATION
# ==========================================================

class PermutationSampling(

    BaseSampler

):

    name = "Permutation"

    def sample(

        self,

        X,

    ):

        return X.sample(

            frac=1

        )

# ==========================================================
# AUTO
# ==========================================================

class AutoSampling(

    BaseSampler

):

    """
    Choix automatique.

    Petit dataset

        -> Bootstrap

    Classification

        -> Stratified

    Grand dataset

        -> Random

    Séries temporelles

        -> Systematic
    """

    name = "Auto"

# ==========================================================
# SERVICE
# ==========================================================

class Sampling:

    registry = {

        "random":

            RandomSampling,

        "bootstrap":

            BootstrapSampling,

        "stratified":

            StratifiedSampling,

        "systematic":

            SystematicSampling,

        "cluster":

            ClusterSampling,

        "weighted":

            WeightedSampling,

        "permutation":

            PermutationSampling,

        "auto":

            AutoSampling

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
    def sample(

        cls,

        X,

        method="auto",

        **kwargs,

    ):

        sampler = cls.get(

            method,

            **kwargs

        )

        return sampler.sample(

            X

        )