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

    numeric_columns = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    options = [
        {
            "label": column,
            "value": column,
        }
        for column in columns
    ]

    numeric_options = [
        {
            "label": column,
            "value": column,
        }
        for column in numeric_columns
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
                                            "Modèles à évaluer"
                                        ),

                                        dcc.Dropdown(
                                            id="eaie-models",
                                            options=[],
                                            value=[],
                                            multi=True,
                                            placeholder=(
                                                "Choisissez d'abord "
                                                "le type de problème"
                                            ),
                                        ),

                                        html.Small(
                                            (
                                                "Si aucun modèle n'est "
                                                "sélectionné, EAIE évalue "
                                                "tous les modèles disponibles "
                                                "pour la tâche choisie."
                                            ),
                                            className="text-muted",
                                        ),
                                    ],
                                    md=12,
                                ),
                            ],
                            className="g-3 mt-2",
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
                                            value=3,
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

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "Analyse statistique OLS"
                                    ),

                                    html.P(
                                        (
                                            "Régression linéaire par "
                                            "moindres carrés ordinaires "
                                            "avec inférence statistique."
                                        ),
                                        className="text-muted",
                                    ),

                                    dbc.Label(
                                        "Variable dépendante"
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ols-target",
                                        options=numeric_options,
                                        placeholder=(
                                            "Sélectionner la cible"
                                        ),
                                        clearable=True,
                                    ),

                                    dbc.Label(
                                        "Variables explicatives",
                                        className="mt-3",
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ols-features",
                                        options=numeric_options,
                                        multi=True,
                                        placeholder=(
                                            "Sélectionner les variables "
                                            "explicatives"
                                        ),
                                    ),

                                    dbc.Label(
                                        "Niveau alpha",
                                        className="mt-3",
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ols-alpha",
                                        options=[
                                            {
                                                "label": "10 %",
                                                "value": 0.10,
                                            },
                                            {
                                                "label": "5 %",
                                                "value": 0.05,
                                            },
                                            {
                                                "label": "1 %",
                                                "value": 0.01,
                                            },
                                        ],
                                        value=0.05,
                                        clearable=False,
                                    ),

                                    dbc.Button(
                                        "Exécuter OLS",
                                        id="eaie-ols-run",
                                        color="info",
                                        className="mt-3",
                                    ),

                                    dbc.Spinner(
                                        html.Div(
                                            id="eaie-ols-status",
                                            className="mt-3",
                                        )
                                    ),

                                    html.Div(
                                        id="eaie-ols-result",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            className="h-100",
                        ),
                        md=6,
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "Modèle multiniveau"
                                    ),

                                    html.P(
                                        (
                                            "Modèle linéaire à intercept "
                                            "aléatoire pour données "
                                            "hiérarchiques ou groupées."
                                        ),
                                        className="text-muted",
                                    ),

                                    dbc.Label(
                                        "Variable dépendante"
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ml-target",
                                        options=numeric_options,
                                        placeholder=(
                                            "Sélectionner la cible"
                                        ),
                                        clearable=True,
                                    ),

                                    dbc.Label(
                                        "Effets fixes",
                                        className="mt-3",
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ml-features",
                                        options=numeric_options,
                                        multi=True,
                                        placeholder=(
                                            "Sélectionner les effets fixes"
                                        ),
                                    ),

                                    dbc.Label(
                                        "Variable de groupe",
                                        className="mt-3",
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ml-group",
                                        options=options,
                                        placeholder=(
                                            "Sélectionner la variable "
                                            "de groupe"
                                        ),
                                        clearable=True,
                                    ),

                                    dbc.Label(
                                        "Méthode d'optimisation",
                                        className="mt-3",
                                    ),

                                    dcc.Dropdown(
                                        id="eaie-ml-method",
                                        options=[
                                            {
                                                "label": "L-BFGS",
                                                "value": "lbfgs",
                                            },
                                            {
                                                "label": "BFGS",
                                                "value": "bfgs",
                                            },
                                            {
                                                "label": "Conjugate Gradient",
                                                "value": "cg",
                                            },
                                        ],
                                        value="lbfgs",
                                        clearable=False,
                                    ),

                                    dcc.Checklist(
                                        id="eaie-ml-reml",
                                        options=[
                                            {
                                                "label": " Utiliser REML",
                                                "value": "reml",
                                            }
                                        ],
                                        value=[],
                                        className="mt-3",
                                    ),

                                    dbc.Button(
                                        "Exécuter le modèle multiniveau",
                                        id="eaie-ml-run",
                                        color="warning",
                                        className="mt-3",
                                    ),

                                    dbc.Spinner(
                                        html.Div(
                                            id="eaie-ml-status",
                                            className="mt-3",
                                        )
                                    ),

                                    html.Div(
                                        id="eaie-ml-result",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            className="h-100",
                        ),
                        md=6,
                    ),
                ],
                className="g-3 mb-4",
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
                id="eaie-project-id",
                data=project_id,
            ),
            dcc.Store(
                id="eaie-dataset-id",
                data=dataset_id,
            ),
        ],
        fluid=True,
    )
