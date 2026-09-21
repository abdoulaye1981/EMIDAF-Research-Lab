

import logging

import pandas as pd

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

from emidaf_core.preprocessing import (
    DuplicateDetection,
    Encoding,
    Imputation,
    OutlierDetection,
    Scaling,
)

from emidaf_studio.services.model_registry import (
    get_analysis,
    register_analysis,
)

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)


logger = logging.getLogger(__name__)


def _unwrap_dataframe(result):
    """
    Certains composants EMIDAF retournent directement un
    DataFrame, d'autres un tuple (DataFrame, objet ajusté).
    """

    if isinstance(result, pd.DataFrame):
        return result

    if (
        isinstance(result, tuple)
        and result
        and isinstance(result[0], pd.DataFrame)
    ):
        return result[0]

    if isinstance(result, dict):
        for key in ("data", "X", "dataframe"):
            candidate = result.get(key)

            if isinstance(candidate, pd.DataFrame):
                return candidate

    raise TypeError(
        "Le composant de prétraitement n'a pas renvoyé "
        "un DataFrame exploitable."
    )


def _metrics(dataframe):

    rows, columns = dataframe.shape

    return {
        "rows": int(rows),
        "columns": int(columns),
        "cells": int(rows * columns),
        "missing": int(
            dataframe.isna().sum().sum()
        ),
        "duplicates": int(
            dataframe.duplicated().sum()
        ),
    }


def _comparison_table(before, after):

    before_metrics = _metrics(before)
    after_metrics = _metrics(after)

    rows = []

    labels = {
        "rows": "Lignes",
        "columns": "Colonnes",
        "cells": "Cellules",
        "missing": "Valeurs manquantes",
        "duplicates": "Doublons",
    }

    for key, label in labels.items():

        rows.append(
            html.Tr(
                [
                    html.Td(
                        html.Strong(label)
                    ),
                    html.Td(
                        f"{before_metrics[key]:,}"
                    ),
                    html.Td(
                        f"{after_metrics[key]:,}"
                    ),
                    html.Td(
                        f"{after_metrics[key] - before_metrics[key]:+,}"
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Indicateur"),
                        html.Th("Avant"),
                        html.Th("Après"),
                        html.Th("Variation"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _preview(dataframe):

    preview = dataframe.head(10)

    return dbc.Table.from_dataframe(
        preview,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )



def _coerce_numeric_like_columns(
    dataframe,
    threshold=0.95,
):
    """
    Convertit en numérique les colonnes object/string dont
    une très grande majorité des valeurs est convertible.

    Exemple :
        IMC = ["29.3", "22.5", ..., "inconnu"]

    devient :
        IMC = [29.3, 22.5, ..., NaN]

    Les vraies variables catégorielles comme Genre restent
    inchangées.
    """

    result = dataframe.copy()

    converted_columns = []

    for column in result.select_dtypes(
        include=["object", "string"]
    ).columns:

        series = result[column]

        non_missing = series.dropna()

        if non_missing.empty:
            continue

        converted = pd.to_numeric(
            non_missing,
            errors="coerce",
        )

        conversion_rate = (
            converted.notna().sum()
            / len(non_missing)
        )

        if conversion_rate >= threshold:

            result[column] = pd.to_numeric(
                result[column],
                errors="coerce",
            )

            converted_columns.append(
                {
                    "column": column,
                    "conversion_rate": round(
                        conversion_rate * 100,
                        2,
                    ),
                }
            )

    return result, converted_columns


def _impute_dataframe(dataframe, strategy):

    if strategy == "none":
        return dataframe.copy()

    result = dataframe.copy()

    numeric_columns = list(
        result.select_dtypes(
            include="number"
        ).columns
    )

    other_columns = [
        column
        for column in result.columns
        if column not in numeric_columns
    ]

    # ----------------------------------------------
    # Variables numériques
    # ----------------------------------------------

    numeric_missing = [
        column
        for column in numeric_columns
        if result[column].isna().any()
    ]

    if numeric_missing:

        numeric_strategy = strategy

        if strategy == "mode":
            numeric_strategy = "mode"

        transformed = Imputation.fit_transform(
            result[numeric_missing],
            strategy=numeric_strategy,
        )

        transformed = _unwrap_dataframe(
            transformed
        )

        result.loc[
            :,
            numeric_missing,
        ] = transformed[
            numeric_missing
        ].to_numpy()

    # ----------------------------------------------
    # Variables non numériques
    # Mode uniquement : statistiquement cohérent
    # pour les catégories.
    # ----------------------------------------------

    categorical_missing = [
        column
        for column in other_columns
        if result[column].isna().any()
    ]

    if categorical_missing:

        transformed = Imputation.fit_transform(
            result[categorical_missing],
            strategy="mode",
        )

        transformed = _unwrap_dataframe(
            transformed
        )

        result.loc[
            :,
            categorical_missing,
        ] = transformed[
            categorical_missing
        ].to_numpy()

    return result


def _encode_dataframe(dataframe, method):

    if method == "none":
        return dataframe.copy()

    transformer = Encoding(
        method=method
    )

    result = transformer.fit_transform(
        dataframe
    )

    return _unwrap_dataframe(result)


def _scale_dataframe(dataframe, method):

    if method == "none":
        return dataframe.copy()

    result = dataframe.copy()

    numeric_columns = list(
        result.select_dtypes(
            include="number"
        ).columns
    )

    if not numeric_columns:
        return result

    scaler = Scaling(
        method=method
    )

    transformed = scaler.fit_transform(
        result[numeric_columns]
    )

    transformed = _unwrap_dataframe(
        transformed
    )

    result.loc[
        :,
        numeric_columns,
    ] = transformed[
        numeric_columns
    ].to_numpy()

    return result


@callback(
    Output(
        "eidpp-comparison",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eidpp-preview",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eidpp-alert",
        "children",
        allow_duplicate=True,
    ),
    Input(
        "eidpp-apply",
        "n_clicks",
    ),
    State(
        "eidpp-imputation",
        "value",
    ),
    State(
        "eidpp-duplicates",
        "value",
    ),
    State(
        "eidpp-outliers",
        "value",
    ),
    State(
        "eidpp-encoding",
        "value",
    ),
    State(
        "eidpp-scaling",
        "value",
    ),
    State(
        "eidpp-project-id",
        "data",
    ),
    State(
        "eidpp-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def apply_preprocessing(
    n_clicks,
    imputation,
    duplicates,
    outliers,
    encoding,
    scaling,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
        )

    try:
        project, dataset, result = load_dataset(
            project_id,
            dataset_id,
        )

        if isinstance(result, str):
            return (
                no_update,
                no_update,
                dbc.Alert(
                    result,
                    color="danger",
                ),
            )

        original = result

        # Chaque exécution repart du dataset source.
        # Cela évite de cumuler silencieusement les
        # transformations lors de plusieurs clics.
        dataframe = original.copy(
            deep=True
        )

        # ==========================================
        # 0. CORRECTION DES TYPES
        # ==========================================

        dataframe, converted_columns = (
            _coerce_numeric_like_columns(
                dataframe
            )
        )

        # ==========================================
        # 1. IMPUTATION
        # ==========================================

        dataframe = _impute_dataframe(
            dataframe,
            imputation,
        )

        # ==========================================
        # 2. DUPLICATES
        # ==========================================

        if "remove" in (duplicates or []):
            dataframe = (
                DuplicateDetection.remove(
                    dataframe,
                    keep="first",
                )
            )

        # ==========================================
        # 3. OUTLIERS
        # ==========================================

        if outliers == "remove_iqr":
            dataframe = (
                OutlierDetection.remove_iqr(
                    dataframe
                )
            )

        elif outliers == "winsorize":
            dataframe = (
                OutlierDetection.winsorize(
                    dataframe
                )
            )

        # ==========================================
        # 4. ENCODING
        # ==========================================

        dataframe = _encode_dataframe(
            dataframe,
            encoding,
        )

        # ==========================================
        # 5. SCALING
        # ==========================================

        dataframe = _scale_dataframe(
            dataframe,
            scaling,
        )

        dataframe = dataframe.reset_index(
            drop=True
        )

        # ==========================================
        # PERSISTANCE EIDPP
        # ==========================================

        register_analysis(
            project_id,
            dataset_id,
            "eidpp",
            {
                "before_metrics": _metrics(
                    original
                ),
                "after_metrics": _metrics(
                    dataframe
                ),
                "operations": {
                    "imputation": imputation,
                    "duplicates": duplicates,
                    "outliers": outliers,
                    "encoding": encoding,
                    "scaling": scaling,
                },
                "converted_columns": list(
                    converted_columns
                ),
                "rows_before": int(
                    original.shape[0]
                ),
                "rows_after": int(
                    dataframe.shape[0]
                ),
                "columns_before": int(
                    original.shape[1]
                ),
                "columns_after": int(
                    dataframe.shape[1]
                ),
                "processed_dataframe":
                    dataframe.copy(
                        deep=True
                    ),
            },
        )

        return (
            _comparison_table(
                original,
                dataframe,
            ),
            _preview(dataframe),
            dbc.Alert(
                [
                    html.Strong(
                        "Prétraitement appliqué "
                        "avec succès. "
                    ),
                    html.Span(
                        (
                            "Le dataset source "
                            "n'a pas été modifié."
                        )
                    ),
                    (
                        html.Div(
                            [
                                html.Br(),
                                html.Strong(
                                    (
                                        "Types corrigés "
                                        "automatiquement : "
                                    )
                                ),
                                ", ".join(
                                    (
                                        f"{item['column']} "
                                        f"({item['conversion_rate']:.2f} % "
                                        "convertible)"
                                    )
                                    for item
                                    in converted_columns
                                ),
                            ]
                        )
                        if converted_columns
                        else None
                    ),
                ],
                color="success",
            ),
        )

    except Exception as exc:
        logger.exception(
            "EIDPP preprocessing failed "
            "(project_id=%s, dataset_id=%s)",
            project_id,
            dataset_id,
        )

        return (
            no_update,
            no_update,
            dbc.Alert(
                [
                    html.Strong(
                        "Erreur de prétraitement : "
                    ),
                    html.Span(
                        str(exc)
                    ),
                ],
                color="danger",
            ),
        )


@callback(
    Output(
        "eidpp-comparison",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eidpp-preview",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eidpp-alert",
        "children",
        allow_duplicate=True,
    ),
    Input(
        "eidpp-reset",
        "n_clicks",
    ),
    State(
        "eidpp-project-id",
        "data",
    ),
    State(
        "eidpp-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def reset_preprocessing(
    n_clicks,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
        )

    project, dataset, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        return (
            no_update,
            no_update,
            dbc.Alert(
                result,
                color="danger",
            ),
        )

    dataframe = result

    register_analysis(
        project_id,
        dataset_id,
        "eidpp",
        {
            "before_metrics": _metrics(
                dataframe
            ),
            "after_metrics": _metrics(
                dataframe
            ),
            "operations": {
                "imputation": "none",
                "duplicates": [],
                "outliers": "none",
                "encoding": "none",
                "scaling": "none",
            },
            "converted_columns": [],
            "rows_before": int(
                dataframe.shape[0]
            ),
            "rows_after": int(
                dataframe.shape[0]
            ),
            "columns_before": int(
                dataframe.shape[1]
            ),
            "columns_after": int(
                dataframe.shape[1]
            ),
            "processed_dataframe":
                dataframe.copy(
                    deep=True
                ),
        },
    )

    return (
        _comparison_table(
            dataframe,
            dataframe,
        ),
        _preview(dataframe),
        dbc.Alert(
            "Dataset réinitialisé.",
            color="info",
        ),
    )


@callback(
    Output(
        "eidpp-download-data",
        "data",
    ),
    Input(
        "eidpp-download",
        "n_clicks",
    ),
    State(
        "eidpp-project-id",
        "data",
    ),
    State(
        "eidpp-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def download_processed_dataset(
    n_clicks,
    project_id,
    dataset_id,
):
    if not n_clicks:
        return no_update

    context = get_analysis(
        project_id,
        dataset_id,
        "eidpp",
        default=None,
    )

    dataframe = None

    if isinstance(
        context,
        dict,
    ):
        candidate = context.get(
            "processed_dataframe"
        )

        if isinstance(
            candidate,
            pd.DataFrame,
        ):
            dataframe = candidate

    # Avant tout prétraitement EIDPP, le bouton
    # conserve son comportement utile en permettant
    # de télécharger le dataset source.
    if dataframe is None:
        project, dataset, result = load_dataset(
            project_id,
            dataset_id,
        )

        if isinstance(result, str):
            return no_update

        dataframe = result

    return dcc.send_data_frame(
        dataframe.to_csv,
        f"dataset_{dataset_id}_eidpp.csv",
        index=False,
    )
