
from io import StringIO

import numpy as np
import pandas as pd
import plotly.express as px

from dash import (
    Input,
    Output,
    State,
    callback,
    dcc,
    html,
    no_update,
)

import dash_bootstrap_components as dbc

from emidaf_core.dataset.profiler import DatasetProfiler


def _df(data):
    return pd.read_json(
        StringIO(data),
        orient="split",
    )


def _table(dataframe):
    return dbc.Table.from_dataframe(
        dataframe,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _numeric_like(series):
    if pd.api.types.is_numeric_dtype(series):
        return True

    non_null = series.dropna()

    if non_null.empty:
        return False

    converted = pd.to_numeric(
        non_null,
        errors="coerce",
    )

    return (
        converted.notna().mean()
        >= 0.95
    )


@callback(
    Output(
        "elae-descriptive",
        "children",
    ),
    Input(
        "elae-data",
        "data",
    ),
)
def descriptive_analysis(data):

    dataframe = _df(data)

    numeric = dataframe.select_dtypes(
        include="number"
    )

    if numeric.empty:
        return dbc.Alert(
            "Aucune variable numérique.",
            color="warning",
        )

    profiler = DatasetProfiler()
    profile = profiler.profile(dataframe)

    distributions = (
        getattr(
            profile,
            "distributions",
            {},
        )
        or {}
    )

    columns = distributions.get(
        "columns",
        {},
    )

    if columns:

        rows = []

        for variable, stats in columns.items():

            rows.append(
                {
                    "Variable": variable,
                    "n": stats.get("count"),
                    "Moyenne": stats.get("mean"),
                    "Médiane": stats.get("median"),
                    "Écart-type": stats.get("std"),
                    "Variance": stats.get("variance"),
                    "Minimum": stats.get("minimum"),
                    "Maximum": stats.get("maximum"),
                }
            )

        summary = pd.DataFrame(rows)

    else:

        summary = (
            numeric
            .describe()
            .T
            .reset_index()
            .rename(
                columns={
                    "index": "Variable"
                }
            )
        )

    return _table(summary.round(4))


@callback(
    Output(
        "elae-univariate-summary",
        "children",
    ),
    Output(
        "elae-univariate-graph",
        "figure",
    ),
    Input(
        "elae-univariate-variable",
        "value",
    ),
    State(
        "elae-data",
        "data",
    ),
)
def univariate(variable, data):

    dataframe = _df(data)

    if (
        variable is None
        or variable not in dataframe.columns
    ):
        return (
            dbc.Alert(
                "Variable indisponible.",
                color="warning",
            ),
            {},
        )

    series = dataframe[variable]

    if _numeric_like(series):

        numeric = pd.to_numeric(
            series,
            errors="coerce",
        )

        summary = pd.DataFrame(
            {
                "Indicateur": [
                    "Effectif",
                    "Manquants",
                    "Moyenne",
                    "Médiane",
                    "Écart-type",
                    "Minimum",
                    "Q1",
                    "Q3",
                    "Maximum",
                    "Asymétrie",
                ],
                "Valeur": [
                    int(numeric.notna().sum()),
                    int(numeric.isna().sum()),
                    numeric.mean(),
                    numeric.median(),
                    numeric.std(),
                    numeric.min(),
                    numeric.quantile(0.25),
                    numeric.quantile(0.75),
                    numeric.max(),
                    numeric.skew(),
                ],
            }
        )

        plot_df = pd.DataFrame(
            {
                variable: numeric
            }
        )

        figure = px.histogram(
            plot_df,
            x=variable,
            marginal="box",
            title=(
                f"Distribution de {variable}"
            ),
        )

    else:

        counts = (
            series
            .fillna("Valeur manquante")
            .value_counts(dropna=False)
            .rename_axis("Modalité")
            .reset_index(name="Effectif")
        )

        counts["Pourcentage"] = (
            100
            * counts["Effectif"]
            / len(series)
        )

        summary = counts

        figure = px.bar(
            counts,
            x="Modalité",
            y="Effectif",
            title=(
                f"Distribution de {variable}"
            ),
        )

    return (
        _table(summary.round(4)),
        figure,
    )


@callback(
    Output(
        "elae-bivariate-summary",
        "children",
    ),
    Output(
        "elae-bivariate-graph",
        "figure",
    ),
    Input(
        "elae-x",
        "value",
    ),
    Input(
        "elae-y",
        "value",
    ),
    State(
        "elae-data",
        "data",
    ),
)
def bivariate(x, y, data):

    dataframe = _df(data)

    if (
        x not in dataframe.columns
        or y not in dataframe.columns
        or x == y
    ):
        return (
            dbc.Alert(
                "Sélectionnez deux variables différentes.",
                color="warning",
            ),
            {},
        )

    x_num = _numeric_like(
        dataframe[x]
    )

    y_num = _numeric_like(
        dataframe[y]
    )

    # ==========================================
    # Numérique / numérique
    # ==========================================

    if x_num and y_num:

        temp = pd.DataFrame(
            {
                x: pd.to_numeric(
                    dataframe[x],
                    errors="coerce",
                ),
                y: pd.to_numeric(
                    dataframe[y],
                    errors="coerce",
                ),
            }
        ).dropna()

        corr = temp[x].corr(
            temp[y]
        )

        summary = dbc.Alert(
            f"Corrélation de Pearson : {corr:.4f}",
            color="info",
        )

        figure = px.scatter(
            temp,
            x=x,
            y=y,
            trendline=None,
            title=f"{y} en fonction de {x}",
        )

        return summary, figure

    # ==========================================
    # Catégorielle / numérique
    # ==========================================

    if not x_num and y_num:

        temp = dataframe[
            [x, y]
        ].copy()

        temp[y] = pd.to_numeric(
            temp[y],
            errors="coerce",
        )

        grouped = (
            temp
            .groupby(
                x,
                dropna=False,
            )[y]
            .agg(
                [
                    "count",
                    "mean",
                    "median",
                    "std",
                    "min",
                    "max",
                ]
            )
            .reset_index()
        )

        figure = px.box(
            temp,
            x=x,
            y=y,
            title=f"{y} selon {x}",
        )

        return (
            _table(grouped.round(4)),
            figure,
        )

    if x_num and not y_num:

        temp = dataframe[
            [x, y]
        ].copy()

        temp[x] = pd.to_numeric(
            temp[x],
            errors="coerce",
        )

        grouped = (
            temp
            .groupby(
                y,
                dropna=False,
            )[x]
            .agg(
                [
                    "count",
                    "mean",
                    "median",
                    "std",
                    "min",
                    "max",
                ]
            )
            .reset_index()
        )

        figure = px.box(
            temp,
            x=y,
            y=x,
            title=f"{x} selon {y}",
        )

        return (
            _table(grouped.round(4)),
            figure,
        )

    # ==========================================
    # Catégorielle / catégorielle
    # ==========================================

    table = pd.crosstab(
        dataframe[x],
        dataframe[y],
        dropna=False,
    )

    plot = table.reset_index().melt(
        id_vars=x,
        var_name=y,
        value_name="Effectif",
    )

    figure = px.density_heatmap(
        plot,
        x=y,
        y=x,
        z="Effectif",
        title=f"{x} × {y}",
    )

    return (
        _table(
            table.reset_index()
        ),
        figure,
    )


@callback(
    Output(
        "elae-correlation-table",
        "children",
    ),
    Output(
        "elae-correlation-graph",
        "figure",
    ),
    Input(
        "elae-data",
        "data",
    ),
)
def correlations(data):

    dataframe = _df(data)

    numeric = dataframe.select_dtypes(
        include="number"
    )

    if numeric.shape[1] < 2:
        return (
            dbc.Alert(
                (
                    "Au moins deux variables numériques "
                    "sont nécessaires."
                ),
                color="warning",
            ),
            {},
        )

    profiler = DatasetProfiler()
    profile = profiler.profile(
        dataframe
    )

    correlation_result = (
        getattr(
            profile,
            "correlations",
            {},
        )
        or {}
    )

    matrix = (
        correlation_result.get(
            "correlation_matrix"
        )
        or correlation_result.get(
            "matrix"
        )
    )

    if isinstance(matrix, dict):
        corr = pd.DataFrame(matrix)
    else:
        corr = numeric.corr()

    corr = corr.astype(float)

    figure = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Matrice de corrélation",
        zmin=-1,
        zmax=1,
    )

    display = (
        corr
        .round(4)
        .reset_index()
        .rename(
            columns={
                "index": "Variable"
            }
        )
    )

    return (
        _table(display),
        figure,
    )


@callback(
    Output(
        "elae-group-summary",
        "children",
    ),
    Output(
        "elae-group-graph",
        "figure",
    ),
    Input(
        "elae-group-variable",
        "value",
    ),
    Input(
        "elae-value-variable",
        "value",
    ),
    State(
        "elae-data",
        "data",
    ),
)
def grouped_analysis(
    group_variable,
    value_variable,
    data,
):

    dataframe = _df(data)

    if (
        not group_variable
        or not value_variable
        or group_variable not in dataframe.columns
        or value_variable not in dataframe.columns
    ):
        return (
            dbc.Alert(
                (
                    "Sélectionnez une variable de groupe "
                    "et une variable numérique."
                ),
                color="warning",
            ),
            {},
        )

    temp = dataframe[
        [
            group_variable,
            value_variable,
        ]
    ].copy()

    temp[value_variable] = pd.to_numeric(
        temp[value_variable],
        errors="coerce",
    )

    grouped = (
        temp
        .groupby(
            group_variable,
            dropna=False,
        )[value_variable]
        .agg(
            [
                "count",
                "mean",
                "median",
                "std",
                "min",
                "max",
            ]
        )
        .reset_index()
    )

    figure = px.box(
        temp,
        x=group_variable,
        y=value_variable,
        points="outliers",
        title=(
            f"{value_variable} selon "
            f"{group_variable}"
        ),
    )

    return (
        _table(grouped.round(4)),
        figure,
    )


@callback(
    Output(
        "elae-download-data",
        "data",
    ),
    Input(
        "elae-download",
        "n_clicks",
    ),
    State(
        "elae-data",
        "data",
    ),
    prevent_initial_call=True,
)
def download_summary(
    n_clicks,
    data,
):

    if not n_clicks:
        return no_update

    dataframe = _df(data)

    summary = (
        dataframe
        .describe(
            include="all"
        )
        .T
        .reset_index()
        .rename(
            columns={
                "index": "Variable"
            }
        )
    )

    return dcc.send_data_frame(
        summary.to_csv,
        "elae_resume_descriptif.csv",
        index=False,
    )
