"""
=========================================================
EMIDAF Framework
Visualization - Categorical Variables
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def frequency_barplot(
    data,
    column,
    figsize=(10, 6),
    title=None,
    rotation=45
):

    counts = (
        data[column]
        .value_counts(dropna=False)
    )

    fig, ax = plt.subplots(
        figsize=figsize
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

    if title is None:
        title = f"Effectifs - {column}"

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=counts
    )


def frequency_barh(
    data,
    column,
    figsize=(10, 6),
    title=None
):

    counts = (
        data[column]
        .value_counts(dropna=False)
        .sort_values()
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    counts.plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Effectif")
    ax.set_ylabel(column)

    if title is None:
        title = f"Effectifs - {column}"

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=counts
    )


def frequency_pie(
    data,
    column,
    figsize=(8, 8),
    title=None
):

    counts = (
        data[column]
        .value_counts(dropna=False)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    counts.plot(
        kind="pie",
        ax=ax,
        autopct="%1.1f%%"
    )

    ax.set_ylabel("")

    if title is None:
        title = f"Répartition - {column}"

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=counts
    )


def frequency_table(
    data,
    column
):

    counts = (
        data[column]
        .value_counts(dropna=False)
    )

    frequencies = (
        data[column]
        .value_counts(
            normalize=True,
            dropna=False
        )
    )

    result = pd.DataFrame({
        "effectif": counts,
        "frequence": frequencies,
        "pourcentage": frequencies * 100
    })

    return result


def cumulative_frequency(
    data,
    column,
    figsize=(10, 6),
    title=None
):

    table = frequency_table(
        data,
        column
    )

    table["effectif_cumule"] = (
        table["effectif"].cumsum()
    )

    table["pourcentage_cumule"] = (
        table["pourcentage"].cumsum()
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        range(len(table)),
        table["pourcentage_cumule"],
        marker="o"
    )

    ax.set_xticks(
        range(len(table))
    )

    ax.set_xticklabels(
        table.index,
        rotation=45,
        ha="right"
    )

    ax.set_xlabel(column)
    ax.set_ylabel(
        "Pourcentage cumulé"
    )

    if title is None:
        title = (
            f"Fréquence cumulée - {column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=table
    )


def compare_categories(
    data,
    column1,
    column2,
    figsize=(10, 6),
    title=None
):

    table = pd.crosstab(
        data[column1],
        data[column2]
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    table.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel(column1)
    ax.set_ylabel("Effectif")

    if title is None:
        title = (
            f"{column2} selon {column1}"
        )

    ax.set_title(title)

    ax.legend(
        title=column2
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=table
    )


class CategoricalVisualizer:

    name = "Categorical Visualizer"

    def __init__(
        self,
        figsize=(10, 6)
    ):

        self.figsize = figsize

    def frequency_barplot(
        self,
        data,
        column,
        title=None,
        rotation=45
    ):

        return frequency_barplot(
            data,
            column,
            figsize=self.figsize,
            title=title,
            rotation=rotation
        )

    def frequency_barh(
        self,
        data,
        column,
        title=None
    ):

        return frequency_barh(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def frequency_pie(
        self,
        data,
        column,
        title=None
    ):

        return frequency_pie(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def frequency_table(
        self,
        data,
        column
    ):

        return frequency_table(
            data,
            column
        )

    def cumulative_frequency(
        self,
        data,
        column,
        title=None
    ):

        return cumulative_frequency(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def compare_categories(
        self,
        data,
        column1,
        column2,
        title=None
    ):

        return compare_categories(
            data,
            column1,
            column2,
            figsize=self.figsize,
            title=title
        )
