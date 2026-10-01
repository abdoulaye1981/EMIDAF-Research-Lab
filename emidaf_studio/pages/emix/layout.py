"""
=========================================================
EMIDAF Framework v1.0
EMIX Studio - Layout
=========================================================
"""

from __future__ import annotations

from dash import (
    dcc,
    html,
)
import dash_bootstrap_components as dbc


def build_emix_layout(
    project_id: int,
    dataset_id: int,
):
    """
    Layout principal EMIX.

    EMIX organise l'intégration de résultats
    quantitatifs, textuels et qualitatifs.

    Les relations scientifiques et les
    méta-inférences restent sous validation
    explicite du chercheur.
    """

    return dbc.Container(
        [
            dcc.Store(
                id="emix-project-id",
                data=project_id,
            ),
            dcc.Store(
                id="emix-dataset-id",
                data=dataset_id,
            ),
            dcc.Store(
                id="emix-selected-sources",
                data=[],
            ),

            dbc.Row(
                dbc.Col(
                    [
                        html.H2(
                            "EMIX",
                            className="mb-1",
                        ),
                        html.H5(
                            (
                                "Mixed Methods "
                                "Integration Engine"
                            ),
                            className=(
                                "text-muted mb-3"
                            ),
                        ),
                        html.P(
                            (
                                "Intégration structurée "
                                "des résultats issus des "
                                "différents moteurs EMIDAF."
                            ),
                            className="mb-2",
                        ),
                        dbc.Alert(
                            (
                                "EMIX assiste le "
                                "rapprochement des résultats, "
                                "mais ne transforme pas "
                                "automatiquement une association "
                                "quantitative et un résultat "
                                "qualitatif en conclusion "
                                "scientifique ou causale."
                            ),
                            color="info",
                            className="mb-4",
                        ),
                    ]
                )
            ),

            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Sources",
                        tab_id="emix-tab-sources",
                    ),
                    dbc.Tab(
                        label="Candidats",
                        tab_id="emix-tab-candidates",
                    ),
                    dbc.Tab(
                        label="Intégration",
                        tab_id="emix-tab-integration",
                    ),
                    dbc.Tab(
                        label="Joint Display",
                        tab_id="emix-tab-joint-display",
                    ),
                    dbc.Tab(
                        label="Méta-inférences",
                        tab_id="emix-tab-inferences",
                    ),
                    dbc.Tab(
                        label="Synthèse",
                        tab_id="emix-tab-summary",
                    ),
                ],
                id="emix-tabs",
                active_tab="emix-tab-sources",
                className="mb-4",
            ),

            html.Div(
                id="emix-tab-content",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "Retour à EQAE",
                                color="secondary",
                                outline=True,
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/eqae"
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
