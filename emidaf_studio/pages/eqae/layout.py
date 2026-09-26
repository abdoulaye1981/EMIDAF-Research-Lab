"""
=========================================================
EMIDAF Studio
EQAE - Qualitative Analysis Engine
=========================================================
"""

from __future__ import annotations

import dash_bootstrap_components as dbc

from dash import (
    dcc,
    html,
)


def build_eqae_layout(
    *,
    project_id: str | int,
    dataset_id: str | int,
):
    """
    Layout principal EQAE.

    EQAE prend en charge l'analyse qualitative
    interprétative avec validation du chercheur.
    """

    return dbc.Container(
        [
            dcc.Store(
                id="eqae-project-id",
                data=project_id,
            ),

            dcc.Store(
                id="eqae-dataset-id",
                data=dataset_id,
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(
                                "EQAE"
                            ),
                            html.P(
                                "EMIDAF Qualitative Analysis Engine"
                            ),
                        ]
                    ),
                ],
                className="mb-3",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Analyse qualitative : "
                    ),
                    (
                        "codez et interprétez les données "
                        "qualitatives en conservant le "
                        "chercheur au centre du processus "
                        "analytique."
                    ),
                ],
                color="info",
                className="mb-4",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Principe méthodologique : "
                    ),
                    (
                        "les suggestions automatiques ou "
                        "issues d'ETAE ne constituent pas "
                        "des résultats qualitatifs validés. "
                        "Le chercheur conserve la décision "
                        "d'accepter, modifier ou rejeter "
                        "les propositions de codage."
                    ),
                ],
                color="light",
                className="mb-4",
            ),

            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Corpus",
                        tab_id="eqae-tab-corpus",
                    ),
                    dbc.Tab(
                        label="Codebook",
                        tab_id="eqae-tab-codebook",
                    ),
                    dbc.Tab(
                        label="Codage",
                        tab_id="eqae-tab-coding",
                    ),
                    dbc.Tab(
                        label="Codage assisté",
                        tab_id="eqae-tab-assisted",
                    ),
                    dbc.Tab(
                        label="Thèmes",
                        tab_id="eqae-tab-themes",
                    ),
                    dbc.Tab(
                        label="Verbatims",
                        tab_id="eqae-tab-quotations",
                    ),
                    dbc.Tab(
                        label="Cooccurrences",
                        tab_id="eqae-tab-cooccurrence",
                    ),
                    dbc.Tab(
                        label="Mémos",
                        tab_id="eqae-tab-memos",
                    ),
                    dbc.Tab(
                        label="Synthèse",
                        tab_id="eqae-tab-summary",
                    ),
                ],
                id="eqae-tabs",
                active_tab="eqae-tab-corpus",
                className="mb-3",
            ),

            dcc.Loading(
                html.Div(
                    id="eqae-tab-content"
                ),
                type="default",
            ),

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← ETAE",
                                color="secondary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/etae"
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
