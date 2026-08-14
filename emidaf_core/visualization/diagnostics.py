"""
=========================================================
EMIDAF Framework
Visualization - Statistical Diagnostics
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def acf_plot(
    data,
    column,
    lags=20,
    figsize=(10, 6),
    title=None
):

    from statsmodels.graphics.tsaplots import plot_acf

    series = data[column].dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    plot_acf(
        series,
        lags=lags,
        ax=ax
    )

    if title is None:
        title = f"ACF - {column}"

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def pacf_plot(
    data,
    column,
    lags=20,
    figsize=(10, 6),
    title=None
):

    from statsmodels.graphics.tsaplots import plot_pacf

    series = data[column].dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    plot_pacf(
        series,
        lags=lags,
        ax=ax
    )

    if title is None:
        title = f"PACF - {column}"

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def residuals_plot(
    residuals,
    figsize=(10, 6),
    title="Analyse des résidus"
):

    residuals = pd.Series(
        residuals
    ).dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        residuals
    )

    ax.axhline(
        0,
        linestyle="--"
    )

    ax.set_xlabel(
        "Observation"
    )

    ax.set_ylabel(
        "Résidu"
    )

    ax.set_title(
        title
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=residuals
    )


def residuals_histogram(
    residuals,
    bins=30,
    figsize=(10, 6),
    title="Distribution des résidus"
):

    residuals = pd.Series(
        residuals
    ).dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.hist(
        residuals,
        bins=bins
    )

    ax.set_xlabel(
        "Résidu"
    )

    ax.set_ylabel(
        "Effectif"
    )

    ax.set_title(
        title
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=residuals
    )


def residuals_qqplot(
    residuals,
    figsize=(8, 8),
    title="QQ-Plot des résidus"
):

    from scipy import stats

    residuals = pd.Series(
        residuals
    ).dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    stats.probplot(
        residuals,
        dist="norm",
        plot=ax
    )

    ax.set_title(
        title
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=residuals
    )


def residuals_acf(
    residuals,
    lags=20,
    figsize=(10, 6),
    title="ACF des résidus"
):

    from statsmodels.graphics.tsaplots import plot_acf

    residuals = pd.Series(
        residuals
    ).dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    plot_acf(
        residuals,
        lags=lags,
        ax=ax
    )

    ax.set_title(
        title
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=residuals
    )


class DiagnosticsVisualizer:

    name = "Diagnostics Visualizer"

    def __init__(
        self,
        figsize=(10, 6)
    ):

        self.figsize = figsize

    def acf(
        self,
        data,
        column,
        lags=20,
        title=None
    ):

        return acf_plot(
            data,
            column,
            lags=lags,
            figsize=self.figsize,
            title=title
        )

    def pacf(
        self,
        data,
        column,
        lags=20,
        title=None
    ):

        return pacf_plot(
            data,
            column,
            lags=lags,
            figsize=self.figsize,
            title=title
        )

    def residuals(
        self,
        residuals,
        title="Analyse des résidus"
    ):

        return residuals_plot(
            residuals,
            figsize=self.figsize,
            title=title
        )

    def residuals_histogram(
        self,
        residuals,
        bins=30,
        title="Distribution des résidus"
    ):

        return residuals_histogram(
            residuals,
            bins=bins,
            figsize=self.figsize,
            title=title
        )

    def residuals_qqplot(
        self,
        residuals,
        title="QQ-Plot des résidus"
    ):

        return residuals_qqplot(
            residuals,
            figsize=self.figsize,
            title=title
        )

    def residuals_acf(
        self,
        residuals,
        lags=20,
        title="ACF des résidus"
    ):

        return residuals_acf(
            residuals,
            lags=lags,
            figsize=self.figsize,
            title=title
        )
