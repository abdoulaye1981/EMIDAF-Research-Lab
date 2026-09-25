"""
=========================================================
EMIDAF Studio
ETAE - Text Analysis Engine
=========================================================
"""

from __future__ import annotations

import dash_bootstrap_components as dbc

from dash import (
    dcc,
    html,
)


def build_etae_layout(
    *,
    project_id: str,
    dataset_id: str,
):
    """
    Layout principal ETAE.

    Les analyses sont chargées dynamiquement
    par les callbacks.
    """

    return dbc.Container(
        [
            dcc.Store(
                id="etae-project-id",
                data=project_id,
            ),
            dcc.Store(
                id="etae-dataset-id",
                data=dataset_id,
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(
                                "ETAE"
                            ),
                            html.P(
                                "EMIDAF Text Analysis Engine"
                            ),
                        ]
                    ),
                ],
                className="mb-3",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Analyse textuelle : "
                    ),
                    (
                        "sélectionnez une variable "
                        "contenant du texte libre."
                    ),
                ],
                color="info",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Label(
                            "Variable textuelle"
                        ),
                        dcc.Dropdown(
                            id="etae-text-column",
                            options=[],
                            value=None,
                            clearable=False,
                            placeholder=(
                                "Sélectionner une "
                                "colonne textuelle"
                            ),
                        ),

                        html.Div(
                            id="etae-text-column-status",
                            className="mt-2",
                        ),
                    ]
                ),
                className="mb-4",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Label(
                            "Variable structurée pour les associations"
                        ),
                        dcc.Dropdown(
                            id="etae-association-target",
                            options=[],
                            value=None,
                            clearable=True,
                            placeholder=(
                                "Sélectionner une variable "
                                "à comparer au texte"
                            ),
                        ),
                    ]
                ),
                className="mb-4",
            ),

            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Corpus",
                        tab_id="etae-tab-corpus",
                    ),
                    dbc.Tab(
                        label="Lexique",
                        tab_id="etae-tab-lexique",
                    ),
                    dbc.Tab(
                        label="N-grams",
                        tab_id="etae-tab-ngrams",
                    ),
                    dbc.Tab(
                        label="TF-IDF",
                        tab_id="etae-tab-tfidf",
                    ),
                    dbc.Tab(
                        label="Sentiment",
                        tab_id="etae-tab-sentiment",
                    ),
                    dbc.Tab(
                        label="Thèmes",
                        tab_id="etae-tab-topics",
                    ),
                    dbc.Tab(
                        label="Clusters",
                        tab_id="etae-tab-clusters",
                    ),
                    dbc.Tab(
                        label="Associations",
                        tab_id="etae-tab-associations",
                    ),
                ],
                id="etae-tabs",
                active_tab="etae-tab-corpus",
                className="mb-3",
            ),

            dcc.Loading(
                html.Div(
                    id="etae-tab-content"
                ),
                type="default",
            ),

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← ELAE",
                                color="secondary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/elae"
                            ),
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "Espace projet",
                                color="primary",
                                outline=True,
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                            ),
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "Ouvrir EKDE",
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
        ],
        fluid=True,
        className="py-4",
    )
