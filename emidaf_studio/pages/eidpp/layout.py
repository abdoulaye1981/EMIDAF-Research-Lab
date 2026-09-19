
from dash import html, dcc
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset


def _metric_card(title, value, suffix=""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title),
                html.H4(f"{value}{suffix}"),
            ]
        ),
        className="h-100",
    )


def _initial_metrics(dataframe):
    rows, columns = dataframe.shape
    missing = int(dataframe.isna().sum().sum())
    duplicates = int(dataframe.duplicated().sum())

    return {
        "rows": rows,
        "columns": columns,
        "missing": missing,
        "duplicates": duplicates,
    }


def eidpp_layout(project_id, dataset_id):

    project, dataset, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        return dbc.Container(
            dbc.Alert(
                result,
                color="danger",
            ),
            fluid=True,
        )

    dataframe = result
    metrics = _initial_metrics(dataframe)

    return dbc.Container(
        [
            html.H2(
                "🧹 EIDPP — Prétraitement des données",
                className="mt-3",
            ),

            html.P(
                (
                    "Environnement interactif de diagnostic, "
                    "préparation et transformation des données."
                ),
                className="text-muted",
            ),

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects",
                    },
                    {
                        "label": project.name,
                        "href": f"/projects/{project_id}",
                    },
                    {
                        "label": dataset.name,
                        "href": (
                            f"/projects/{project_id}"
                            f"/datasets/{dataset_id}"
                        ),
                    },
                    {
                        "label": "EIDPP",
                        "active": True,
                    },
                ]
            ),

            # ==================================================
            # DATASET
            # ==================================================

            html.H4(
                "📋 Dataset source",
                className="mt-4",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        _metric_card(
                            "Lignes",
                            metrics["rows"],
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _metric_card(
                            "Colonnes",
                            metrics["columns"],
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _metric_card(
                            "Valeurs manquantes",
                            metrics["missing"],
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _metric_card(
                            "Doublons",
                            metrics["duplicates"],
                        ),
                        md=3,
                    ),
                ],
                className="g-3 mb-4",
            ),

            # ==================================================
            # CONFIGURATION
            # ==================================================

            html.H4(
                "⚙️ Configuration du prétraitement",
                className="mt-4",
            ),

            dbc.Accordion(
                [
                    # ------------------------------------------
                    # Missing
                    # ------------------------------------------

                    dbc.AccordionItem(
                        [
                            html.P(
                                (
                                    "Choisissez la stratégie "
                                    "d'imputation à appliquer."
                                )
                            ),

                            dbc.Label(
                                "Méthode d'imputation"
                            ),

                            dcc.Dropdown(
                                id="eidpp-imputation",
                                options=[
                                    {
                                        "label":
                                            "Ne pas imputer",
                                        "value":
                                            "none",
                                    },
                                    {
                                        "label":
                                            "Moyenne",
                                        "value":
                                            "mean",
                                    },
                                    {
                                        "label":
                                            "Médiane",
                                        "value":
                                            "median",
                                    },
                                    {
                                        "label":
                                            "Mode",
                                        "value":
                                            "mode",
                                    },
                                    {
                                        "label":
                                            "KNN",
                                        "value":
                                            "knn",
                                    },
                                    {
                                        "label":
                                            "MICE",
                                        "value":
                                            "mice",
                                    },
                                ],
                                value="none",
                                clearable=False,
                            ),
                        ],
                        title="🧩 Valeurs manquantes",
                    ),

                    # ------------------------------------------
                    # Duplicates
                    # ------------------------------------------

                    dbc.AccordionItem(
                        dbc.Checklist(
                            id="eidpp-duplicates",
                            options=[
                                {
                                    "label":
                                        (
                                            "Supprimer les lignes "
                                            "dupliquées"
                                        ),
                                    "value":
                                        "remove",
                                }
                            ],
                            value=[],
                            switch=True,
                        ),
                        title="📑 Doublons",
                    ),

                    # ------------------------------------------
                    # Outliers
                    # ------------------------------------------

                    dbc.AccordionItem(
                        [
                            dbc.Label(
                                "Traitement des valeurs aberrantes"
                            ),

                            dcc.Dropdown(
                                id="eidpp-outliers",
                                options=[
                                    {
                                        "label":
                                            "Conserver",
                                        "value":
                                            "none",
                                    },
                                    {
                                        "label":
                                            (
                                                "Supprimer selon "
                                                "la règle IQR"
                                            ),
                                        "value":
                                            "remove_iqr",
                                    },
                                    {
                                        "label":
                                            "Winsoriser",
                                        "value":
                                            "winsorize",
                                    },
                                ],
                                value="none",
                                clearable=False,
                            ),
                        ],
                        title="⚠️ Valeurs aberrantes",
                    ),

                    # ------------------------------------------
                    # Encoding
                    # ------------------------------------------

                    dbc.AccordionItem(
                        [
                            dbc.Label(
                                "Encodage des variables catégorielles"
                            ),

                            dcc.Dropdown(
                                id="eidpp-encoding",
                                options=[
                                    {
                                        "label":
                                            "Aucun encodage",
                                        "value":
                                            "none",
                                    },
                                    {
                                        "label":
                                            "One-Hot Encoding",
                                        "value":
                                            "onehot",
                                    },
                                    {
                                        "label":
                                            "Ordinal",
                                        "value":
                                            "ordinal",
                                    },
                                ],
                                value="none",
                                clearable=False,
                            ),
                        ],
                        title="🔤 Encodage",
                    ),

                    # ------------------------------------------
                    # Scaling
                    # ------------------------------------------

                    dbc.AccordionItem(
                        [
                            dbc.Label(
                                "Mise à l'échelle"
                            ),

                            dcc.Dropdown(
                                id="eidpp-scaling",
                                options=[
                                    {
                                        "label":
                                            "Aucune",
                                        "value":
                                            "none",
                                    },
                                    {
                                        "label":
                                            "Standardisation",
                                        "value":
                                            "standard",
                                    },
                                    {
                                        "label":
                                            "Min-Max",
                                        "value":
                                            "minmax",
                                    },
                                    {
                                        "label":
                                            "Robust Scaler",
                                        "value":
                                            "robust",
                                    },
                                ],
                                value="none",
                                clearable=False,
                            ),
                        ],
                        title="📏 Scaling / Normalisation",
                    ),
                ],
                start_collapsed=True,
                always_open=True,
                className="mb-4",
            ),

            # ==================================================
            # ACTIONS
            # ==================================================

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "▶️ Appliquer le prétraitement",
                            id="eidpp-apply",
                            color="primary",
                            className="w-100",
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dbc.Button(
                            "↩️ Réinitialiser",
                            id="eidpp-reset",
                            color="secondary",
                            outline=True,
                            className="w-100",
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dbc.Button(
                            "💾 Exporter le CSV",
                            id="eidpp-download",
                            color="success",
                            outline=True,
                            className="w-100",
                        ),
                        md=4,
                    ),
                ],
                className="g-3 mb-4",
            ),

            html.Div(
                id="eidpp-alert",
            ),

            # ==================================================
            # AVANT APRES
            # ==================================================

            html.H4(
                "📊 Comparaison avant / après",
                className="mt-4",
            ),

            html.Div(
                id="eidpp-comparison",
            ),

            # ==================================================
            # APERCU
            # ==================================================

            html.H4(
                "👁️ Aperçu du dataset traité",
                className="mt-4",
            ),

            html.Div(
                id="eidpp-preview",
            ),

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← Retour à l'inspection",
                                color="secondary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}"
                            ),
                        ),
                        md=6,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "📊 Ouvrir ELAE",
                                color="primary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/elae"
                            ),
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
            ),

            # ==================================================
            # STORES
            # ==================================================

            dcc.Store(
                id="eidpp-project-id",
                data=project_id,
            ),

            dcc.Store(
                id="eidpp-dataset-id",
                data=dataset_id,
            ),

            dcc.Store(
                id="eidpp-original-data",
                data=dataframe.to_json(
                    orient="split",
                    date_format="iso",
                ),
            ),

            dcc.Store(
                id="eidpp-working-data",
                data=dataframe.to_json(
                    orient="split",
                    date_format="iso",
                ),
            ),

            dcc.Download(
                id="eidpp-download-data"
            ),
        ],
        fluid=True,
    )
