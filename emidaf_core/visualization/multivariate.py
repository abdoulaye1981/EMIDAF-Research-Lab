"""
=========================================================
EMIDAF Framework
Visualization - Multivariate Analysis
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def pairplot(
    data,
    columns=None,
    figsize=(10, 10),
    title=None
):

    if columns is None:

        plot_data = data.select_dtypes(
            include="number"
        )

    else:

        plot_data = data[columns]

    n = len(plot_data.columns)

    if n == 0:

        raise ValueError(
            "Aucune variable numérique disponible."
        )

    fig, axes = plt.subplots(
        n,
        n,
        figsize=figsize,
        squeeze=False
    )

    for i, column_y in enumerate(
        plot_data.columns
    ):

        for j, column_x in enumerate(
            plot_data.columns
        ):

            ax = axes[i, j]

            if i == j:

                ax.hist(
                    plot_data[column_x]
                    .dropna(),
                    bins=20
                )

            else:

                ax.scatter(
                    plot_data[column_x],
                    plot_data[column_y]
                )

            if i == n - 1:

                ax.set_xlabel(
                    column_x
                )

            else:

                ax.set_xlabel("")

            if j == 0:

                ax.set_ylabel(
                    column_y
                )

            else:

                ax.set_ylabel("")

    if title is not None:

        fig.suptitle(
            title
        )

    else:

        fig.suptitle(
            "Analyse multivariée"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=axes,
        data=plot_data
    )


def correlation_matrix(
    data,
    method="pearson"
):

    numeric_data = data.select_dtypes(
        include="number"
    )

    return numeric_data.corr(
        method=method
    )


def correlation_heatmap(
    data,
    method="pearson",
    figsize=(10, 8),
    title=None
):

    correlation = correlation_matrix(
        data,
        method=method
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    image = ax.imshow(
        correlation,
        interpolation="nearest"
    )

    ax.set_xticks(
        range(
            len(correlation.columns)
        )
    )

    ax.set_yticks(
        range(
            len(correlation.columns)
        )
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

    if title is not None:

        ax.set_title(
            title
        )

    else:

        ax.set_title(
            "Matrice de corrélation"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=correlation
    )


def parallel_coordinates(
    data,
    class_column,
    columns=None,
    figsize=(12, 7),
    title=None
):

    if columns is None:

        columns = list(
            data.select_dtypes(
                include="number"
            ).columns
        )

    if len(columns) == 0:

        raise ValueError(
            "Aucune variable numérique disponible."
        )

    classes = data[
        class_column
    ].dropna().unique()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    x = range(
        len(columns)
    )

    for class_value in classes:

        subset = data[
            data[class_column]
            == class_value
        ]

        for _, row in subset[
            columns
        ].dropna().iterrows():

            ax.plot(
                x,
                row.values,
                alpha=0.6
            )

    ax.set_xticks(
        list(x)
    )

    ax.set_xticklabels(
        columns,
        rotation=45,
        ha="right"
    )

    if title is not None:

        ax.set_title(
            title
        )

    else:

        ax.set_title(
            f"Coordonnées parallèles selon {class_column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=data[
            columns + [class_column]
        ].copy()
    )


def stacked_barplot(
    data,
    columns,
    figsize=(10, 6),
    title=None
):

    table = data[
        columns
    ].value_counts()

    table = table.unstack(
        fill_value=0
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    table.plot(
        kind="bar",
        stacked=True,
        ax=ax
    )

    if title is not None:

        ax.set_title(
            title
        )

    else:

        ax.set_title(
            "Barplot empilé"
        )

    ax.set_ylabel(
        "Effectif"
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=table
    )


def cumulative_distribution(
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

    cumulative = (
        series
        .rank(
            method="average"
        )
        / len(series)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        series.values,
        cumulative.values
    )

    ax.set_xlabel(
        column
    )

    ax.set_ylabel(
        "Fréquence cumulée"
    )

    if title is not None:

        ax.set_title(
            title
        )

    else:

        ax.set_title(
            f"Distribution cumulée de {column}"
        )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=pd.DataFrame({
            column: series.values,
            "cumulative":
                cumulative.values
        })
    )


class MultivariateVisualizer:

    name = "Multivariate Visualizer"

    def __init__(
        self,
        figsize=(10, 8)
    ):

        self.figsize = figsize

    def pairplot(
        self,
        data,
        columns=None,
        title=None
    ):

        return pairplot(
            data,
            columns=columns,
            figsize=self.figsize,
            title=title
        )

    def correlation_heatmap(
        self,
        data,
        method="pearson",
        title=None
    ):

        return correlation_heatmap(
            data,
            method=method,
            figsize=self.figsize,
            title=title
        )

    def parallel_coordinates(
        self,
        data,
        class_column,
        columns=None,
        title=None
    ):

        return parallel_coordinates(
            data,
            class_column,
            columns=columns,
            figsize=self.figsize,
            title=title
        )

    def stacked_barplot(
        self,
        data,
        columns,
        title=None
    ):

        return stacked_barplot(
            data,
            columns,
            figsize=self.figsize,
            title=title
        )

    def cumulative_distribution(
        self,
        data,
        column,
        title=None
    ):

        return cumulative_distribution(
            data,
            column,
            figsize=self.figsize,
            title=title
        )
