"""
=========================================================
EMIDAF Framework
Random Sampling Methods
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

import pandas as pd

from scipy.stats import qmc

# ==========================================================
# RANDOM SAMPLING
# ==========================================================

class RandomSampling:

    """
    Random sampling engine.
    """

    def __init__(

        self,

        random_state=None,

    ):

        self.random_state=random_state

        self.rng=np.random.default_rng(

            random_state

        )

    # ==========================================================
# SIMPLE RANDOM
# ==========================================================

    def simple(

        self,

        data,

        n,

        replace=False,

    ):

        if isinstance(

            data,

            pd.DataFrame

        ):

            return data.sample(

                n=n,

                replace=replace,

                random_state=self.random_state

            )

        index=self.rng.choice(

            len(data),

            size=n,

            replace=replace

        )

        return np.asarray(

            data

        )[index]


    # ==========================================================
# BOOTSTRAP
# ==========================================================

    def bootstrap(

        self,

        data,

        n=None,

    ):

        if n is None:

            n=len(data)

        index=self.rng.choice(

            len(data),

            size=n,

            replace=True

        )

        if isinstance(

            data,

            pd.DataFrame

        ):

            return data.iloc[index]

        return np.asarray(

            data

        )[index]


    # ==========================================================
# STRATIFIED
# ==========================================================

    def stratified(

        self,

        dataframe,

        strata,

        frac=0.20,

    ):

        return (

            dataframe

            .groupby(strata,group_keys=False)

            .apply(

                lambda x:

                x.sample(

                    frac=frac,

                    random_state=self.random_state

                )

            )

        )

    # ==========================================================
# SYSTEMATIC
# ==========================================================

    def systematic(

        self,

        data,

        step,

    ):

        data=np.asarray(

            data

        )

        start=self.rng.integers(

            0,

            step

        )

        return data[

            start::step

        ]

    # ==========================================================
# WEIGHTED
# ==========================================================

    def weighted(

        self,

        data,

        weights,

        n,

        replace=True,

    ):

        index=self.rng.choice(

            len(data),

            size=n,

            replace=replace,

            p=np.asarray(weights)/np.sum(weights)

        )

        return np.asarray(

            data

        )[index]


    # ==========================================================
# CLUSTER
# ==========================================================

    def cluster(

        self,

        dataframe,

        cluster_column,

        n_clusters,

    ):

        clusters=self.rng.choice(

            dataframe[cluster_column].unique(),

            size=n_clusters,

            replace=False

        )

        return dataframe[

            dataframe[cluster_column].isin(

                clusters

            )

        ]

    # ==========================================================
# LATIN HYPERCUBE
# ==========================================================

    def latin_hypercube(

        self,

        dimension,

        samples,

    ):

        sampler=qmc.LatinHypercube(

            d=dimension,

            seed=self.random_state

        )

        return sampler.random(

            samples

        )

    # ==========================================================
# SOBOL
# ==========================================================

    def sobol(

        self,

        dimension,

        samples,

    ):

        sampler=qmc.Sobol(

            d=dimension,

            scramble=True,

            seed=self.random_state

        )

        return sampler.random(

            samples

        )

    # ==========================================================
# HALTON
# ==========================================================

    def halton(

        self,

        dimension,

        samples,

    ):

        sampler=qmc.Halton(

            d=dimension,

            seed=self.random_state

        )

        return sampler.random(

            samples

        )

    # ==========================================================
# MONTE CARLO
# ==========================================================

    def monte_carlo(

        self,

        dimension,

        samples,

    ):

        return self.rng.random(

            (

                samples,

                dimension

            )

        )

# ==========================================================
# SERVICE
# ==========================================================

Sampling=RandomSampling