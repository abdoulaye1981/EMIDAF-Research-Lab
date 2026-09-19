
from dash import html, dcc
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset


def _card(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title),
                html.H4(str(value)),
            ]
        ),
        className="h-100",
    )


def elae_layout(project_id, dataset_id):

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

    df = result

    numeric = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    non_numeric = [
        column
        for column in df.columns
        if column not in numeric
    ]

    return dbc.Container(
        [
            html.H2(
                "📊 ELAE — Analyse exploratoire des données",
                className="mt-3",
            ),

            html.P(
                (
                    "Exploration statistique et graphique "
                    "interactive du dataset."
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
                        "label": "ELAE",
                        "active": True,
                    },
                ]
            ),

            # ==================================================
            # OVERVIEW
            # ==================================================

            dbc.Row(
                [
                    dbc.Col(
                        _card(
                            "Lignes",
                            df.shape[0],
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _card(
                            "Colonnes",
                            df.shape[1],
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _card(
                            "Variables numériques",
                            len(numeric),
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _card(
                            "Variables non numériques",
                            len(non_numeric),
                        ),
                        md=3,
                    ),
                ],
                className="g-3 mb-4",
            ),

            dbc.Tabs(
                [
                    # ==========================================
                    # DESCRIPTIVE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "📋 Statistiques descriptives",
                                className="mt-4",
                            ),

                            html.Div(
                                id="elae-descriptive",
                            ),
                        ],
                        label="Résumé descriptif",
                    ),

                    # ==========================================
                    # UNIVARIATE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "📈 Analyse univariée",
                                className="mt-4",
                            ),

                            dbc.Label(
                                "Variable"
                            ),

                            dcc.Dropdown(
                                id="elae-univariate-variable",
                                options=[
                                    {
                                        "label": column,
                                        "value": column,
                                    }
                                    for column in df.columns
                                ],
                                value=(
                                    df.columns[0]
                                    if len(df.columns)
                                    else None
                                ),
                                clearable=False,
                            ),

                            html.Div(
                                id="elae-univariate-summary",
                                className="mt-3",
                            ),

                            dcc.Graph(
                                id="elae-univariate-graph",
                            ),
                        ],
                        label="Univariée",
                    ),

                    # ==========================================
                    # BIVARIATE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "🔗 Analyse bivariée",
                                className="mt-4",
                            ),

                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Variable X"
                                            ),
                                            dcc.Dropdown(
                                                id="elae-x",
                                                options=[
                                                    {
                                                        "label": c,
                                                        "value": c,
                                                    }
                                                    for c in df.columns
                                                ],
                                                value=(
                                                    df.columns[0]
                                                    if len(df.columns)
                                                    else None
                                                ),
                                                clearable=False,
                                            ),
                                        ],
                                        md=6,
                                    ),

                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Variable Y"
                                            ),
                                            dcc.Dropdown(
                                                id="elae-y",
                                                options=[
                                                    {
                                                        "label": c,
                                                        "value": c,
                                                    }
                                                    for c in df.columns
                                                ],
                                                value=(
                                                    df.columns[1]
                                                    if len(df.columns) > 1
                                                    else None
                                                ),
                                                clearable=False,
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ]
                            ),

                            html.Div(
                                id="elae-bivariate-summary",
                                className="mt-3",
                            ),

                            dcc.Graph(
                                id="elae-bivariate-graph",
                            ),
                        ],
                        label="Bivariée",
                    ),

                    # ==========================================
                    # CORRELATION
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "🧭 Corrélations",
                                className="mt-4",
                            ),

                            html.Div(
                                id="elae-correlation-table",
                            ),

                            dcc.Graph(
                                id="elae-correlation-graph",
                            ),
                        ],
                        label="Corrélations",
                    ),

                    # ==========================================
                    # GROUPED
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "👥 Analyse par groupes",
                                className="mt-4",
                            ),

                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Variable de groupe"
                                            ),

                                            dcc.Dropdown(
                                                id="elae-group-variable",
                                                options=[
                                                    {
                                                        "label": c,
                                                        "value": c,
                                                    }
                                                    for c in non_numeric
                                                ],
                                                value=(
                                                    non_numeric[0]
                                                    if non_numeric
                                                    else None
                                                ),
                                                clearable=True,
                                            ),
                                        ],
                                        md=6,
                                    ),

                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Variable numérique"
                                            ),

                                            dcc.Dropdown(
                                                id="elae-value-variable",
                                                options=[
                                                    {
                                                        "label": c,
                                                        "value": c,
                                                    }
                                                    for c in numeric
                                                ],
                                                value=(
                                                    numeric[0]
                                                    if numeric
                                                    else None
                                                ),
                                                clearable=True,
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ]
                            ),

                            html.Div(
                                id="elae-group-summary",
                                className="mt-3",
                            ),

                            dcc.Graph(
                                id="elae-group-graph",
                            ),
                        ],
                        label="Groupes",
                    ),
                ]
            ),

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← Inspection",
                                color="secondary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}"
                            ),
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "🧹 EIDPP",
                                color="primary",
                                outline=True,
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/eidpp"
                            ),
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "🧠 Ouvrir EKDE",
                                color="success",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/ekde"
                            ),
                        ),
                        md=4,
                    ),
                ],
                className="g-3 mt-3",
            ),

            dcc.Store(
                id="elae-project-id",
                data=project_id,
            ),

            dcc.Store(
                id="elae-dataset-id",
                data=dataset_id,
            ),

            dcc.Store(
                id="elae-data",
                data=df.to_json(
                    orient="split",
                    date_format="iso",
                ),
            ),

            dcc.Download(
                id="elae-download-data"
            ),
        ],
        fluid=True,
    )
