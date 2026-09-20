from dash import dcc, html
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset


def eaie_layout(project_id, dataset_id):

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

    columns = list(df.columns)

    options = [
        {
            "label": column,
            "value": column,
        }
        for column in columns
    ]

    return dbc.Container(
        [
            html.H2(
                "Modélisation prédictive : EAIE",
                className="mt-3",
            ),

            html.P(
                (
                    "Entraînez, comparez et sélectionnez des modèles "
                    "prédictifs selon des critères de validation adaptés "
                    "au problème étudié. Le jeu de test reste réservé "
                    "à l'évaluation finale du modèle retenu."
                ),
                className="text-muted",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Principe méthodologique : "
                    ),
                    (
                        "le modèle est sélectionné sur la validation "
                        "croisée. Le jeu de test reste réservé à "
                        "l'évaluation finale."
                    ),
                ],
                color="info",
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
                        "label": "EAIE",
                        "active": True,
                    },
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Observations",
                                        className="text-muted",
                                    ),
                                    html.H4(
                                        str(df.shape[0])
                                    ),
                                ]
                            )
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Variables",
                                        className="text-muted",
                                    ),
                                    html.H4(
                                        str(df.shape[1])
                                    ),
                                ]
                            )
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Valeurs manquantes",
                                        className="text-muted",
                                    ),
                                    html.H4(
                                        str(
                                            int(
                                                df.isna()
                                                .sum()
                                                .sum()
                                            )
                                        )
                                    ),
                                ]
                            )
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Mode",
                                        className="text-muted",
                                    ),
                                    html.H4(
                                        "Supervisé"
                                    ),
                                ]
                            )
                        ),
                        md=3,
                    ),
                ],
                className="g-3 mb-4",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(
                            "Configuration"
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Variable cible"
                                        ),

                                        dcc.Dropdown(
                                            id="eaie-target",
                                            options=options,
                                            placeholder=(
                                                "Sélectionner "
                                                "la cible"
                                            ),
                                            clearable=True,
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Type de problème"
                                        ),

                                        dcc.Dropdown(
                                            id="eaie-task",
                                            options=[
                                                {
                                                    "label": (
                                                        "Détection "
                                                        "automatique"
                                                    ),
                                                    "value": "auto",
                                                },
                                                {
                                                    "label": (
                                                        "Classification"
                                                    ),
                                                    "value": (
                                                        "classification"
                                                    ),
                                                },
                                                {
                                                    "label": (
                                                        "Régression"
                                                    ),
                                                    "value": (
                                                        "regression"
                                                    ),
                                                },
                                            ],
                                            value="auto",
                                            clearable=False,
                                        ),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Taille du jeu test"
                                        ),

                                        dcc.Slider(
                                            id="eaie-test-size",
                                            min=0.15,
                                            max=0.40,
                                            step=0.05,
                                            value=0.20,
                                            marks={
                                                0.15: "15 %",
                                                0.20: "20 %",
                                                0.25: "25 %",
                                                0.30: "30 %",
                                                0.40: "40 %",
                                            },
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Validation croisée"
                                        ),

                                        dcc.Dropdown(
                                            id="eaie-cv",
                                            options=[
                                                {
                                                    "label": "3 folds",
                                                    "value": 3,
                                                },
                                                {
                                                    "label": "5 folds",
                                                    "value": 5,
                                                },
                                                {
                                                    "label": "10 folds",
                                                    "value": 10,
                                                },
                                            ],
                                            value=5,
                                            clearable=False,
                                        ),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3 mt-2",
                        ),

                        dbc.Button(
                            "Lancer la modélisation",
                            id="eaie-run",
                            color="primary",
                            className="mt-4",
                        ),

                        dbc.Spinner(
                            html.Div(
                                id="eaie-status",
                                className="mt-3",
                            )
                        ),
                    ]
                ),
                className="mb-4",
            ),

            dbc.Tabs(
                [
                    dbc.Tab(
                        [
                            html.Div(
                                id="eaie-summary",
                                className="mt-4",
                            )
                        ],
                        label="Synthèse",
                    ),

                    dbc.Tab(
                        [
                            html.Div(
                                id="eaie-comparison",
                                className="mt-4",
                            )
                        ],
                        label="Comparaison",
                    ),

                    dbc.Tab(
                        [
                            html.Div(
                                id="eaie-best-model",
                                className="mt-4",
                            )
                        ],
                        label="Modèle sélectionné",
                    ),

                    dbc.Tab(
                        [
                            html.Div(
                                id="eaie-evaluation",
                                className="mt-4",
                            )
                        ],
                        label="Évaluation",
                    ),
                ]
            ),

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← EKDE",
                                color="secondary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/ekde"
                            ),
                        ),
                        md=6,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "EXAIE →",
                                color="success",
                                outline=True,
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/exaie"
                            ),
                        ),
                        md=6,
                    ),
                ],
                className="g-3 mt-3",
            ),

            dcc.Store(
                id="eaie-data",
                data=df.to_json(
                    orient="split",
                    date_format="iso",
                ),
            ),

            dcc.Store(
                id="eaie-result-store",
            ),
        ],
        fluid=True,
    )
