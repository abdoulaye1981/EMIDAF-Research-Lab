"""
=========================================================
EMIDAF Framework
Visualization - Bivariate Analysis
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def scatterplot(
    data,
    x,
    y,
    figsize=(10, 6),
    title=None
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.scatter(
        data[x],
        data[y]
    )

    ax.set_xlabel(x)
    ax.set_ylabel(y)

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"{y} en fonction de {x}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=data[[x, y]].copy()
    )


def lineplot(
    data,
    x,
    y,
    figsize=(10, 6),
    title=None
):

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        data[x],
        data[y]
    )

    ax.set_xlabel(x)
    ax.set_ylabel(y)

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"{y} selon {x}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=data[[x, y]].copy()
    )


def correlation_heatmap(
    data,
    figsize=(10, 8),
    title="Matrice de corrélation"
):

    numeric_data = data.select_dtypes(
        include="number"
    )

    correlation = (
        numeric_data.corr()
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    image = ax.imshow(
        correlation,
        interpolation="nearest"
    )

    ax.set_xticks(
        range(len(correlation.columns))
    )

    ax.set_yticks(
        range(len(correlation.columns))
    )

    ax.set_xticklabels(
        correlation.columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticklabels(
        correlation.columns
    )

    fig.colorbar(
        image,
        ax=ax
    )

    ax.set_title(
        title
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=correlation
    )


def grouped_boxplot(
    data,
    categorical,
    numeric,
    figsize=(10, 6),
    title=None
):

    groups = [
        group[numeric].dropna().values
        for _, group
        in data.groupby(
            categorical,
            observed=True
        )
    ]

    labels = [
        str(value)
        for value
        in data[categorical]
        .dropna()
        .unique()
    ]

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.boxplot(
        groups,
        tick_labels=labels
    )

    ax.set_xlabel(
        categorical
    )

    ax.set_ylabel(
        numeric
    )

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"{numeric} selon {categorical}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=data[
            [categorical, numeric]
        ].copy()
    )


def grouped_barplot(
    data,
    categorical,
    target,
    figsize=(10, 6),
    title=None
):

    table = pd.crosstab(
        data[categorical],
        data[target]
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    table.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel(
        categorical
    )

    ax.set_ylabel(
        "Effectif"
    )

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"{target} selon {categorical}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=table
    )


def mean_plot(
    data,
    categorical,
    numeric,
    figsize=(10, 6),
    title=None
):

    means = (
        data.groupby(
            categorical,
            observed=True
        )[numeric]
        .mean()
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    means.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel(
        categorical
    )

    ax.set_ylabel(
        f"Moyenne de {numeric}"
    )

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Moyenne de {numeric} selon {categorical}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=means
    )


class BivariateVisualizer:

    name = "Bivariate Visualizer"

    def __init__(
        self,
        figsize=(10, 6)
    ):

        self.figsize = figsize

    def scatterplot(
        self,
        data,
        x,
        y,
        title=None
    ):

        return scatterplot(
            data,
            x,
            y,
            figsize=self.figsize,
            title=title
        )

    def lineplot(
        self,
        data,
        x,
        y,
        title=None
    ):

        return lineplot(
            data,
            x,
            y,
            figsize=self.figsize,
            title=title
        )

    def correlation_heatmap(
        self,
        data,
        title="Matrice de corrélation"
    ):

        return correlation_heatmap(
            data,
            figsize=self.figsize,
            title=title
        )

    def grouped_boxplot(
        self,
        data,
        categorical,
        numeric,
        title=None
    ):

        return grouped_boxplot(
            data,
            categorical,
            numeric,
            figsize=self.figsize,
            title=title
        )

    def grouped_barplot(
        self,
        data,
        categorical,
        target,
        title=None
    ):

        return grouped_barplot(
            data,
            categorical,
            target,
            figsize=self.figsize,
            title=title
        )

    def mean_plot(
        self,
        data,
        categorical,
        numeric,
        title=None
    ):

        return mean_plot(
            data,
            categorical,
            numeric,
            figsize=self.figsize,
            title=title
        )
