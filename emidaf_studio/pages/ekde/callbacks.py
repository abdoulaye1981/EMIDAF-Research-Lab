from __future__ import annotations

from io import StringIO
from typing import Any

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

from sklearn.preprocessing import StandardScaler

from emidaf_core.preprocessing.dimensionality import (
    PCAReduction,
)

from emidaf_core.preprocessing.feature_selection import (
    FeatureSelection,
)


# ============================================================
# UTILITIES
# ============================================================


def _deserialize(data):

    return pd.read_json(
        StringIO(data),
        orient="split",
    )


def _table(dataframe):

    if dataframe is None or dataframe.empty:

        return dbc.Alert(
            "Aucun résultat disponible.",
            color="secondary",
        )

    return dbc.Table.from_dataframe(
        dataframe,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _numeric_like_dataframe(
    dataframe,
    threshold=0.95,
):

    result = {}

    converted_info = []

    for column in dataframe.columns:

        series = dataframe[column]

        if pd.api.types.is_numeric_dtype(series):

            result[column] = pd.to_numeric(
                series,
                errors="coerce",
            )

            continue

        if not (
            pd.api.types.is_object_dtype(series)
            or pd.api.types.is_string_dtype(series)
        ):
            continue

        non_missing = series.dropna()

        if non_missing.empty:
            continue

        converted_non_missing = pd.to_numeric(
            non_missing,
            errors="coerce",
        )

        conversion_rate = (
            converted_non_missing
            .notna()
            .mean()
        )

        if conversion_rate >= threshold:

            result[column] = pd.to_numeric(
                series,
                errors="coerce",
            )

            converted_info.append(
                {
                    "column": column,
                    "conversion_rate": (
                        100 * conversion_rate
                    ),
                }
            )

    numeric = pd.DataFrame(
        result,
        index=dataframe.index,
    )

    return numeric, converted_info


def _prepare_numeric_matrix(dataframe):

    numeric, conversions = (
        _numeric_like_dataframe(
            dataframe
        )
    )

    if numeric.empty:

        return numeric, conversions

    # Retirer les colonnes totalement vides.
    numeric = numeric.dropna(
        axis=1,
        how="all",
    )

    # Imputation médiane temporaire.
    for column in numeric.columns:

        if numeric[column].isna().any():

            median = numeric[column].median()

            if pd.isna(median):
                median = 0.0

            numeric[column] = (
                numeric[column]
                .fillna(median)
            )

    return numeric, conversions


def _result_to_dataframe(result):

    if isinstance(result, pd.DataFrame):
        return result

    if isinstance(result, pd.Series):

        return (
            result
            .rename("Valeur")
            .reset_index()
        )

    if isinstance(result, dict):

        rows = []

        for key, value in result.items():

            if np.isscalar(value) or value is None:

                rows.append(
                    {
                        "Élément": key,
                        "Valeur": value,
                    }
                )

        if rows:
            return pd.DataFrame(rows)

    if isinstance(
        result,
        (
            list,
            tuple,
            np.ndarray,
        ),
    ):

        array = np.asarray(result)

        if array.ndim == 1:

            return pd.DataFrame(
                {
                    "Valeur": array
                }
            )

        if array.ndim == 2:

            return pd.DataFrame(array)

    return pd.DataFrame(
        {
            "Résultat": [
                str(result)
            ]
        }
    )


def _unwrap_transformed(
    result,
    index=None,
):

    if isinstance(result, pd.DataFrame):
        return result

    if isinstance(result, pd.Series):
        return result.to_frame()

    if isinstance(result, tuple):

        for item in result:

            try:
                return _unwrap_transformed(
                    item,
                    index=index,
                )
            except Exception:
                continue

    if isinstance(result, dict):

        for key in (
            "data",
            "X",
            "dataframe",
            "transformed",
            "components",
        ):

            if key in result:

                return _unwrap_transformed(
                    result[key],
                    index=index,
                )

    array = np.asarray(result)

    if array.ndim != 2:

        raise ValueError(
            "Résultat transformé non matriciel."
        )

    return pd.DataFrame(
        array,
        index=index,
    )


def _safe_summary(model):

    try:
        result = model.summary()
    except Exception:
        return {}

    if isinstance(result, dict):
        return result

    if hasattr(result, "__dict__"):
        return dict(result.__dict__)

    return {
        "summary": str(result)
    }


def _extract_explained_variance(
    model,
    summary,
    n_components,
):

    candidates = []

    if isinstance(summary, dict):

        for key in (
            "explained_variance_ratio",
            "explained_variance_ratio_",
            "variance_ratio",
            "explained_variance",
        ):

            value = summary.get(key)

            if value is not None:
                candidates.append(value)

    for attribute in (
        "explained_variance_ratio_",
        "explained_variance_ratio",
    ):

        if hasattr(model, attribute):

            candidates.append(
                getattr(
                    model,
                    attribute,
                )
            )

    inner_model = getattr(
        model,
        "model",
        None,
    )

    if inner_model is None:

        inner_model = getattr(
            model,
            "model_",
            None,
        )

    if inner_model is not None:

        if hasattr(
            inner_model,
            "explained_variance_ratio_",
        ):

            candidates.append(
                inner_model
                .explained_variance_ratio_
            )

    for candidate in candidates:

        try:

            array = np.asarray(
                candidate,
                dtype=float,
            ).reshape(-1)

            if len(array):

                return array[
                    :n_components
                ]

        except Exception:
            continue

    return None


# ============================================================
# STRUCTURE / REDUNDANCY
# ============================================================


@callback(
    Output(
        "ekde-structure-summary",
        "children",
    ),
    Output(
        "ekde-correlation-graph",
        "figure",
    ),
    Input(
        "ekde-correlation-threshold",
        "value",
    ),
    State(
        "ekde-data",
        "data",
    ),
)
def structure_analysis(
    threshold,
    data,
):

    dataframe = _deserialize(data)

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
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

    corr = numeric.corr(
        method="pearson"
    )

    strong_pairs = []

    columns = list(corr.columns)

    for i, column_a in enumerate(columns):

        for j in range(i + 1, len(columns)):

            column_b = columns[j]

            value = corr.loc[
                column_a,
                column_b,
            ]

            if (
                pd.notna(value)
                and abs(value) >= threshold
            ):

                strong_pairs.append(
                    {
                        "Variable 1": column_a,
                        "Variable 2": column_b,
                        "Corrélation": value,
                        "|Corrélation|": abs(value),
                    }
                )

    pairs_df = pd.DataFrame(
        strong_pairs
    )

    if not pairs_df.empty:

        pairs_df = (
            pairs_df
            .sort_values(
                "|Corrélation|",
                ascending=False,
            )
            .round(4)
        )

        result = [
            dbc.Alert(
                (
                    f"{len(pairs_df)} paire(s) "
                    f"avec |r| ≥ {threshold:.2f}."
                ),
                color="info",
            ),
            _table(pairs_df),
        ]

    else:

        result = dbc.Alert(
            (
                "Aucune paire ne dépasse "
                f"le seuil |r| ≥ {threshold:.2f}."
            ),
            color="success",
        )

    figure = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        zmin=-1,
        zmax=1,
        title=(
            "Structure de corrélation "
            "des variables numériques"
        ),
    )

    return result, figure


# ============================================================
# PCA
# ============================================================


@callback(
    Output(
        "ekde-pca-summary",
        "children",
    ),
    Output(
        "ekde-pca-variance-graph",
        "figure",
    ),
    Output(
        "ekde-pca-projection",
        "figure",
    ),
    Input(
        "ekde-pca-components",
        "value",
    ),
    State(
        "ekde-data",
        "data",
    ),
)
def pca_analysis(
    n_components,
    data,
):

    dataframe = _deserialize(data)

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.shape[1] < 2:

        message = dbc.Alert(
            (
                "La PCA nécessite au moins "
                "deux variables numériques."
            ),
            color="warning",
        )

        return message, {}, {}

    n_components = int(
        min(
            max(2, n_components or 2),
            numeric.shape[1],
            numeric.shape[0],
        )
    )

    # La PCA dépend de l'échelle.
    scaler = StandardScaler()

    standardized = pd.DataFrame(
        scaler.fit_transform(
            numeric
        ),
        columns=numeric.columns,
        index=numeric.index,
    )

    model = PCAReduction(
        n_components=n_components
    )

    transformed = model.fit_transform(
        standardized
    )

    components = _unwrap_transformed(
        transformed,
        index=numeric.index,
    )

    components.columns = [
        f"PC{i + 1}"
        for i in range(
            components.shape[1]
        )
    ]

    summary = _safe_summary(model)

    variance_ratio = (
        _extract_explained_variance(
            model,
            summary,
            n_components,
        )
    )

    if variance_ratio is not None:

        variance_df = pd.DataFrame(
            {
                "Composante": [
                    f"PC{i + 1}"
                    for i in range(
                        len(variance_ratio)
                    )
                ],
                "Variance expliquée": (
                    variance_ratio
                ),
            }
        )

        variance_df[
            "Variance cumulée"
        ] = (
            variance_df[
                "Variance expliquée"
            ]
            .cumsum()
        )

        variance_figure = px.bar(
            variance_df,
            x="Composante",
            y="Variance expliquée",
            title=(
                "Variance expliquée "
                "par composante"
            ),
        )

        cumulative = (
            100
            * variance_df[
                "Variance cumulée"
            ].iloc[-1]
        )

        summary_content = [
            dbc.Alert(
                (
                    f"{n_components} composantes "
                    f"expliquent environ "
                    f"{cumulative:.2f} % "
                    "de la variance."
                ),
                color="info",
            ),

            _table(
                variance_df.assign(
                    **{
                        "Variance expliquée": (
                            100
                            * variance_df[
                                "Variance expliquée"
                            ]
                        ),
                        "Variance cumulée": (
                            100
                            * variance_df[
                                "Variance cumulée"
                            ]
                        ),
                    }
                ).round(4)
            ),
        ]

    else:

        variance_figure = {}

        summary_content = [
            dbc.Alert(
                (
                    "Projection PCA calculée. "
                    "Le backend n'a pas exposé "
                    "la variance expliquée sous "
                    "une forme reconnue par Studio."
                ),
                color="warning",
            ),
            _table(
                _result_to_dataframe(
                    summary
                )
            ),
        ]

    projection = components.copy()

    projection["Observation"] = (
        np.arange(
            1,
            len(projection) + 1,
        )
    )

    projection_figure = px.scatter(
        projection,
        x="PC1",
        y="PC2",
        hover_data=["Observation"],
        title=(
            "Projection des observations "
            "sur le premier plan factoriel"
        ),
    )

    return (
        summary_content,
        variance_figure,
        projection_figure,
    )


# ============================================================
# ASSOCIATIONS
# ============================================================


@callback(
    Output(
        "ekde-association-results",
        "children",
    ),
    Output(
        "ekde-association-graph",
        "figure",
    ),
    Input(
        "ekde-association-x",
        "value",
    ),
    Input(
        "ekde-association-y",
        "value",
    ),
    State(
        "ekde-data",
        "data",
    ),
)
def association_analysis(
    x,
    y,
    data,
):

    dataframe = _deserialize(data)

    if (
        not x
        or not y
        or x == y
        or x not in dataframe.columns
        or y not in dataframe.columns
    ):

        return (
            dbc.Alert(
                (
                    "Sélectionnez deux variables "
                    "différentes."
                ),
                color="warning",
            ),
            {},
        )

    pair = dataframe[
        [x, y]
    ].copy()

    pair[x] = pd.to_numeric(
        pair[x],
        errors="coerce",
    )

    pair[y] = pd.to_numeric(
        pair[y],
        errors="coerce",
    )

    pair = pair.dropna()

    if len(pair) < 3:

        return (
            dbc.Alert(
                "Données insuffisantes.",
                color="warning",
            ),
            {},
        )

    pearson = pair[x].corr(
        pair[y],
        method="pearson",
    )

    spearman = pair[x].corr(
        pair[y],
        method="spearman",
    )

    # Information mutuelle à travers le backend
    # FeatureSelection.
    try:

        X = pair[[x]]

        y_values = pair[y]

        mi_result = (
            FeatureSelection
            .mutual_information_regression(
                X,
                y_values,
                k=1,
            )
        )

        mi_df = _result_to_dataframe(
            mi_result
        )

        mi_text = str(
            mi_df.iloc[0].to_dict()
        )

    except Exception as exc:

        mi_text = (
            "Non disponible : "
            f"{exc}"
        )

    metrics = pd.DataFrame(
        {
            "Mesure": [
                "Corrélation de Pearson",
                "Corrélation de Spearman",
                "Information mutuelle",
            ],
            "Résultat": [
                round(
                    float(pearson),
                    4,
                ),
                round(
                    float(spearman),
                    4,
                ),
                mi_text,
            ],
        }
    )

    figure = px.scatter(
        pair,
        x=x,
        y=y,
        title=(
            f"Relation entre {x} et {y}"
        ),
    )

    return (
        _table(metrics),
        figure,
    )


# ============================================================
# FEATURE SELECTION
# ============================================================


@callback(
    Output(
        "ekde-selection-results",
        "children",
    ),
    Input(
        "ekde-selection-run",
        "n_clicks",
    ),
    State(
        "ekde-selection-method",
        "value",
    ),
    State(
        "ekde-target",
        "value",
    ),
    State(
        "ekde-variance-threshold",
        "value",
    ),
    State(
        "ekde-data",
        "data",
    ),
    prevent_initial_call=True,
)
def selection_analysis(
    n_clicks,
    method,
    target,
    variance_threshold,
    data,
):

    if not n_clicks:
        return no_update

    dataframe = _deserialize(data)

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.empty:

        return dbc.Alert(
            "Aucune variable numérique exploitable.",
            color="warning",
        )

    try:

        if method == "variance":

            threshold = float(
                variance_threshold or 0.0
            )

            result = (
                FeatureSelection
                .variance_threshold(
                    numeric,
                    threshold=threshold,
                )
            )

        else:

            if (
                not target
                or target not in dataframe.columns
            ):

                return dbc.Alert(
                    (
                        "Une variable cible est "
                        "nécessaire pour cette méthode."
                    ),
                    color="warning",
                )

            y = dataframe[target]

            X = numeric.drop(
                columns=[target],
                errors="ignore",
            )

            valid = y.notna()

            X = X.loc[valid]
            y = y.loc[valid]

            if X.empty:

                return dbc.Alert(
                    (
                        "Aucune variable prédictive "
                        "numérique disponible."
                    ),
                    color="warning",
                )

            if method == "correlation":

                y_numeric = pd.to_numeric(
                    y,
                    errors="coerce",
                )

                valid_numeric = (
                    y_numeric.notna()
                )

                X = X.loc[
                    valid_numeric
                ]

                y_numeric = y_numeric.loc[
                    valid_numeric
                ]

                result = (
                    FeatureSelection
                    .compare_correlations(
                        X,
                        y_numeric,
                    )
                )

            elif method == "mi_classification":

                y_class = (
                    y.astype(str)
                )

                k = min(
                    10,
                    X.shape[1],
                )

                result = (
                    FeatureSelection
                    .mutual_information_classification(
                        X,
                        y_class,
                        k=k,
                    )
                )

            elif method == "mi_regression":

                y_numeric = pd.to_numeric(
                    y,
                    errors="coerce",
                )

                valid_numeric = (
                    y_numeric.notna()
                )

                X = X.loc[
                    valid_numeric
                ]

                y_numeric = y_numeric.loc[
                    valid_numeric
                ]

                k = min(
                    10,
                    X.shape[1],
                )

                result = (
                    FeatureSelection
                    .mutual_information_regression(
                        X,
                        y_numeric,
                        k=k,
                    )
                )

            else:

                return dbc.Alert(
                    "Méthode inconnue.",
                    color="danger",
                )

        result_df = (
            _result_to_dataframe(
                result
            )
        )

        return [
            dbc.Alert(
                "Analyse de sélection terminée.",
                color="success",
            ),
            _table(
                result_df
            ),
        ]

    except Exception as exc:

        return dbc.Alert(
            [
                html.Strong(
                    "La méthode n'a pas pu être calculée : "
                ),
                str(exc),
            ],
            color="danger",
        )


# ============================================================
# KNOWLEDGE SUMMARY
# ============================================================


@callback(
    Output(
        "ekde-knowledge-summary",
        "children",
    ),
    Input(
        "ekde-data",
        "data",
    ),
)
def knowledge_summary(data):

    dataframe = _deserialize(data)

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    findings = []

    findings.append(
        html.Li(
            (
                f"{numeric.shape[1]} variable(s) "
                "numérique(s) ou numeric-like "
                "sont exploitables pour les analyses "
                "multivariées."
            )
        )
    )

    if conversions:

        findings.append(
            html.Li(
                (
                    "Variables numeric-like identifiées : "
                    + ", ".join(
                        item["column"]
                        for item in conversions
                    )
                    + "."
                )
            )
        )

    if numeric.shape[1] >= 2:

        corr = numeric.corr()

        strong = []

        for i, column_a in enumerate(
            corr.columns
        ):

            for j in range(
                i + 1,
                len(corr.columns),
            ):

                column_b = corr.columns[j]

                value = corr.loc[
                    column_a,
                    column_b,
                ]

                if (
                    pd.notna(value)
                    and abs(value) >= 0.90
                ):

                    strong.append(
                        (
                            column_a,
                            column_b,
                            value,
                        )
                    )

        if strong:

            findings.append(
                html.Li(
                    (
                        f"{len(strong)} association(s) "
                        "linéaire(s) forte(s) "
                        "(|r| ≥ 0,90) détectée(s). "
                        "Elles peuvent signaler une "
                        "redondance entre variables."
                    )
                )
            )

        else:

            findings.append(
                html.Li(
                    (
                        "Aucune redondance linéaire "
                        "forte n'est détectée au seuil "
                        "|r| ≥ 0,90."
                    )
                )
            )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Connaissances automatiquement dégagées"
                ),

                html.Ul(findings),

                html.Hr(),

                html.Small(
                    (
                        "Ces éléments sont des diagnostics "
                        "exploratoires. Une association ou "
                        "une composante latente ne constitue "
                        "pas, à elle seule, une relation "
                        "causale."
                    ),
                    className="text-muted",
                ),
            ]
        )
    )


# ============================================================
# EXPORT
# ============================================================


@callback(
    Output(
        "ekde-download-data",
        "data",
    ),
    Input(
        "ekde-download",
        "n_clicks",
    ),
    State(
        "ekde-data",
        "data",
    ),
    prevent_initial_call=True,
)
def export_knowledge(
    n_clicks,
    data,
):

    if not n_clicks:
        return no_update

    dataframe = _deserialize(data)

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    rows = [
        {
            "Indicateur": "Observations",
            "Valeur": dataframe.shape[0],
        },
        {
            "Indicateur": "Variables",
            "Valeur": dataframe.shape[1],
        },
        {
            "Indicateur": (
                "Variables numériques/numeric-like"
            ),
            "Valeur": numeric.shape[1],
        },
        {
            "Indicateur": (
                "Conversions numeric-like"
            ),
            "Valeur": ", ".join(
                item["column"]
                for item in conversions
            ),
        },
    ]

    report = pd.DataFrame(rows)

    return dcc.send_data_frame(
        report.to_csv,
        "ekde_connaissances.csv",
        index=False,
    )
