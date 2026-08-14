"""
=========================================================
EMIDAF Framework
Visualization - Time Series
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .base import VisualizationResult


def time_series_plot(
    data,
    date_column,
    value_column,
    figsize=(12, 6),
    title=None
):

    plot_data = data[
        [date_column, value_column]
    ].dropna().copy()

    plot_data[date_column] = pd.to_datetime(
        plot_data[date_column]
    )

    plot_data = plot_data.sort_values(
        date_column
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        plot_data[date_column],
        plot_data[value_column]
    )

    ax.set_xlabel(
        date_column
    )

    ax.set_ylabel(
        value_column
    )

    if title is None:
        title = (
            f"{value_column} dans le temps"
        )

    ax.set_title(title)

    fig.autofmt_xdate()
    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=plot_data
    )


def rolling_mean_plot(
    data,
    date_column,
    value_column,
    window=7,
    figsize=(12, 6),
    title=None
):

    plot_data = data[
        [date_column, value_column]
    ].dropna().copy()

    plot_data[date_column] = pd.to_datetime(
        plot_data[date_column]
    )

    plot_data = plot_data.sort_values(
        date_column
    )

    plot_data["rolling_mean"] = (
        plot_data[value_column]
        .rolling(window=window)
        .mean()
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        plot_data[date_column],
        plot_data[value_column],
        alpha=0.5,
        label="Valeur"
    )

    ax.plot(
        plot_data[date_column],
        plot_data["rolling_mean"],
        label=f"Moyenne mobile ({window})"
    )

    ax.set_xlabel(
        date_column
    )

    ax.set_ylabel(
        value_column
    )

    if title is None:
        title = (
            f"Moyenne mobile de {value_column}"
        )

    ax.set_title(title)
    ax.legend()

    fig.autofmt_xdate()
    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=plot_data
    )


def rolling_std_plot(
    data,
    date_column,
    value_column,
    window=7,
    figsize=(12, 6),
    title=None
):

    plot_data = data[
        [date_column, value_column]
    ].dropna().copy()

    plot_data[date_column] = pd.to_datetime(
        plot_data[date_column]
    )

    plot_data = plot_data.sort_values(
        date_column
    )

    plot_data["rolling_std"] = (
        plot_data[value_column]
        .rolling(window=window)
        .std()
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.plot(
        plot_data[date_column],
        plot_data["rolling_std"]
    )

    ax.set_xlabel(
        date_column
    )

    ax.set_ylabel(
        "Écart-type mobile"
    )

    if title is None:
        title = (
            f"Écart-type mobile de {value_column}"
        )

    ax.set_title(title)

    fig.autofmt_xdate()
    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=plot_data
    )


def seasonal_boxplot(
    data,
    date_column,
    value_column,
    period="month",
    figsize=(12, 6),
    title=None
):

    plot_data = data[
        [date_column, value_column]
    ].dropna().copy()

    plot_data[date_column] = pd.to_datetime(
        plot_data[date_column]
    )

    if period == "month":

        plot_data["period"] = (
            plot_data[date_column]
            .dt.month
        )

    elif period == "weekday":

        plot_data["period"] = (
            plot_data[date_column]
            .dt.dayofweek
        )

    elif period == "hour":

        plot_data["period"] = (
            plot_data[date_column]
            .dt.hour
        )

    else:

        raise ValueError(
            "period doit être : "
            "'month', 'weekday' ou 'hour'."
        )

    groups = [
        group[value_column].values
        for _, group
        in plot_data.groupby(
            "period",
            sort=True
        )
    ]

    labels = [
        str(value)
        for value in sorted(
            plot_data["period"].unique()
        )
    ]

    fig, ax = plt.subplots(
        figsize=figsize
    )

    ax.boxplot(
        groups,
        labels=labels
    )

    ax.set_xlabel(
        period
    )

    ax.set_ylabel(
        value_column
    )

    if title is None:
        title = (
            f"Distribution de {value_column} "
            f"par {period}"
        )

    ax.set_title(title)

    fig.tight_layout()

    return VisualizationResult(
        figure=fig,
        axes=ax,
        data=plot_data
    )


class TimeSeriesVisualizer:

    name = "Time Series Visualizer"

    def __init__(
        self,
        figsize=(12, 6)
    ):

        self.figsize = figsize

    def plot(
        self,
        data,
        date_column,
        value_column,
        title=None
    ):

        return time_series_plot(
            data,
            date_column,
            value_column,
            figsize=self.figsize,
            title=title
        )

    def rolling_mean(
        self,
        data,
        date_column,
        value_column,
        window=7,
        title=None
    ):

        return rolling_mean_plot(
            data,
            date_column,
            value_column,
            window=window,
            figsize=self.figsize,
            title=title
        )

    def rolling_std(
        self,
        data,
        date_column,
        value_column,
        window=7,
        title=None
    ):

        return rolling_std_plot(
            data,
            date_column,
            value_column,
            window=window,
            figsize=self.figsize,
            title=title
        )

    def seasonal_boxplot(
        self,
        data,
        date_column,
        value_column,
        period="month",
        title=None
    ):

        return seasonal_boxplot(
            data,
            date_column,
            value_column,
            period=period,
            figsize=self.figsize,
            title=title
        )
