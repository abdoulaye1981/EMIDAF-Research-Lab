"""
=========================================================
EMIDAF Framework
Distribution Visualization
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Visualisation des distributions.

=========================================================
"""

from __future__ import annotations

import numpy as np

import matplotlib.pyplot as plt

from scipy.stats import probplot

from statsmodels.distributions.empirical_distribution import ECDF

from .continuous import Continuous


class DistributionVisualization:

    """
    Visualisation des distributions.
    """

    # =====================================================
    # Histogramme + PDF
    # =====================================================

    @staticmethod
    def histogram(

        values,

        distribution="normal",

        bins=30,

        density=True,

        figsize=(8,5),

    ):

        model = Continuous.get(

            distribution

        )

        params = model.fit(values)

        x = np.linspace(

            np.min(values),

            np.max(values),

            500

        )

        y = model.pdf(

            x,

            *params

        )

        plt.figure(

            figsize=figsize

        )

        plt.hist(

            values,

            bins=bins,

            density=density,

            alpha=.6,

            label="Data"

        )

        plt.plot(

            x,

            y,

            linewidth=3,

            label=distribution

        )

        plt.legend()

        plt.title(

            "Histogram + PDF"

        )

        plt.show()

    # =====================================================
    # PDF
    # =====================================================

    @staticmethod
    def pdf(

        distribution,

        *params,

        xmin=-5,

        xmax=5,

    ):

        model = Continuous.get(

            distribution

        )

        x = np.linspace(

            xmin,

            xmax,

            1000

        )

        y = model.pdf(

            x,

            *params

        )

        plt.figure(

            figsize=(8,5)

        )

        plt.plot(

            x,

            y

        )

        plt.title(

            f"PDF : {distribution}"

        )

        plt.show()

    # =====================================================
    # CDF
    # =====================================================

    @staticmethod
    def cdf(

        distribution,

        *params,

        xmin=-5,

        xmax=5,

    ):

        model = Continuous.get(

            distribution

        )

        x = np.linspace(

            xmin,

            xmax,

            1000

        )

        y = model.cdf(

            x,

            *params

        )

        plt.figure(

            figsize=(8,5)

        )

        plt.plot(

            x,

            y

        )

        plt.title(

            f"CDF : {distribution}"

        )

        plt.show()

    # =====================================================
    # QQ Plot
    # =====================================================

    @staticmethod
    def qqplot(

        values,

    ):

        plt.figure(

            figsize=(6,6)

        )

        probplot(

            values,

            dist="norm",

            plot=plt

        )

        plt.title(

            "QQ Plot"

        )

        plt.show()

    # =====================================================
    # ECDF
    # =====================================================

    @staticmethod
    def ecdf(

        values,

    ):

        estimator = ECDF(

            values

        )

        plt.figure(

            figsize=(8,5)

        )

        plt.step(

            estimator.x,

            estimator.y

        )

        plt.title(

            "Empirical CDF"

        )

        plt.show()

    # =====================================================
    # Survival Function
    # =====================================================

    @staticmethod
    def survival(

        distribution,

        *params,

        xmin=-5,

        xmax=5,

    ):

        model = Continuous.get(

            distribution

        )

        x = np.linspace(

            xmin,

            xmax,

            1000

        )

        y = model.sf(

            x,

            *params

        )

        plt.figure(

            figsize=(8,5)

        )

        plt.plot(

            x,

            y

        )

        plt.title(

            "Survival Function"

        )

        plt.show()

    # =====================================================
    # PPF
    # =====================================================

    @staticmethod
    def quantile(

        distribution,

        *params,

    ):

        model = Continuous.get(

            distribution

        )

        q = np.linspace(

            0.001,

            0.999,

            1000

        )

        x = model.ppf(

            q,

            *params

        )

        plt.figure(

            figsize=(8,5)

        )

        plt.plot(

            q,

            x

        )

        plt.title(

            "Quantile Function"

        )

        plt.show()

    # =====================================================
    # Comparaison
    # =====================================================

    @staticmethod
    def compare(

        values,

        distributions,

    ):

        plt.figure(

            figsize=(10,6)

        )

        plt.hist(

            values,

            bins=30,

            density=True,

            alpha=.40

        )

        x = np.linspace(

            np.min(values),

            np.max(values),

            500

        )

        for distribution in distributions:

            model = (

                Continuous.get(

                    distribution

                )

            )

            params = model.fit(values)

            y = model.pdf(

                x,

                *params

            )

            plt.plot(

                x,

                y,

                label=distribution

            )

        plt.legend()

        plt.title(

            "Distribution Comparison"

        )

        plt.show()