"""
=========================================================
EMIDAF Framework
Visualization - Statistical Distributions
=========================================================
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from .base import VisualizationResult


def histogram(
    data,
    column,
    bins=30,
    figsize=(10, 6),
    title=None
):

    series = data[column].dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.hist(
        series,
        bins=bins
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Effectif")

    if title is None:
        title = f"Distribution de {column}"

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def empirical_cdf(
    data,
    column,
    figsize=(10, 6),
    title=None
):

    series = (
        data[column]
        .dropna()
        .sort_values()
    )

    y = np.arange(
        1,
        len(series) + 1
    ) / len(series)

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.step(
        series,
        y,
        where="post"
    )

    ax.set_xlabel(column)
    ax.set_ylabel(
        "F(x)"
    )

    if title is None:
        title = (
            f"Fonction de répartition empirique - {column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    result_data = {
        "x": series.to_numpy(),
        "F_x": y
    }

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=result_data
    )


def qqplot(
    data,
    column,
    figsize=(8, 8),
    title=None
):

    from scipy import stats

    series = data[column].dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    stats.probplot(
        series,
        dist="norm",
        plot=ax
    )

    if title is None:
        title = (
            f"QQ-Plot de {column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def distribution_comparison(
    data,
    columns,
    bins=30,
    figsize=(10, 6),
    title=None
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    for column in columns:

        series = data[column].dropna()

        ax.hist(
            series,
            bins=bins,
            alpha=0.5,
            label=column
        )

    ax.set_xlabel(
        "Valeur"
    )

    ax.set_ylabel(
        "Effectif"
    )

    if title is None:
        title = "Comparaison des distributions"

    ax.set_title(title)

    ax.legend()

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=data[columns].copy()
    )


def boxplot_distribution(
    data,
    columns,
    figsize=(10, 6),
    title=None
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    values = [
        data[column]
        .dropna()
        .values
        for column in columns
    ]

    ax.boxplot(
        values,
        labels=columns
    )

    ax.set_ylabel(
        "Valeur"
    )

    if title is None:
        title = "Comparaison des distributions"

    ax.set_title(title)

    ax.tick_params(
        axis="x",
        rotation=45
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=data[columns].copy()
    )


def probability_histogram(
    data,
    column,
    bins=30,
    figsize=(10, 6),
    title=None
):

    series = data[column].dropna()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    weights = np.ones(
        len(series)
    ) / len(series)

    ax.hist(
        series,
        bins=bins,
        weights=weights
    )

    ax.set_xlabel(
        column
    )

    ax.set_ylabel(
        "Probabilité"
    )

    if title is None:
        title = (
            f"Histogramme probabiliste - {column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


class DistributionVisualizer:

    name = "Distribution Visualizer"

    def __init__(
        self,
        figsize=(10, 6)
    ):

        self.figsize = figsize

    def histogram(
        self,
        data,
        column,
        bins=30,
        title=None
    ):

        return histogram(
            data,
            column,
            bins=bins,
            figsize=self.figsize,
            title=title
        )

    def empirical_cdf(
        self,
        data,
        column,
        title=None
    ):

        return empirical_cdf(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def qqplot(
        self,
        data,
        column,
        title=None
    ):

        return qqplot(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def distribution_comparison(
        self,
        data,
        columns,
        bins=30,
        title=None
    ):

        return distribution_comparison(
            data,
            columns,
            bins=bins,
            figsize=self.figsize,
            title=title
        )

    def boxplot_distribution(
        self,
        data,
        columns,
        title=None
    ):

        return boxplot_distribution(
            data,
            columns,
            figsize=self.figsize,
            title=title
        )

    def probability_histogram(
        self,
        data,
        column,
        bins=30,
        title=None
    ):

        return probability_histogram(
            data,
            column,
            bins=bins,
            figsize=self.figsize,
            title=title
        )
