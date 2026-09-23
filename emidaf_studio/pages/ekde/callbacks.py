from __future__ import annotations

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

from dash.exceptions import PreventUpdate

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)

from emidaf_studio.services.model_registry import (
    merge_analysis_section,
)

from sklearn.preprocessing import StandardScaler

from emidaf_core.preprocessing.dimensionality import (
    PCAReduction,
    TSNEReduction,
    UMAPReduction,
)

from emidaf_core.preprocessing.feature_selection import (
    FeatureSelection,
)

from emidaf_core.ekde import (
    KMeansClustering,
    DBSCANClustering,
    AgglomerativeClusteringEngine,
)


# ============================================================
# UTILITIES
# ============================================================


def _load_ekde_dataframe(
    project_id,
    dataset_id,
):
    """
    Charge le dataset EKDE côté serveur.

    Le navigateur ne doit à terme conserver que
    project_id et dataset_id, jamais le DataFrame complet.
    """
    _, _, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        raise PreventUpdate

    if not isinstance(result, pd.DataFrame):
        raise PreventUpdate

    return result


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


def _persist_ekde(
    project_id,
    dataset_id,
    section,
    payload,
):
    """
    Persiste atomiquement une sous-section EKDE
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
        "ekde",
        section,
        payload,
    )


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
        "ekde-structure-run",
        "n_clicks",
    ),
    State(
        "ekde-correlation-threshold",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def structure_analysis(
    n_clicks,
    threshold,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

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

    _persist_ekde(
        project_id,
        dataset_id,
        "structure",
        {
            "threshold": float(threshold),
            "numeric_variables": list(corr.columns),
            "converted_columns": conversions,
            "strong_pairs": (
                pairs_df.to_dict(
                    orient="records"
                )
                if not pairs_df.empty
                else []
            ),
            "correlation_matrix": (
                corr
                .round(6)
                .to_dict()
            ),
        },
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
        "ekde-pca-run",
        "n_clicks",
    ),
    State(
        "ekde-pca-components",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def pca_analysis(
    n_clicks,
    n_components,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
        )

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

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

    summary_df = _result_to_dataframe(
        summary
    )

    pca_payload = {
        "n_components": int(n_components),
        "numeric_variables": (
            list(numeric.columns)
        ),
        "converted_columns": conversions,
        "summary": (
            summary_df
            .to_dict(
                orient="records"
            )
        ),
    }

    if variance_ratio is not None:

        pca_payload[
            "explained_variance"
        ] = (
            variance_df
            .assign(
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
            )
            .round(6)
            .to_dict(
                orient="records"
            )
        )

        pca_payload[
            "cumulative_variance_percent"
        ] = round(
            float(cumulative),
            6,
        )

    _persist_ekde(
        project_id,
        dataset_id,
        "pca",
        pca_payload,
    )

    return (
        summary_content,
        variance_figure,
        projection_figure,
    )


# ============================================================
# t-SNE
# ============================================================


@callback(
    Output(
        "ekde-tsne-summary",
        "children",
    ),
    Output(
        "ekde-tsne-projection",
        "figure",
    ),
    Input(
        "ekde-tsne-run",
        "n_clicks",
    ),
    State(
        "ekde-tsne-perplexity",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def tsne_analysis(
    n_clicks,
    perplexity,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.shape[1] < 2:
        return (
            dbc.Alert(
                (
                    "t-SNE nécessite au moins "
                    "deux variables numériques."
                ),
                color="warning",
            ),
            {},
        )

    n_observations = int(
        numeric.shape[0]
    )

    if n_observations < 3:
        return (
            dbc.Alert(
                (
                    "t-SNE nécessite au moins "
                    "trois observations."
                ),
                color="warning",
            ),
            {},
        )

    try:
        requested_perplexity = float(
            perplexity
            if perplexity is not None
            else 30.0
        )
    except (TypeError, ValueError):
        requested_perplexity = 30.0

    # sklearn impose perplexity < n_samples.
    effective_perplexity = min(
        max(
            1.0,
            requested_perplexity,
        ),
        float(
            n_observations - 1
        ),
    )

    # t-SNE dépend fortement de l'échelle.
    scaler = StandardScaler()

    standardized = pd.DataFrame(
        scaler.fit_transform(
            numeric
        ),
        columns=numeric.columns,
        index=numeric.index,
    )

    try:
        model = TSNEReduction(
            n_components=2,
            perplexity=effective_perplexity,
        )

        transformed = model.fit_transform(
            standardized
        )

        components = _unwrap_transformed(
            transformed,
            index=numeric.index,
        )

    except Exception as exc:
        return (
            dbc.Alert(
                (
                    "Le calcul t-SNE n'a pas "
                    f"pu être terminé : {exc}"
                ),
                color="danger",
            ),
            {},
        )

    components.columns = [
        "TSNE1",
        "TSNE2",
    ]

    projection = components.copy()

    projection["Observation"] = np.arange(
        1,
        len(projection) + 1,
    )

    projection_figure = px.scatter(
        projection,
        x="TSNE1",
        y="TSNE2",
        hover_data=["Observation"],
        title=(
            "Projection t-SNE "
            "des observations"
        ),
    )

    summary_df = pd.DataFrame(
        [
            {
                "Indicateur": "Observations",
                "Valeur": n_observations,
            },
            {
                "Indicateur": "Variables utilisées",
                "Valeur": int(
                    numeric.shape[1]
                ),
            },
            {
                "Indicateur": "Perplexité demandée",
                "Valeur": requested_perplexity,
            },
            {
                "Indicateur": "Perplexité utilisée",
                "Valeur": effective_perplexity,
            },
        ]
    )

    summary_content = [
        dbc.Alert(
            (
                "Projection t-SNE calculée "
                "sur les variables numériques "
                "standardisées."
            ),
            color="info",
        ),
        _table(summary_df),
        dbc.Alert(
            (
                "t-SNE vise principalement à "
                "préserver les structures locales. "
                "Les distances globales entre "
                "groupes et leur taille apparente "
                "ne doivent pas être interprétées "
                "comme des mesures quantitatives "
                "directes de similarité."
            ),
            color="secondary",
        ),
    ]

    _persist_ekde(
        project_id,
        dataset_id,
        "tsne",
        {
            "n_components": 2,
            "n_observations": n_observations,
            "numeric_variables": (
                list(numeric.columns)
            ),
            "converted_columns": conversions,
            "requested_perplexity": float(
                requested_perplexity
            ),
            "effective_perplexity": float(
                effective_perplexity
            ),
            "standardized": True,
        },
    )

    return (
        summary_content,
        projection_figure,
    )


# ============================================================
# UMAP
# ============================================================


@callback(
    Output(
        "ekde-umap-summary",
        "children",
    ),
    Output(
        "ekde-umap-projection",
        "figure",
    ),
    Input(
        "ekde-umap-run",
        "n_clicks",
    ),
    State(
        "ekde-umap-neighbors",
        "value",
    ),
    State(
        "ekde-umap-min-dist",
        "value",
    ),
    State(
        "ekde-umap-metric",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def umap_analysis(
    n_clicks,
    n_neighbors,
    min_dist,
    metric,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.shape[1] < 2:
        return (
            dbc.Alert(
                (
                    "UMAP nécessite au moins "
                    "deux variables numériques."
                ),
                color="warning",
            ),
            {},
        )

    n_observations = int(
        numeric.shape[0]
    )

    if n_observations < 3:
        return (
            dbc.Alert(
                (
                    "UMAP nécessite au moins "
                    "trois observations."
                ),
                color="warning",
            ),
            {},
        )

    try:
        requested_neighbors = int(
            n_neighbors
            if n_neighbors is not None
            else 15
        )
    except (TypeError, ValueError):
        requested_neighbors = 15

    try:
        requested_min_dist = float(
            min_dist
            if min_dist is not None
            else 0.1
        )
    except (TypeError, ValueError):
        requested_min_dist = 0.1

    requested_metric = (
        metric
        if metric is not None
        else "euclidean"
    )

    allowed_metrics = {
        "euclidean",
        "manhattan",
        "cosine",
    }

    if requested_metric not in allowed_metrics:
        return (
            dbc.Alert(
                "Métrique UMAP non reconnue.",
                color="warning",
            ),
            {},
        )

    effective_neighbors = min(
        max(
            2,
            requested_neighbors,
        ),
        n_observations - 1,
    )

    if requested_min_dist < 0:
        return (
            dbc.Alert(
                (
                    "min_dist doit être "
                    "supérieur ou égal à 0."
                ),
                color="warning",
            ),
            {},
        )

    scaler = StandardScaler()

    standardized = pd.DataFrame(

        scaler.fit_transform(

            numeric

        ).astype(

            np.float32,

            copy=False,

        ),

        columns=numeric.columns,

        index=numeric.index,

    )

    try:
        model = UMAPReduction(
            n_components=2,
            n_neighbors=(
                effective_neighbors
            ),
            min_dist=(
                requested_min_dist
            ),
            metric=(
                requested_metric
            ),
            random_state=42,
        )

        components = (
            model.fit_transform(
                standardized
            )
        )

    except Exception as exc:
        return (
            dbc.Alert(
                (
                    "Le calcul UMAP n'a pas "
                    "pu être terminé : "
                    f"{exc}"
                ),
                color="danger",
            ),
            {},
        )

    projection = components.copy()

    projection["Observation"] = (
        np.arange(
            1,
            len(projection) + 1,
        )
    )

    projection_figure = px.scatter(
        projection,
        x="UMAP1",
        y="UMAP2",
        hover_data=["Observation"],
        title=(
            "Projection UMAP "
            "des observations"
        ),
    )

    summary_df = pd.DataFrame(
        [
            {
                "Indicateur":
                    "Observations",
                "Valeur":
                    n_observations,
            },
            {
                "Indicateur":
                    "Variables utilisées",
                "Valeur":
                    int(
                        numeric.shape[1]
                    ),
            },
            {
                "Indicateur":
                    "n_neighbors demandé",
                "Valeur":
                    requested_neighbors,
            },
            {
                "Indicateur":
                    "n_neighbors utilisé",
                "Valeur":
                    effective_neighbors,
            },
            {
                "Indicateur":
                    "min_dist",
                "Valeur":
                    requested_min_dist,
            },
            {
                "Indicateur":
                    "Métrique",
                "Valeur":
                    requested_metric,
            },
        ]
    )

    summary_content = [
        dbc.Alert(
            (
                "Projection UMAP calculée "
                "sur les variables numériques "
                "standardisées."
            ),
            color="info",
        ),
        _table(summary_df),
        dbc.Alert(
            (
                "UMAP cherche à préserver "
                "principalement les structures "
                "locales tout en conservant "
                "une partie de l'organisation "
                "globale. Les distances et "
                "séparations visibles dans la "
                "projection doivent néanmoins "
                "être interprétées avec "
                "prudence."
            ),
            color="secondary",
        ),
    ]

    _persist_ekde(
        project_id,
        dataset_id,
        "umap",
        {
            "n_components": 2,
            "n_observations": (
                n_observations
            ),
            "numeric_variables": (
                list(numeric.columns)
            ),
            "converted_columns": (
                conversions
            ),
            "standardized": True,
            "requested_neighbors": (
                requested_neighbors
            ),
            "effective_neighbors": (
                effective_neighbors
            ),
            "min_dist": (
                requested_min_dist
            ),
            "metric": (
                requested_metric
            ),
        },
    )

    return (
        summary_content,
        projection_figure,
    )


# ============================================================
# K-MEANS CLUSTERING
# ============================================================


@callback(
    Output(
        "ekde-kmeans-summary",
        "children",
    ),
    Output(
        "ekde-kmeans-projection",
        "figure",
    ),
    Input(
        "ekde-kmeans-run",
        "n_clicks",
    ),
    State(
        "ekde-kmeans-clusters",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def kmeans_analysis(
    n_clicks,
    n_clusters,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.shape[1] < 1:
        return (
            dbc.Alert(
                (
                    "K-Means nécessite au moins "
                    "une variable numérique."
                ),
                color="warning",
            ),
            {},
        )

    n_observations = int(
        numeric.shape[0]
    )

    if n_observations < 3:
        return (
            dbc.Alert(
                (
                    "K-Means nécessite au moins "
                    "trois observations pour "
                    "cette analyse."
                ),
                color="warning",
            ),
            {},
        )

    try:
        requested_clusters = int(
            n_clusters
            if n_clusters is not None
            else 3
        )
    except (TypeError, ValueError):
        requested_clusters = 3

    if (
        requested_clusters < 2
        or requested_clusters
        >= n_observations
    ):
        return (
            dbc.Alert(
                (
                    "Le nombre de clusters doit "
                    "être au moins égal à 2 et "
                    "strictement inférieur au "
                    "nombre d'observations."
                ),
                color="warning",
            ),
            {},
        )

    # K-Means dépend de l'échelle :
    # standardisation analytique temporaire.
    scaler = StandardScaler()

    standardized = pd.DataFrame(
        scaler.fit_transform(
            numeric
        ),
        columns=numeric.columns,
        index=numeric.index,
    )

    try:
        result = KMeansClustering.fit(
            standardized,
            n_clusters=requested_clusters,
            random_state=42,
        )

    except Exception as exc:
        return (
            dbc.Alert(
                (
                    "Le clustering K-Means "
                    "n'a pas pu être terminé : "
                    f"{exc}"
                ),
                color="danger",
            ),
            {},
        )

    labels = pd.Series(
        result.predictions,
        index=standardized.index,
        name="Cluster",
    )

    cluster_sizes = (
        labels
        .value_counts()
        .sort_index()
        .rename_axis("Cluster")
        .reset_index(name="Effectif")
    )

    cluster_sizes[
        "Cluster"
    ] = cluster_sizes[
        "Cluster"
    ].astype(int) + 1

    cluster_sizes[
        "Pourcentage"
    ] = (
        100
        * cluster_sizes["Effectif"]
        / n_observations
    ).round(2)

    metrics_df = pd.DataFrame(
        [
            {
                "Métrique": "Nombre de clusters",
                "Valeur": requested_clusters,
            },
            {
                "Métrique": "Inertie",
                "Valeur": round(
                    float(result.inertia),
                    6,
                ),
            },
            {
                "Métrique": "Silhouette",
                "Valeur": (
                    round(
                        float(
                            result.silhouette_score
                        ),
                        6,
                    )
                    if (
                        result.silhouette_score
                        is not None
                    )
                    else None
                ),
            },
            {
                "Métrique": "Davies-Bouldin",
                "Valeur": (
                    round(
                        float(
                            result.davies_bouldin_score
                        ),
                        6,
                    )
                    if (
                        result.davies_bouldin_score
                        is not None
                    )
                    else None
                ),
            },
            {
                "Métrique": "Calinski-Harabasz",
                "Valeur": (
                    round(
                        float(
                            result.calinski_harabasz_score
                        ),
                        6,
                    )
                    if (
                        result.calinski_harabasz_score
                        is not None
                    )
                    else None
                ),
            },
        ]
    )

    # Projection PCA utilisée uniquement
    # pour la visualisation du clustering.
    if standardized.shape[1] >= 2:
        projection_model = PCAReduction(
            n_components=2
        )

        transformed = (
            projection_model.fit_transform(
                standardized
            )
        )

        projection = _unwrap_transformed(
            transformed,
            index=standardized.index,
        )

        projection.columns = [
            "Dimension 1",
            "Dimension 2",
        ]

    else:
        projection = pd.DataFrame(
            {
                "Dimension 1":
                    standardized.iloc[:, 0],
                "Dimension 2":
                    np.zeros(
                        n_observations
                    ),
            },
            index=standardized.index,
        )

    projection["Cluster"] = (
        labels
        .astype(int)
        .add(1)
        .astype(str)
    )

    projection["Observation"] = (
        np.arange(
            1,
            n_observations + 1,
        )
    )

    projection_figure = px.scatter(
        projection,
        x="Dimension 1",
        y="Dimension 2",
        color="Cluster",
        hover_data=["Observation"],
        title=(
            "Projection 2D des clusters K-Means"
        ),
    )

    summary_content = [
        dbc.Alert(
            (
                "Clustering K-Means calculé sur "
                "les variables numériques après "
                "standardisation analytique "
                "temporaire."
            ),
            color="info",
        ),
        html.H6(
            "Métriques du partitionnement",
            className="mt-3",
        ),
        _table(metrics_df),
        html.H6(
            "Effectifs par cluster",
            className="mt-4",
        ),
        _table(cluster_sizes),
        dbc.Alert(
            (
                "La projection 2D est une "
                "représentation destinée à la "
                "visualisation. Lorsqu'il existe "
                "au moins deux variables, elle "
                "est obtenue par PCA et ne "
                "modifie pas le clustering "
                "K-Means calculé dans l'espace "
                "standardisé complet."
            ),
            color="secondary",
        ),
        dbc.Alert(
            (
                "Les métriques aident à comparer "
                "des partitionnements. Elles ne "
                "suffisent pas, à elles seules, "
                "à établir qu'un nombre de "
                "clusters est scientifiquement "
                "optimal."
            ),
            color="secondary",
        ),
    ]

    _persist_ekde(
        project_id,
        dataset_id,
        "kmeans",
        {
            "n_clusters": (
                requested_clusters
            ),
            "n_observations": (
                n_observations
            ),
            "numeric_variables": (
                list(numeric.columns)
            ),
            "converted_columns": (
                conversions
            ),
            "standardized": True,
            "inertia": (
                float(result.inertia)
            ),
            "silhouette_score": (
                result.silhouette_score
            ),
            "davies_bouldin_score": (
                result.davies_bouldin_score
            ),
            "calinski_harabasz_score": (
                result.calinski_harabasz_score
            ),
            "cluster_sizes": (
                cluster_sizes
                .to_dict(
                    orient="records"
                )
            ),
            "labels": (
                [
                    int(value) + 1
                    for value
                    in result.predictions
                ]
            ),
            "cluster_centers": (
                result.cluster_centers
            ),
        },
    )

    return (
        summary_content,
        projection_figure,
    )


# ============================================================
# DBSCAN CLUSTERING
# ============================================================


@callback(
    Output(
        "ekde-dbscan-summary",
        "children",
    ),
    Output(
        "ekde-dbscan-projection",
        "figure",
    ),
    Input(
        "ekde-dbscan-run",
        "n_clicks",
    ),
    State(
        "ekde-dbscan-eps",
        "value",
    ),
    State(
        "ekde-dbscan-min-samples",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def dbscan_analysis(
    n_clicks,
    eps,
    min_samples,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.shape[1] < 1:
        return (
            dbc.Alert(
                (
                    "DBSCAN nécessite au moins "
                    "une variable numérique."
                ),
                color="warning",
            ),
            {},
        )

    n_observations = int(
        numeric.shape[0]
    )

    if n_observations < 3:
        return (
            dbc.Alert(
                (
                    "DBSCAN nécessite au moins "
                    "trois observations pour "
                    "cette analyse."
                ),
                color="warning",
            ),
            {},
        )

    try:
        requested_eps = float(
            eps
            if eps is not None
            else 0.5
        )
    except (TypeError, ValueError):
        requested_eps = 0.5

    try:
        requested_min_samples = int(
            min_samples
            if min_samples is not None
            else 5
        )
    except (TypeError, ValueError):
        requested_min_samples = 5

    if requested_eps <= 0:
        return (
            dbc.Alert(
                (
                    "eps doit être strictement "
                    "positif."
                ),
                color="warning",
            ),
            {},
        )

    if (
        requested_min_samples < 2
        or requested_min_samples
        > n_observations
    ):
        return (
            dbc.Alert(
                (
                    "min_samples doit être au "
                    "moins égal à 2 et ne peut "
                    "pas dépasser le nombre "
                    "d'observations."
                ),
                color="warning",
            ),
            {},
        )

    # DBSCAN est sensible aux échelles.
    scaler = StandardScaler()

    standardized = pd.DataFrame(
        scaler.fit_transform(
            numeric
        ),
        columns=numeric.columns,
        index=numeric.index,
    )

    try:
        result = DBSCANClustering.fit(
            standardized,
            eps=requested_eps,
            min_samples=(
                requested_min_samples
            ),
        )

    except Exception as exc:
        return (
            dbc.Alert(
                (
                    "Le clustering DBSCAN "
                    "n'a pas pu être terminé : "
                    f"{exc}"
                ),
                color="danger",
            ),
            {},
        )

    labels = pd.Series(
        result.predictions,
        index=standardized.index,
        name="Cluster",
    )

    n_clusters = int(
        result.parameters[
            "n_clusters"
        ]
    )

    noise_count = int(
        result.parameters[
            "noise_count"
        ]
    )

    noise_percentage = float(
        result.parameters[
            "noise_percentage"
        ]
    )

    def _label_name(value):
        value = int(value)

        if value == -1:
            return "Bruit"

        return f"Cluster {value + 1}"

    display_labels = labels.map(
        _label_name
    )

    cluster_sizes = (
        display_labels
        .value_counts()
        .rename_axis("Groupe")
        .reset_index(name="Effectif")
    )

    cluster_sizes[
        "Pourcentage"
    ] = (
        100
        * cluster_sizes["Effectif"]
        / n_observations
    ).round(2)

    def _metric_value(value):
        if value is None:
            return None

        return round(
            float(value),
            6,
        )

    metrics_df = pd.DataFrame(
        [
            {
                "Métrique":
                    "Clusters détectés",
                "Valeur": n_clusters,
            },
            {
                "Métrique":
                    "Observations bruit",
                "Valeur": noise_count,
            },
            {
                "Métrique":
                    "Bruit (%)",
                "Valeur": round(
                    noise_percentage,
                    2,
                ),
            },
            {
                "Métrique":
                    "Silhouette",
                "Valeur": _metric_value(
                    result.silhouette_score
                ),
            },
            {
                "Métrique":
                    "Davies-Bouldin",
                "Valeur": _metric_value(
                    result.davies_bouldin_score
                ),
            },
            {
                "Métrique":
                    "Calinski-Harabasz",
                "Valeur": _metric_value(
                    result.calinski_harabasz_score
                ),
            },
        ]
    )

    # PCA uniquement pour la visualisation.
    if standardized.shape[1] >= 2:
        projection_model = PCAReduction(
            n_components=2
        )

        transformed = (
            projection_model.fit_transform(
                standardized
            )
        )

        projection = _unwrap_transformed(
            transformed,
            index=standardized.index,
        )

        projection.columns = [
            "Dimension 1",
            "Dimension 2",
        ]

    else:
        projection = pd.DataFrame(
            {
                "Dimension 1":
                    standardized.iloc[:, 0],
                "Dimension 2":
                    np.zeros(
                        n_observations
                    ),
            },
            index=standardized.index,
        )

    projection["Groupe"] = (
        display_labels
    )

    projection["Observation"] = (
        np.arange(
            1,
            n_observations + 1,
        )
    )

    projection_figure = px.scatter(
        projection,
        x="Dimension 1",
        y="Dimension 2",
        color="Groupe",
        hover_data=["Observation"],
        title=(
            "Projection 2D des groupes DBSCAN"
        ),
    )

    summary_content = [
        dbc.Alert(
            (
                "DBSCAN a été exécuté sur "
                "les variables numériques "
                "standardisées."
            ),
            color="info",
        ),
        html.H6(
            "Résumé du partitionnement",
            className="mt-3",
        ),
        _table(metrics_df),
        html.H6(
            "Effectifs par groupe",
            className="mt-4",
        ),
        _table(cluster_sizes),
    ]

    if n_clusters < 2:
        summary_content.append(
            dbc.Alert(
                (
                    "DBSCAN n'a pas identifié "
                    "au moins deux clusters "
                    "distincts. Les métriques "
                    "comparatives de clustering "
                    "ne sont donc pas calculées."
                ),
                color="warning",
            )
        )

    summary_content.extend(
        [
            dbc.Alert(
                (
                    "Le groupe « Bruit » "
                    "correspond aux observations "
                    "étiquetées -1 par DBSCAN. "
                    "Ces observations ne sont "
                    "pas automatiquement "
                    "considérées comme des "
                    "erreurs ou supprimées."
                ),
                color="secondary",
            ),
            dbc.Alert(
                (
                    "La projection PCA sert "
                    "uniquement à la "
                    "visualisation. DBSCAN est "
                    "calculé dans l'espace "
                    "standardisé complet."
                ),
                color="secondary",
            ),
        ]
    )

    _persist_ekde(
        project_id,
        dataset_id,
        "dbscan",
        {
            "eps": requested_eps,
            "min_samples": (
                requested_min_samples
            ),
            "n_observations": (
                n_observations
            ),
            "n_clusters": n_clusters,
            "noise_count": noise_count,
            "noise_percentage": (
                noise_percentage
            ),
            "numeric_variables": (
                list(numeric.columns)
            ),
            "converted_columns": (
                conversions
            ),
            "standardized": True,
            "silhouette_score": (
                result.silhouette_score
            ),
            "davies_bouldin_score": (
                result.davies_bouldin_score
            ),
            "calinski_harabasz_score": (
                result.calinski_harabasz_score
            ),
            "cluster_sizes": (
                cluster_sizes
                .to_dict(
                    orient="records"
                )
            ),
            "labels": (
                [
                    int(value)
                    for value
                    in result.predictions
                ]
            ),
        },
    )

    return (
        summary_content,
        projection_figure,
    )


# ============================================================
# AGGLOMERATIVE CLUSTERING
# ============================================================


@callback(
    Output(
        "ekde-agglomerative-summary",
        "children",
    ),
    Output(
        "ekde-agglomerative-projection",
        "figure",
    ),
    Input(
        "ekde-agglomerative-run",
        "n_clicks",
    ),
    State(
        "ekde-agglomerative-clusters",
        "value",
    ),
    State(
        "ekde-agglomerative-linkage",
        "value",
    ),
    State(
        "ekde-agglomerative-metric",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def agglomerative_analysis(
    n_clicks,
    n_clusters,
    linkage,
    metric,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    if numeric.shape[1] < 1:
        return (
            dbc.Alert(
                (
                    "Le clustering hiérarchique "
                    "nécessite au moins une "
                    "variable numérique."
                ),
                color="warning",
            ),
            {},
        )

    n_observations = int(
        numeric.shape[0]
    )

    if n_observations < 3:
        return (
            dbc.Alert(
                (
                    "Le clustering hiérarchique "
                    "nécessite au moins trois "
                    "observations."
                ),
                color="warning",
            ),
            {},
        )

    try:
        requested_clusters = int(
            n_clusters
            if n_clusters is not None
            else 3
        )
    except (TypeError, ValueError):
        requested_clusters = 3

    if (
        requested_clusters < 2
        or requested_clusters
        >= n_observations
    ):
        return (
            dbc.Alert(
                (
                    "Le nombre de clusters doit "
                    "être au moins égal à 2 et "
                    "strictement inférieur au "
                    "nombre d'observations."
                ),
                color="warning",
            ),
            {},
        )

    requested_linkage = (
        linkage
        if linkage is not None
        else "ward"
    )

    requested_metric = (
        metric
        if metric is not None
        else "euclidean"
    )

    allowed_linkages = {
        "ward",
        "complete",
        "average",
        "single",
    }

    if requested_linkage not in allowed_linkages:
        return (
            dbc.Alert(
                "Linkage non reconnu.",
                color="warning",
            ),
            {},
        )

    allowed_metrics = {
        "euclidean",
        "manhattan",
        "cosine",
    }

    if requested_metric not in allowed_metrics:
        return (
            dbc.Alert(
                "Métrique non reconnue.",
                color="warning",
            ),
            {},
        )

    # Le linkage Ward exige la métrique euclidienne.
    effective_metric = requested_metric

    if requested_linkage == "ward":
        effective_metric = "euclidean"

    # Standardisation analytique temporaire.
    scaler = StandardScaler()

    standardized = pd.DataFrame(
        scaler.fit_transform(
            numeric
        ),
        columns=numeric.columns,
        index=numeric.index,
    )

    try:
        result = (
            AgglomerativeClusteringEngine.fit(
                standardized,
                n_clusters=(
                    requested_clusters
                ),
                linkage=(
                    requested_linkage
                ),
                metric=(
                    effective_metric
                ),
            )
        )

    except Exception as exc:
        return (
            dbc.Alert(
                (
                    "Le clustering hiérarchique "
                    "n'a pas pu être terminé : "
                    f"{exc}"
                ),
                color="danger",
            ),
            {},
        )

    labels = pd.Series(
        result.predictions,
        index=standardized.index,
        name="Cluster",
    )

    display_labels = (
        labels
        .astype(int)
        .add(1)
        .map(
            lambda value:
                f"Cluster {value}"
        )
    )

    cluster_sizes = (
        display_labels
        .value_counts()
        .sort_index()
        .rename_axis("Cluster")
        .reset_index(name="Effectif")
    )

    cluster_sizes[
        "Pourcentage"
    ] = (
        100
        * cluster_sizes["Effectif"]
        / n_observations
    ).round(2)

    def _metric_value(value):
        if value is None:
            return None

        return round(
            float(value),
            6,
        )

    metrics_df = pd.DataFrame(
        [
            {
                "Métrique":
                    "Nombre de clusters",
                "Valeur":
                    requested_clusters,
            },
            {
                "Métrique":
                    "Linkage",
                "Valeur":
                    requested_linkage,
            },
            {
                "Métrique":
                    "Métrique demandée",
                "Valeur":
                    requested_metric,
            },
            {
                "Métrique":
                    "Métrique utilisée",
                "Valeur":
                    effective_metric,
            },
            {
                "Métrique":
                    "Silhouette",
                "Valeur":
                    _metric_value(
                        result.silhouette_score
                    ),
            },
            {
                "Métrique":
                    "Davies-Bouldin",
                "Valeur":
                    _metric_value(
                        result.davies_bouldin_score
                    ),
            },
            {
                "Métrique":
                    "Calinski-Harabasz",
                "Valeur":
                    _metric_value(
                        result.calinski_harabasz_score
                    ),
            },
        ]
    )

    # PCA uniquement pour la visualisation.
    if standardized.shape[1] >= 2:
        projection_model = PCAReduction(
            n_components=2
        )

        transformed = (
            projection_model.fit_transform(
                standardized
            )
        )

        projection = _unwrap_transformed(
            transformed,
            index=standardized.index,
        )

        projection.columns = [
            "Dimension 1",
            "Dimension 2",
        ]

    else:
        projection = pd.DataFrame(
            {
                "Dimension 1":
                    standardized.iloc[:, 0],
                "Dimension 2":
                    np.zeros(
                        n_observations
                    ),
            },
            index=standardized.index,
        )

    projection["Cluster"] = (
        display_labels
    )

    projection["Observation"] = (
        np.arange(
            1,
            n_observations + 1,
        )
    )

    projection_figure = px.scatter(
        projection,
        x="Dimension 1",
        y="Dimension 2",
        color="Cluster",
        hover_data=["Observation"],
        title=(
            "Projection 2D du clustering "
            "hiérarchique"
        ),
    )

    summary_content = [
        dbc.Alert(
            (
                "Le clustering hiérarchique "
                "agglomératif a été exécuté "
                "sur les variables numériques "
                "standardisées."
            ),
            color="info",
        ),
        html.H6(
            "Paramètres et métriques",
            className="mt-3",
        ),
        _table(metrics_df),
        html.H6(
            "Effectifs par cluster",
            className="mt-4",
        ),
        _table(cluster_sizes),
    ]

    if (
        requested_linkage == "ward"
        and requested_metric
        != "euclidean"
    ):
        summary_content.append(
            dbc.Alert(
                (
                    "Le linkage Ward nécessite "
                    "la distance euclidienne. "
                    "La métrique demandée a donc "
                    "été remplacée par "
                    "« euclidean »."
                ),
                color="warning",
            )
        )

    summary_content.extend(
        [
            dbc.Alert(
                (
                    "Les métriques permettent "
                    "d'évaluer et de comparer "
                    "des partitionnements, mais "
                    "ne démontrent pas à elles "
                    "seules qu'un nombre de "
                    "clusters est optimal."
                ),
                color="secondary",
            ),
            dbc.Alert(
                (
                    "La projection PCA 2D sert "
                    "uniquement à visualiser "
                    "les groupes. Le clustering "
                    "est calculé dans l'espace "
                    "standardisé complet."
                ),
                color="secondary",
            ),
        ]
    )

    _persist_ekde(
        project_id,
        dataset_id,
        "agglomerative",
        {
            "n_clusters": (
                requested_clusters
            ),
            "linkage": (
                requested_linkage
            ),
            "requested_metric": (
                requested_metric
            ),
            "effective_metric": (
                effective_metric
            ),
            "n_observations": (
                n_observations
            ),
            "numeric_variables": (
                list(numeric.columns)
            ),
            "converted_columns": (
                conversions
            ),
            "standardized": True,
            "silhouette_score": (
                result.silhouette_score
            ),
            "davies_bouldin_score": (
                result.davies_bouldin_score
            ),
            "calinski_harabasz_score": (
                result.calinski_harabasz_score
            ),
            "cluster_sizes": (
                cluster_sizes
                .to_dict(
                    orient="records"
                )
            ),
            "labels": [
                int(value) + 1
                for value
                in result.predictions
            ],
        },
    )

    return (
        summary_content,
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
        "ekde-association-run",
        "n_clicks",
    ),
    State(
        "ekde-association-x",
        "value",
    ),
    State(
        "ekde-association-y",
        "value",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def association_analysis(
    n_clicks,
    x,
    y,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update, no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

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

    _persist_ekde(
        project_id,
        dataset_id,
        "associations",
        {
            "x": x,
            "y": y,
            "n": int(len(pair)),
            "pearson": round(
                float(pearson),
                6,
            ),
            "spearman": round(
                float(spearman),
                6,
            ),
            "mutual_information": (
                mi_text
            ),
            "metrics": (
                metrics.to_dict(
                    orient="records"
                )
            ),
        },
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
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def selection_analysis(
    n_clicks,
    method,
    target,
    variance_threshold,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

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

        _persist_ekde(
            project_id,
            dataset_id,
            "selection",
            {
                "method": method,
                "target": target,
                "variance_threshold": (
                    float(
                        variance_threshold
                        or 0.0
                    )
                    if method == "variance"
                    else None
                ),
                "numeric_variables": (
                    list(numeric.columns)
                ),
                "converted_columns": conversions,
                "result": (
                    result_df
                    .to_dict(
                        orient="records"
                    )
                ),
            },
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
        "ekde-knowledge-run",
        "n_clicks",
    ),
    State(
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def knowledge_summary(
    n_clicks,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

    numeric, conversions = (
        _prepare_numeric_matrix(
            dataframe
        )
    )

    findings = []
    findings_text = []

    numeric_message = (
        f"{numeric.shape[1]} variable(s) "
        "numérique(s) ou numeric-like "
        "sont exploitables pour les analyses "
        "multivariées."
    )

    findings.append(
        html.Li(
            numeric_message
        )
    )

    findings_text.append(
        numeric_message
    )

    if conversions:

        converted_names = [
            item["column"]
            for item in conversions
        ]

        conversion_message = (
            "Variables numeric-like identifiées : "
            + ", ".join(converted_names)
            + "."
        )

        findings.append(
            html.Li(
                conversion_message
            )
        )

        findings_text.append(
            conversion_message
        )

    strong_pairs = []

    if numeric.shape[1] >= 2:

        corr = numeric.corr()

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

                    strong_pairs.append(
                        {
                            "variable_1":
                                column_a,
                            "variable_2":
                                column_b,
                            "correlation":
                                round(
                                    float(value),
                                    6,
                                ),
                            "absolute_correlation":
                                round(
                                    abs(
                                        float(value)
                                    ),
                                    6,
                                ),
                        }
                    )

        if strong_pairs:

            correlation_message = (
                f"{len(strong_pairs)} association(s) "
                "linéaire(s) forte(s) "
                "(|r| ≥ 0,90) détectée(s). "
                "Elles peuvent signaler une "
                "redondance entre variables."
            )

        else:

            correlation_message = (
                "Aucune redondance linéaire "
                "forte n'est détectée au seuil "
                "|r| ≥ 0,90."
            )

        findings.append(
            html.Li(
                correlation_message
            )
        )

        findings_text.append(
            correlation_message
        )

    limitation = (
        "Ces éléments sont des diagnostics "
        "exploratoires. Une association ou "
        "une composante latente ne constitue "
        "pas, à elle seule, une relation "
        "causale."
    )

    _persist_ekde(
        project_id,
        dataset_id,
        "knowledge_summary",
        {
            "numeric_variable_count": int(
                numeric.shape[1]
            ),
            "numeric_variables": (
                list(numeric.columns)
            ),
            "converted_columns": conversions,
            "correlation_threshold": 0.90,
            "strong_correlations": strong_pairs,
            "findings": findings_text,
            "limitations": [
                limitation
            ],
        },
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Connaissances automatiquement dégagées"
                ),

                html.Ul(
                    findings
                ),

                html.Hr(),

                html.Small(
                    limitation,
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
        "ekde-project-id",
        "data",
    ),
    State(
        "ekde-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def export_knowledge(
    n_clicks,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update

    dataframe = _load_ekde_dataframe(
        project_id,
        dataset_id,
    )

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
