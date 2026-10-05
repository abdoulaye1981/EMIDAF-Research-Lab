
from dash import html, dcc
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset
from emidaf_core.dataset.profiler import DatasetProfiler
from emidaf_studio.pages.elae.labels import (
    variable_label,
)


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

    profiler = DatasetProfiler()
    profile = profiler.profile(df)

    datatypes = profile.datatypes or {}

    numeric = datatypes.get(
        "numeric",
        [],
    )

    categorical = datatypes.get(
        "categorical",
        [],
    )

    boolean = datatypes.get(
        "boolean",
        [],
    )

    text_columns = datatypes.get(
        "text",
        [],
    )

    identifiers = datatypes.get(
        "identifier",
        [],
    )

    datetime_columns = datatypes.get(
        "datetime",
        [],
    )

    # --------------------------------------------------------
    # Colonnes autorisées dans les analyses ELAE
    # --------------------------------------------------------
    # Les identifiants et le texte libre sont volontairement
    # exclus des sélecteurs analytiques.
    #
    # Les booléennes restent analysables comme variables
    # binaires/catégorielles et non comme quantitatives.
    # --------------------------------------------------------

    univariate_columns = (
        list(numeric)
        + list(categorical)
        + list(boolean)
        + list(datetime_columns)
    )

    bivariate_columns = list(
        univariate_columns
    )

    group_columns = (
        list(categorical)
        + list(boolean)
    )

    value_columns = list(
        numeric
    )

    return dbc.Container(
        [
            html.H2(
                "Analyse exploratoire des données : ELAE",
                className="mt-3",
            ),

            html.P(
                (
                    "Explorez les distributions, relations et principales "
                    "caractéristiques du jeu de données avant toute "
                    "modélisation. Les résultats sont descriptifs et "
                    "ne constituent pas, à eux seuls, des relations causales."
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
                        md=2,
                    ),
                    dbc.Col(
                        _card(
                            "Colonnes",
                            df.shape[1],
                        ),
                        md=2,
                    ),
                    dbc.Col(
                        _card(
                            "Numériques",
                            len(numeric),
                        ),
                        md=2,
                    ),
                    dbc.Col(
                        _card(
                            "Catégorielles",
                            len(categorical),
                        ),
                        md=2,
                    ),
                    dbc.Col(
                        _card(
                            "Booléennes",
                            len(boolean),
                        ),
                        md=2,
                    ),
                    dbc.Col(
                        _card(
                            "Texte",
                            len(text_columns),
                        ),
                        md=2,
                    ),
                    dbc.Col(
                        _card(
                            "Identifiants",
                            len(identifiers),
                        ),
                        md=2,
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
                                "Statistiques descriptives",
                                className="mt-4",
                            ),

                            html.Div(
                                id="elae-descriptive",
                            ),
                        ],
                        label="Résumé descriptif",
                        tab_id="descriptive",
                    ),

                    # ==========================================
                    # UNIVARIATE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Analyse univariée",
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
                                    for column in univariate_columns
                                ],
                                value=(
                                    univariate_columns[0]
                                    if univariate_columns
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
                        tab_id="univariate",
                    ),

                    # ==========================================
                    # BIVARIATE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Analyse bivariée",
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
                                                    for c in bivariate_columns
                                                ],
                                                value=(
                                                    bivariate_columns[0]
                                                    if bivariate_columns
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
                                                    for c in bivariate_columns
                                                ],
                                                value=(
                                                    bivariate_columns[1]
                                                    if len(bivariate_columns) > 1
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
                        tab_id="bivariate",
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
                        tab_id="correlations",
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
                                                    for c in group_columns
                                                ],
                                                value=(
                                                    group_columns[0]
                                                    if group_columns
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
                                                    for c in value_columns
                                                ],
                                                value=(
                                                    value_columns[0]
                                                    if value_columns
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
                        tab_id="grouped",
                    ),
                ],
                id="elae-tabs",
                active_tab="descriptive",
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
                                "Prétraitement",
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
                                "Ouvrir ETAE",
                                color="success",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/etae"
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


            dcc.Download(
                id="elae-download-data"
            ),
        ],
        fluid=True,
    )
