"""
=========================================================
EMIDAF Framework
Visualization - Univariate Analysis
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def histogram(
    data,
    column,
    bins=30,
    figsize=(10, 6),
    title=None,
    kde=False
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    series = data[column].dropna()

    ax.hist(
        series,
        bins=bins,
        density=kde
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Fréquence")

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Histogramme de {column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def boxplot(
    data,
    column,
    figsize=(8, 6),
    title=None
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    series = data[column].dropna()

    ax.boxplot(
        series
    )

    ax.set_ylabel(column)

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Boxplot de {column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def barplot(
    data,
    column,
    figsize=(10, 6),
    title=None,
    rotation=45
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    counts = (
        data[column]
        .value_counts(
            dropna=False
        )
    )

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Effectif")
    ax.tick_params(
        axis="x",
        rotation=rotation
    )

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Barplot de {column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=counts
    )


def piechart(
    data,
    column,
    figsize=(8, 8),
    title=None,
    autopct="%1.1f%%"
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    counts = (
        data[column]
        .value_counts(
            dropna=False
        )
    )

    counts.plot(
        kind="pie",
        ax=ax,
        autopct=autopct
    )

    ax.set_ylabel("")

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Répartition de {column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=counts
    )


def density(
    data,
    column,
    figsize=(10, 6),
    title=None
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    series = data[column].dropna()

    series.plot(
        kind="density",
        ax=ax
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Densité")

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Densité de {column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def frequency_table(
    data,
    column
):

    counts = (
        data[column]
        .value_counts(
            dropna=False
        )
    )

    frequencies = (
        data[column]
        .value_counts(
            normalize=True,
            dropna=False
        )
    )

    return pd.DataFrame({
        "effectif": counts,
        "frequence": frequencies,
        "pourcentage":
            frequencies * 100
    })


class UnivariateVisualizer:

    name = "Univariate Visualizer"

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

    def boxplot(
        self,
        data,
        column,
        title=None
    ):

        return boxplot(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def barplot(
        self,
        data,
        column,
        title=None,
        rotation=45
    ):

        return barplot(
            data,
            column,
            figsize=self.figsize,
            title=title,
            rotation=rotation
        )

    def piechart(
        self,
        data,
        column,
        title=None
    ):

        return piechart(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def density(
        self,
        data,
        column,
        title=None
    ):

        return density(
            data,
            column,
            figsize=self.figsize,
            title=title
        )
