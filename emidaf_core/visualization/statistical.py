"""
=========================================================
EMIDAF Framework
Visualization - Statistical Plots
=========================================================
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def mean_median_plot(
    data,
    column,
    figsize=(10, 6),
    title=None
):

    series = data[column].dropna()

    mean_value = series.mean()
    median_value = series.median()

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.hist(
        series,
        bins=30,
        alpha=0.7
    )

    ax.axvline(
        mean_value,
        linestyle="--",
        label=f"Moyenne = {mean_value:.2f}"
    )

    ax.axvline(
        median_value,
        linestyle=":",
        label=f"Médiane = {median_value:.2f}"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Effectif")

    if title is None:
        title = f"Moyenne et médiane - {column}"

    ax.set_title(title)
    ax.legend()

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data={
            "mean": mean_value,
            "median": median_value
        }
    )


def confidence_interval_plot(
    data,
    column,
    confidence=0.95,
    figsize=(8, 5),
    title=None
):

    series = data[column].dropna()

    n = len(series)

    if n < 2:
        raise ValueError(
            "Au moins deux observations sont nécessaires."
        )

    mean_value = series.mean()
    standard_error = (
        series.std(ddof=1)
        / np.sqrt(n)
    )

    from scipy.stats import t

    alpha = 1 - confidence

    critical_value = t.ppf(
        1 - alpha / 2,
        df=n - 1
    )

    margin = (
        critical_value
        * standard_error
    )

    lower = mean_value - margin
    upper = mean_value + margin

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.errorbar(
        [0],
        [mean_value],
        yerr=[
            [mean_value - lower],
            [upper - mean_value]
        ],
        fmt="o",
        capsize=8
    )

    ax.set_xlim(-1, 1)
    ax.set_xticks([0])
    ax.set_xticklabels([column])

    ax.set_ylabel("Moyenne")

    if title is None:
        title = (
            f"Intervalle de confiance "
            f"à {confidence:.0%} - {column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=pd.DataFrame({
            "mean": [mean_value],
            "lower": [lower],
            "upper": [upper],
            "confidence": [confidence]
        })
    )


def group_mean_ci_plot(
    data,
    group_column,
    value_column,
    confidence=0.95,
    figsize=(10, 6),
    title=None
):

    from scipy.stats import t

    rows = []

    for group, subset in data.groupby(
        group_column,
        observed=True
    ):

        values = (
            subset[value_column]
            .dropna()
        )

        n = len(values)

        if n == 0:
            continue

        mean_value = values.mean()

        if n > 1:

            se = (
                values.std(ddof=1)
                / np.sqrt(n)
            )

            critical = t.ppf(
                (1 + confidence) / 2,
                df=n - 1
            )

            margin = (
                critical * se
            )

        else:

            margin = 0

        rows.append({
            "group": group,
            "mean": mean_value,
            "lower": mean_value - margin,
            "upper": mean_value + margin
        })

    result = pd.DataFrame(rows)

    fig, ax = plt.subplots(
        figsize=figsize
    )

    x = np.arange(
        len(result)
    )

    means = result["mean"].to_numpy()

    lower_errors = (
        means
        - result["lower"].to_numpy()
    )

    upper_errors = (
        result["upper"].to_numpy()
        - means
    )

    ax.errorbar(
        x,
        means,
        yerr=[
            lower_errors,
            upper_errors
        ],
        fmt="o",
        capsize=6
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        result["group"],
        rotation=45,
        ha="right"
    )

    ax.set_xlabel(
        group_column
    )

    ax.set_ylabel(
        f"Moyenne de {value_column}"
    )

    if title is None:
        title = (
            f"Moyenne et IC - {value_column} "
            f"selon {group_column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=result
    )


def rank_plot(
    data,
    column,
    figsize=(10, 6),
    title=None
):

    series = (
        data[column]
        .dropna()
        .sort_values()
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        range(1, len(series) + 1),
        series
    )

    ax.set_xlabel(
        "Rang"
    )

    ax.set_ylabel(
        column
    )

    if title is None:
        title = (
            f"Graphique des rangs - {column}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=series
    )


def proportion_plot(
    data,
    group_column,
    category_column,
    figsize=(10, 6),
    title=None
):

    table = pd.crosstab(
        data[group_column],
        data[category_column],
        normalize="index"
    ) * 100

    fig, ax = plt.subplots(
        figsize=figsize
    )

    table.plot(
        kind="bar",
        stacked=True,
        ax=ax
    )

    ax.set_xlabel(
        group_column
    )

    ax.set_ylabel(
        "Pourcentage"
    )

    if title is None:
        title = (
            f"Proportions de {category_column} "
            f"selon {group_column}"
        )

    ax.set_title(title)

    ax.legend(
        title=category_column
    )

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=table
    )


class StatisticalVisualizer:

    name = "Statistical Visualizer"

    def __init__(
        self,
        figsize=(10, 6)
    ):

        self.figsize = figsize

    def mean_median(
        self,
        data,
        column,
        title=None
    ):

        return mean_median_plot(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def confidence_interval(
        self,
        data,
        column,
        confidence=0.95,
        title=None
    ):

        return confidence_interval_plot(
            data,
            column,
            confidence=confidence,
            figsize=self.figsize,
            title=title
        )

    def group_mean_ci(
        self,
        data,
        group_column,
        value_column,
        confidence=0.95,
        title=None
    ):

        return group_mean_ci_plot(
            data,
            group_column,
            value_column,
            confidence=confidence,
            figsize=self.figsize,
            title=title
        )

    def rank_plot(
        self,
        data,
        column,
        title=None
    ):

        return rank_plot(
            data,
            column,
            figsize=self.figsize,
            title=title
        )

    def proportion_plot(
        self,
        data,
        group_column,
        category_column,
        title=None
    ):

        return proportion_plot(
            data,
            group_column,
            category_column,
            figsize=self.figsize,
            title=title
        )
