
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

from emidaf_studio.services.model_registry import (
    merge_analysis_section,
)

from emidaf_core.dataset.profiler import DatasetProfiler

from emidaf_core.statistics.inferential.group_selector import (
    GroupTestSelector,
)
from emidaf_core.statistics.inferential.group_effect_size import (
    GroupEffectSize,
)
from emidaf_core.statistics.inferential.posthoc import (
    AdaptivePostHoc,
)

from dash.exceptions import PreventUpdate

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)


def _load_elae_dataframe(
    project_id,
    dataset_id,
):
    """
    Charge le dataset côté serveur.

    Le DataFrame complet ne transite pas
    par le navigateur.
    """

    _, _, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        raise PreventUpdate

    return result



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


def _semantic_datatypes(dataframe):
    """
    Retourne le typage sémantique produit par DatasetProfiler.

    ELAE utilise ainsi la même source de vérité que
    l'Inspection des données.
    """

    profiler = DatasetProfiler()
    profile = profiler.profile(
        dataframe
    )

    return (
        profile.datatypes
        or {}
    )


def _semantic_numeric_columns(dataframe):
    datatypes = _semantic_datatypes(
        dataframe
    )

    return [
        column
        for column in datatypes.get(
            "numeric",
            [],
        )
        if column in dataframe.columns
    ]


def _semantic_group_columns(dataframe):
    datatypes = _semantic_datatypes(
        dataframe
    )

    columns = (
        list(
            datatypes.get(
                "categorical",
                [],
            )
            or []
        )
        + list(
            datatypes.get(
                "boolean",
                [],
            )
            or []
        )
    )

    return [
        column
        for column in columns
        if column in dataframe.columns
    ]


def _persist_elae(
    project_id,
    dataset_id,
    section,
    payload,
):
    """
    Persiste atomiquement une sous-section ELAE
    sans écraser les autres résultats du même stage.
    """

    if (
        project_id is None
        or dataset_id is None
    ):
        return

    merge_analysis_section(
        project_id,
        dataset_id,
        "elae",
        section,
        payload,
    )


@callback(
    Output(
        "elae-descriptive",
        "children",
    ),
    Input(
        "elae-tabs",
        "active_tab",
    ),
    State(
        "elae-project-id",
        "data",
    ),
    State(
        "elae-dataset-id",
        "data",
    ),
)
def descriptive_analysis(
    active_tab,
    project_id,
    dataset_id,
):
    if active_tab != "descriptive":
        return no_update


    dataframe = _load_elae_dataframe(
        project_id,
        dataset_id,
    )

    profiler = DatasetProfiler()
    profile = profiler.profile(
        dataframe
    )

    datatypes = (
        profile.datatypes
        or {}
    )

    numeric_columns = (
        datatypes.get(
            "numeric",
            [],
        )
        or []
    )

    numeric = dataframe[
        [
            column
            for column in numeric_columns
            if column in dataframe.columns
        ]
    ].copy()

    if numeric.empty:
        return dbc.Alert(
            "Aucune variable numérique sémantique.",
            color="warning",
        )

    summary = pd.DataFrame(
        {
            "Variable": list(numeric.columns),
            "n": [
                int(
                    numeric[column]
                    .notna()
                    .sum()
                )
                for column in numeric.columns
            ],
            "Moyenne": [
                numeric[column].mean()
                for column in numeric.columns
            ],
            "Médiane": [
                numeric[column].median()
                for column in numeric.columns
            ],
            "Écart-type": [
                numeric[column].std()
                for column in numeric.columns
            ],
            "Variance": [
                numeric[column].var()
                for column in numeric.columns
            ],
            "Minimum": [
                numeric[column].min()
                for column in numeric.columns
            ],
            "Maximum": [
                numeric[column].max()
                for column in numeric.columns
            ],
        }
    )

    summary = summary.round(4)

    _persist_elae(
        project_id,
        dataset_id,
        "descriptive",
        {
            "numeric_variables": (
                list(numeric.columns)
            ),
            "summary": (
                summary.to_dict(
                    orient="records"
                )
            ),
        },
    )

    return _table(summary)


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
        "elae-tabs",
        "active_tab",
    ),
    Input(
        "elae-univariate-variable",
        "value",
    ),
    State(
        "elae-project-id",
        "data",
    ),
    State(
        "elae-dataset-id",
        "data",
    ),
)
def univariate(
    active_tab,
    variable,
    project_id,
    dataset_id,
):
    if active_tab != "univariate":
        return no_update, no_update


    dataframe = _load_elae_dataframe(
        project_id,
        dataset_id,
    )

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

    datatypes = _semantic_datatypes(
        dataframe
    )

    semantic_numeric = set(
        datatypes.get(
            "numeric",
            [],
        )
        or []
    )

    semantic_identifiers = set(
        datatypes.get(
            "identifier",
            [],
        )
        or []
    )

    semantic_text = set(
        datatypes.get(
            "text",
            [],
        )
        or []
    )

    if (
        variable in semantic_identifiers
        or variable in semantic_text
    ):
        return (
            dbc.Alert(
                (
                    "Cette variable n'est pas destinée "
                    "à l'analyse exploratoire ELAE."
                ),
                color="warning",
            ),
            {},
        )

    if variable in semantic_numeric:

        persisted_numeric = pd.to_numeric(
            series,
            errors="coerce",
        )

        _persist_elae(
            project_id,
            dataset_id,
            "univariate",
            {
                "variable": variable,
                "type": "numeric",
                "statistics": {
                    "count": int(
                        persisted_numeric.notna().sum()
                    ),
                    "missing": int(
                        persisted_numeric.isna().sum()
                    ),
                    "mean": persisted_numeric.mean(),
                    "median": persisted_numeric.median(),
                    "std": persisted_numeric.std(),
                    "minimum": persisted_numeric.min(),
                    "q1": persisted_numeric.quantile(0.25),
                    "q3": persisted_numeric.quantile(0.75),
                    "maximum": persisted_numeric.max(),
                    "skewness": persisted_numeric.skew(),
                },
            },
        )

    else:

        counts = (
            series
            .fillna("<Manquant>")
            .astype(str)
            .value_counts(
                dropna=False
            )
        )

        _persist_elae(
            project_id,
            dataset_id,
            "univariate",
            {
                "variable": variable,
                "type": "categorical",
                "count": int(series.notna().sum()),
                "missing": int(series.isna().sum()),
                "unique": int(
                    series.nunique(
                        dropna=True
                    )
                ),
                "frequencies": (
                    counts.to_dict()
                ),
            },
        )

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
        "elae-tabs",
        "active_tab",
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
        "elae-project-id",
        "data",
    ),
    State(
        "elae-dataset-id",
        "data",
    ),
)
def bivariate(
    active_tab,
    x,
    y,
    project_id,
    dataset_id,
):
    if active_tab != "bivariate":
        return no_update, no_update


    dataframe = _load_elae_dataframe(
        project_id,
        dataset_id,
    )

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

    profiler = DatasetProfiler()
    profile = profiler.profile(
        dataframe
    )

    datatypes = (
        profile.datatypes
        or {}
    )

    correlation_result = (
        getattr(
            profile,
            "correlations",
            {},
        )
        or {}
    )

    semantic = (
        datatypes.get(
            "semantic",
            {},
        )
        or {}
    )

    semantic_numeric = set(
        datatypes.get(
            "numeric",
            [],
        )
        or []
    )

    ordinal_columns = set(
        semantic.get(
            "ordinal",
            [],
        )
        or []
    )

    forbidden_columns = set(
        datatypes.get(
            "identifier",
            [],
        )
        or []
    ) | set(
        datatypes.get(
            "text",
            [],
        )
        or []
    )

    if (
        x in forbidden_columns
        or y in forbidden_columns
    ):
        return (
            dbc.Alert(
                (
                    "Les identifiants et variables texte libre "
                    "ne sont pas analysés dans cet onglet."
                ),
                color="warning",
            ),
            {},
        )

    x_num = x in semantic_numeric
    y_num = y in semantic_numeric


    if x_num and y_num:

        persisted = pd.DataFrame(
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

        adaptive_pairs = (
            correlation_result.get(
                "adaptive_pairs",
                [],
            )
            or []
        )

        adaptive_pair = next(
            (
                pair
                for pair in adaptive_pairs
                if {
                    pair.get("variable_1"),
                    pair.get("variable_2"),
                }
                == {x, y}
            ),
            None,
        )

        correlation = (
            adaptive_pair.get(
                "correlation"
            )
            if adaptive_pair
            else None
        )

        correlation_method = (
            adaptive_pair.get(
                "method"
            )
            if adaptive_pair
            else None
        )

        correlation_reason = (
            adaptive_pair.get(
                "reason"
            )
            if adaptive_pair
            else None
        )

        x_ordinal = x in ordinal_columns
        y_ordinal = y in ordinal_columns

        if x_ordinal and not y_ordinal:
            relationship_type = (
                "ordinal_numeric"
            )
        elif y_ordinal and not x_ordinal:
            relationship_type = (
                "numeric_ordinal"
            )
        elif x_ordinal and y_ordinal:
            relationship_type = (
                "ordinal_ordinal"
            )
        else:
            relationship_type = (
                "numeric_numeric"
            )

        _persist_elae(
            project_id,
            dataset_id,
            "bivariate",
            {
                "x": x,
                "y": y,
                "relationship_type": (
                    relationship_type
                ),
                "n": int(len(persisted)),
                "correlation": correlation,
                "correlation_method": (
                    correlation_method
                ),
                "correlation_reason": (
                    correlation_reason
                ),
            },
        )

    elif not x_num and y_num:

        persisted = (
            dataframe[[x, y]]
            .assign(
                **{
                    y: pd.to_numeric(
                        dataframe[y],
                        errors="coerce",
                    )
                }
            )
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

        _persist_elae(
            project_id,
            dataset_id,
            "bivariate",
            {
                "x": x,
                "y": y,
                "relationship_type": (
                    "categorical_numeric"
                ),
                "group_summary": (
                    persisted
                    .round(6)
                    .to_dict(
                        orient="records"
                    )
                ),
            },
        )

    elif x_num and not y_num:

        persisted = (
            dataframe[[x, y]]
            .assign(
                **{
                    x: pd.to_numeric(
                        dataframe[x],
                        errors="coerce",
                    )
                }
            )
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

        _persist_elae(
            project_id,
            dataset_id,
            "bivariate",
            {
                "x": x,
                "y": y,
                "relationship_type": (
                    "numeric_categorical"
                ),
                "group_summary": (
                    persisted
                    .round(6)
                    .to_dict(
                        orient="records"
                    )
                ),
            },
        )

    else:

        contingency = pd.crosstab(
            dataframe[x],
            dataframe[y],
            dropna=False,
        )

        _persist_elae(
            project_id,
            dataset_id,
            "bivariate",
            {
                "x": x,
                "y": y,
                "relationship_type": (
                    "categorical_categorical"
                ),
                "contingency_table": (
                    contingency
                    .reset_index()
                    .to_dict(
                        orient="records"
                    )
                ),
            },
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

        adaptive_pairs = (
            correlation_result.get(
                "adaptive_pairs",
                [],
            )
            or []
        )

        adaptive_pair = next(
            (
                pair
                for pair in adaptive_pairs
                if {
                    pair.get("variable_1"),
                    pair.get("variable_2"),
                }
                == {x, y}
            ),
            None,
        )

        if adaptive_pair is None:
            summary = dbc.Alert(
                (
                    "Corrélation adaptative indisponible "
                    "pour cette paire."
                ),
                color="warning",
            )

            figure = px.scatter(
                temp,
                x=x,
                y=y,
                trendline=None,
                title=f"{y} en fonction de {x}",
            )

            return summary, figure

        corr = adaptive_pair[
            "correlation"
        ]

        method = adaptive_pair[
            "method"
        ]

        reason = adaptive_pair.get(
            "reason"
        )

        method_label = (
            "Pearson"
            if method == "pearson"
            else "Spearman"
        )

        reason_labels = {
            "ordinal_variable": (
                "présence d'une variable ordinale"
            ),
            "both_variables_compatible_with_normality": (
                "deux variables non ordinales "
                "compatibles avec la normalité"
            ),
            "normality_not_confirmed": (
                "normalité non confirmée"
            ),
            "normality_unavailable": (
                "diagnostic de normalité indisponible"
            ),
        }

        reason_label = (
            reason_labels.get(
                reason,
                reason,
            )
        )

        summary = dbc.Alert(
            [
                html.Strong(
                    (
                        f"Corrélation de {method_label} : "
                        f"{corr:.4f}"
                    )
                ),
                html.Br(),
                html.Small(
                    (
                        "Méthode adaptative EMIDAF"
                        + (
                            f" — {reason_label}."
                            if reason_label
                            else "."
                        )
                        + " Une corrélation décrit une "
                        "association et non une causalité."
                    )
                ),
            ],
            color="info",
        )

        x_ordinal = x in ordinal_columns
        y_ordinal = y in ordinal_columns

        if x_ordinal and not y_ordinal:
            figure = px.box(
                temp,
                x=x,
                y=y,
                points=False,
                title=(
                    f"{y} selon les niveaux de {x}"
                ),
            )

        elif y_ordinal and not x_ordinal:
            figure = px.box(
                temp,
                x=y,
                y=x,
                points=False,
                title=(
                    f"{x} selon les niveaux de {y}"
                ),
            )

        else:
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
        "elae-tabs",
        "active_tab",
    ),
    State(
        "elae-project-id",
        "data",
    ),
    State(
        "elae-dataset-id",
        "data",
    ),
)
def correlations(
    active_tab,
    project_id,
    dataset_id,
):
    if active_tab != "correlations":
        return no_update, no_update


    dataframe = _load_elae_dataframe(
        project_id,
        dataset_id,
    )

    profiler = DatasetProfiler()
    profile = profiler.profile(
        dataframe
    )

    datatypes = (
        profile.datatypes
        or {}
    )

    numeric_columns = (
        datatypes.get(
            "numeric",
            [],
        )
        or []
    )

    if len(numeric_columns) < 2:
        return (
            dbc.Alert(
                (
                    "Au moins deux variables numériques "
                    "sémantiques sont nécessaires."
                ),
                color="warning",
            ),
            {},
        )

    correlation_result = (
        getattr(
            profile,
            "correlations",
            {},
        )
        or {}
    )

    matrix = correlation_result.get(
        "correlation_matrix"
    )

    if matrix is None:
        matrix = correlation_result.get(
            "matrix"
        )

    if isinstance(matrix, pd.DataFrame):
        corr = matrix.copy()

    elif isinstance(matrix, dict):
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

    _persist_elae(
        project_id,
        dataset_id,
        "correlations",
        {
            "variables": (
                list(corr.columns)
            ),
            "matrix": (
                corr
                .round(6)
                .to_dict()
            ),
        },
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
        "elae-tabs",
        "active_tab",
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
        "elae-project-id",
        "data",
    ),
    State(
        "elae-dataset-id",
        "data",
    ),
)
def grouped_analysis(
    active_tab,
    group_variable,
    value_variable,
    project_id,
    dataset_id,
):
    if active_tab != "grouped":
        return no_update, no_update

    dataframe = _load_elae_dataframe(
        project_id,
        dataset_id,
    )

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

    allowed_groups = set(
        _semantic_group_columns(
            dataframe
        )
    )

    allowed_numeric = set(
        _semantic_numeric_columns(
            dataframe
        )
    )

    if group_variable not in allowed_groups:
        return (
            dbc.Alert(
                (
                    "La variable de groupe doit être "
                    "catégorielle ou booléenne."
                ),
                color="warning",
            ),
            {},
        )

    if value_variable not in allowed_numeric:
        return (
            dbc.Alert(
                (
                    "La variable étudiée doit être "
                    "numérique au sens sémantique."
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

    # ======================================================
    # DESCRIPTIF
    # ======================================================

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

    # ------------------------------------------------------
    # Ordre sémantique des niveaux scolaires
    # ------------------------------------------------------

    level_order = [
        "6e",
        "5e",
        "4e",
        "3e",
        "2nde",
        "1ere",
        "Terminale",
    ]

    category_orders = None

    if group_variable in {
        "niveau",
        "niveau_etude",
    }:
        observed = set(
            temp[group_variable]
            .dropna()
            .astype(str)
        )

        present_levels = [
            level
            for level in level_order
            if level in observed
        ]

        if present_levels:
            category_orders = {
                group_variable:
                    present_levels,
            }

            grouped[group_variable] = (
                pd.Categorical(
                    grouped[
                        group_variable
                    ],
                    categories=
                        present_levels,
                    ordered=True,
                )
            )

            grouped = (
                grouped
                .sort_values(
                    group_variable
                )
                .reset_index(
                    drop=True
                )
            )

    display_grouped = grouped.rename(
        columns={
            "count": "Effectif",
            "mean": "Moyenne",
            "median": "Médiane",
            "std": "Écart-type",
            "min": "Minimum",
            "max": "Maximum",
        }
    )

    # ======================================================
    # GROUPES NUMÉRIQUES POUR L'INFÉRENCE
    # ======================================================

    analysis_frame = (
        temp
        .dropna(
            subset=[
                group_variable,
                value_variable,
            ]
        )
        .copy()
    )

    if category_orders:
        labels = [
            label
            for label in (
                category_orders[
                    group_variable
                ]
            )
            if (
                analysis_frame[
                    group_variable
                ]
                .astype(str)
                == str(label)
            ).any()
        ]
    else:
        labels = [
            value
            for value in (
                grouped[
                    group_variable
                ]
                .dropna()
                .tolist()
            )
        ]

    groups = []

    valid_labels = []

    for label in labels:
        mask = (
            analysis_frame[
                group_variable
            ]
            .astype(str)
            == str(label)
        )

        values = (
            analysis_frame.loc[
                mask,
                value_variable,
            ]
            .dropna()
            .to_numpy(
                dtype=float
            )
        )

        if len(values) >= 3:
            groups.append(
                values
            )
            valid_labels.append(
                str(label)
            )

    # ======================================================
    # INFÉRENCE ADAPTATIVE
    # ======================================================

    inference_component = None
    persistence_inference = None

    if len(groups) >= 2:
        try:
            selector = (
                GroupTestSelector(
                    alpha=0.05
                )
            )

            selection = (
                selector.select(
                    *groups
                )
            )

            test_result = (
                selection[
                    "result"
                ]
            )

            effect = (
                GroupEffectSize.compute(
                    selection,
                    *groups,
                )
            )

            posthoc = (
                AdaptivePostHoc.compute(
                    selection,
                    *groups,
                    labels=valid_labels,
                )
            )

            # ----------------------------------------------
            # Traduction de la justification
            # ----------------------------------------------

            reason_labels = {
                (
                    "parametric_compatible_"
                    "two_groups"
                ): (
                    "Approche paramétrique compatible "
                    "pour deux groupes ; le test de "
                    "Welch est retenu."
                ),
                (
                    "parametric_incompatible_"
                    "two_groups"
                ): (
                    "Compatibilité paramétrique "
                    "insuffisante ; le test de "
                    "Mann–Whitney est retenu."
                ),
                (
                    "parametric_compatible_"
                    "equal_variances"
                ): (
                    "Approche paramétrique compatible "
                    "et homogénéité des variances ; "
                    "l'ANOVA à un facteur est retenue."
                ),
                (
                    "parametric_compatible_"
                    "unequal_variances"
                ): (
                    "Approche paramétrique compatible, "
                    "mais variances hétérogènes ; "
                    "l'ANOVA de Welch est retenue."
                ),
                (
                    "parametric_incompatible_"
                    "k_groups"
                ): (
                    "Compatibilité paramétrique "
                    "insuffisante ; le test de "
                    "Kruskal–Wallis est retenu."
                ),
            }

            reason = reason_labels.get(
                selection.get(
                    "reason"
                ),
                (
                    "Sélection adaptative réalisée "
                    "par EMIDAF."
                ),
            )

            statistic = float(
                test_result.statistic
            )

            p_value = float(
                test_result.p_value
            )

            significant = bool(
                test_result.reject_null
            )

            if significant:
                decision = (
                    "Une différence statistiquement "
                    "significative est détectée entre "
                    "les groupes au seuil de 5 %."
                )
                decision_color = "success"
            else:
                decision = (
                    "Aucune différence statistiquement "
                    "significative n'est détectée "
                    "entre les groupes au seuil de 5 %."
                )
                decision_color = "secondary"

            p_display = (
                "< 0,0001"
                if p_value < 0.0001
                else f"{p_value:.4f}"
            )

            # ----------------------------------------------
            # Degrés de liberté si disponibles
            # ----------------------------------------------

            metadata = (
                test_result.metadata
                or {}
            )

            df_text = None

            if (
                "df_num" in metadata
                and
                "df_denom" in metadata
            ):
                df_text = (
                    f"{metadata['df_num']:.3f} ; "
                    f"{metadata['df_denom']:.3f}"
                )

            # ----------------------------------------------
            # Taille d'effet
            # ----------------------------------------------

            effect_name = (
                effect.get(
                    "name",
                    "Taille d'effet",
                )
            )

            effect_value = float(
                effect.get(
                    "value",
                    0.0,
                )
            )

            effect_magnitude = (
                effect.get(
                    "magnitude",
                    "non déterminée",
                )
            )

            effect_note = (
                effect.get(
                    "note"
                )
            )

            effect_rows = [
                html.Tr(
                    [
                        html.Th(
                            "Mesure"
                        ),
                        html.Td(
                            effect_name
                        ),
                    ]
                ),
                html.Tr(
                    [
                        html.Th(
                            "Valeur"
                        ),
                        html.Td(
                            f"{effect_value:.4f}"
                        ),
                    ]
                ),
                html.Tr(
                    [
                        html.Th(
                            "Importance"
                        ),
                        html.Td(
                            effect_magnitude
                        ),
                    ]
                ),
            ]

            secondary_effect = (
                effect.get(
                    "secondary"
                )
            )

            if secondary_effect:
                effect_rows.append(
                    html.Tr(
                        [
                            html.Th(
                                secondary_effect[
                                    "name"
                                ]
                            ),
                            html.Td(
                                f"{float(secondary_effect['value']):.4f}"
                            ),
                        ]
                    )
                )

            # ----------------------------------------------
            # Post-hoc
            # ----------------------------------------------

            posthoc_component = None

            if posthoc.get(
                "performed"
            ):
                comparisons = (
                    posthoc.get(
                        "comparisons",
                        [],
                    )
                )

                posthoc_rows = []

                for comparison in comparisons:
                    p_adjusted = float(
                        comparison.get(
                            "p_value_adjusted",
                            np.nan,
                        )
                    )

                    significant_pair = bool(
                        comparison.get(
                            "reject",
                            False,
                        )
                    )

                    row = {
                        "Comparaison": (
                            f"{comparison.get('group_1')} "
                            f"vs "
                            f"{comparison.get('group_2')}"
                        ),
                        "p-ajustée": (
                            "< 0,0001"
                            if (
                                np.isfinite(
                                    p_adjusted
                                )
                                and
                                p_adjusted
                                < 0.0001
                            )
                            else (
                                f"{p_adjusted:.4f}"
                                if np.isfinite(
                                    p_adjusted
                                )
                                else "—"
                            )
                        ),
                        "Conclusion": (
                            "Significative"
                            if significant_pair
                            else
                            "Non significative"
                        ),
                    }

                    if (
                        "mean_difference"
                        in comparison
                    ):
                        row[
                            "Différence"
                        ] = round(
                            float(
                                comparison[
                                    "mean_difference"
                                ]
                            ),
                            4,
                        )

                    elif "z" in comparison:
                        row[
                            "Statistique z"
                        ] = round(
                            float(
                                comparison[
                                    "z"
                                ]
                            ),
                            4,
                        )

                    posthoc_rows.append(
                        row
                    )

                posthoc_frame = (
                    pd.DataFrame(
                        posthoc_rows
                    )
                )

                posthoc_component = (
                    html.Div(
                        [
                            html.H6(
                                "Comparaisons post-hoc",
                                className="mt-4",
                            ),
                            html.P(
                                [
                                    html.Strong(
                                        "Méthode : "
                                    ),
                                    posthoc.get(
                                        "method",
                                        "—",
                                    ),
                                ],
                                className="mb-2",
                            ),
                            _table(
                                posthoc_frame
                            ),
                        ]
                    )
                )

            else:
                posthoc_reason = (
                    posthoc.get(
                        "reason"
                    )
                )

                if (
                    posthoc_reason
                    ==
                    "two_groups_no_posthoc"
                ):
                    posthoc_text = (
                        "Aucun post-hoc nécessaire : "
                        "la comparaison concerne "
                        "uniquement deux groupes."
                    )

                elif (
                    posthoc_reason
                    ==
                    "global_test_not_significant"
                ):
                    posthoc_text = (
                        "Post-hoc non exécuté : "
                        "le test global n'est pas "
                        "statistiquement significatif."
                    )

                else:
                    posthoc_text = (
                        "Aucun post-hoc applicable."
                    )

                posthoc_component = (
                    dbc.Alert(
                        posthoc_text,
                        color="light",
                        className="mt-3",
                    )
                )

            # ----------------------------------------------
            # Règle décisionnelle
            # ----------------------------------------------

            parametric_text = (
                "Oui"
                if selection.get(
                    "parametric_compatible"
                )
                else "Non"
            )

            variance_homogeneous = (
                selection.get(
                    "variance_homogeneous"
                )
            )

            if variance_homogeneous is None:
                variance_text = (
                    "Non applicable"
                )
            else:
                variance_text = (
                    "Oui"
                    if variance_homogeneous
                    else "Non"
                )

            test_rows = [
                html.Tr(
                    [
                        html.Th(
                            "Test retenu"
                        ),
                        html.Td(
                            test_result.test
                        ),
                    ]
                ),
                html.Tr(
                    [
                        html.Th(
                            "Statistique"
                        ),
                        html.Td(
                            f"{statistic:.4f}"
                        ),
                    ]
                ),
                html.Tr(
                    [
                        html.Th(
                            "p-value"
                        ),
                        html.Td(
                            p_display
                        ),
                    ]
                ),
            ]

            if df_text is not None:
                test_rows.append(
                    html.Tr(
                        [
                            html.Th(
                                "Degrés de liberté"
                            ),
                            html.Td(
                                df_text
                            ),
                        ]
                    )
                )

            inference_component = (
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(
                                "Analyse inférentielle",
                                className="card-title",
                            ),

                            html.H6(
                                "Règle décisionnelle EMIDAF",
                                className="mt-3",
                            ),

                            dbc.Table(
                                [
                                    html.Tbody(
                                        [
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        "Approche paramétrique compatible"
                                                    ),
                                                    html.Td(
                                                        parametric_text
                                                    ),
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        "Homogénéité des variances"
                                                    ),
                                                    html.Td(
                                                        variance_text
                                                    ),
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                bordered=True,
                                size="sm",
                                responsive=True,
                            ),

                            html.P(
                                [
                                    html.Strong(
                                        "Justification : "
                                    ),
                                    reason,
                                ],
                                className="mt-3",
                            ),

                            html.H6(
                                "Résultat du test global",
                                className="mt-4",
                            ),

                            dbc.Table(
                                [
                                    html.Tbody(
                                        test_rows
                                    )
                                ],
                                bordered=True,
                                size="sm",
                                responsive=True,
                            ),

                            dbc.Alert(
                                decision,
                                color=decision_color,
                                className="mt-3",
                            ),

                            html.H6(
                                "Taille d'effet",
                                className="mt-4",
                            ),

                            dbc.Table(
                                [
                                    html.Tbody(
                                        effect_rows
                                    )
                                ],
                                bordered=True,
                                size="sm",
                                responsive=True,
                            ),

                            (
                                dbc.Alert(
                                    effect_note,
                                    color="info",
                                    className="mt-2",
                                )
                                if effect_note
                                else html.Div()
                            ),

                            posthoc_component,

                            dbc.Alert(
                                (
                                    "Interprétation : une association "
                                    "ou une différence statistique "
                                    "n'établit pas à elle seule une "
                                    "relation causale. Avec de grands "
                                    "effectifs, une différence peut être "
                                    "statistiquement significative tout "
                                    "en restant faible en pratique."
                                ),
                                color="warning",
                                className="mt-4 mb-0",
                            ),
                        ]
                    ),
                    className="mt-4",
                )
            )

            # ----------------------------------------------
            # Persistance sérialisable
            # ----------------------------------------------

            persistence_inference = {
                "selected_test":
                    selection.get(
                        "selected_test"
                    ),
                "test_name":
                    test_result.test,
                "reason":
                    selection.get(
                        "reason"
                    ),
                "alpha":
                    float(
                        selection.get(
                            "alpha",
                            0.05,
                        )
                    ),
                "number_of_groups":
                    int(
                        selection.get(
                            "number_of_groups",
                            len(groups),
                        )
                    ),
                "parametric_compatible":
                    bool(
                        selection.get(
                            "parametric_compatible"
                        )
                    ),
                "variance_test":
                    selection.get(
                        "variance_test"
                    ),
                "variance_p_value": (
                    None
                    if selection.get(
                        "variance_p_value"
                    ) is None
                    else float(
                        selection[
                            "variance_p_value"
                        ]
                    )
                ),
                "variance_homogeneous":
                    selection.get(
                        "variance_homogeneous"
                    ),
                "statistic":
                    statistic,
                "p_value":
                    p_value,
                "reject_null":
                    significant,
                "effect_size":
                    effect,
                "posthoc":
                    posthoc,
                "group_labels":
                    valid_labels,
                "group_diagnostics":
                    selection.get(
                        "group_diagnostics",
                        [],
                    ),
            }

        except Exception as error:
            inference_component = (
                dbc.Alert(
                    [
                        html.Strong(
                            "Analyse inférentielle indisponible. "
                        ),
                        str(error),
                    ],
                    color="warning",
                    className="mt-4",
                )
            )

            persistence_inference = {
                "error": str(error),
            }

    else:
        inference_component = (
            dbc.Alert(
                (
                    "Analyse inférentielle impossible : "
                    "au moins deux groupes contenant "
                    "suffisamment d'observations sont nécessaires."
                ),
                color="warning",
                className="mt-4",
            )
        )

    # ======================================================
    # PERSISTANCE
    # ======================================================

    persisted_summary = (
        grouped
        .copy()
    )

    # Éviter de persister un dtype Categorical.
    if pd.api.types.is_categorical_dtype(
        persisted_summary[
            group_variable
        ]
    ):
        persisted_summary[
            group_variable
        ] = (
            persisted_summary[
                group_variable
            ]
            .astype(str)
        )

    _persist_elae(
        project_id,
        dataset_id,
        "grouped",
        {
            "group_variable":
                group_variable,
            "value_variable":
                value_variable,
            "summary": (
                persisted_summary
                .round(6)
                .to_dict(
                    orient="records"
                )
            ),
            "inference":
                persistence_inference,
        },
    )

    # ======================================================
    # GRAPHIQUE
    # ======================================================

    figure = px.box(
        temp,
        x=group_variable,
        y=value_variable,
        points="outliers",
        category_orders=category_orders,
        title=(
            f"{value_variable} selon "
            f"{group_variable}"
        ),
    )

    # ======================================================
    # SORTIE
    # ======================================================

    content = html.Div(
        [
            html.H6(
                "Statistiques descriptives",
                className="mb-3",
            ),
            _table(
                display_grouped.round(4)
            ),
            inference_component,
        ]
    )

    return (
        content,
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
        "elae-project-id",
        "data",
    ),
    State(
        "elae-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def download_summary(
    n_clicks,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update

    dataframe = _load_elae_dataframe(
        project_id,
        dataset_id,
    )

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
