"""
=========================================================
EMIDAF Framework v1.0
EMIX Studio - Components
=========================================================
"""

from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc


def emix_intro_component(
    title: str,
    description: str,
    *,
    note: str | None = None,
):
    """
    Composant introductif homogène
    pour les onglets EMIX.
    """

    children = [
        html.H4(
            title,
            className="mb-3",
        ),
        html.P(
            description,
            className="text-muted",
        ),
    ]

    if note:
        children.append(
            dbc.Alert(
                note,
                color="light",
                className="mt-3 mb-0",
            )
        )

    return dbc.Card(
        dbc.CardBody(
            children
        ),
        className="shadow-sm",
    )


def emix_source_card(
    *,
    stage: str,
    label: str,
    family: str,
    available: bool,
    result_type: str | None = None,
    description: str = "",
):
    """
    Carte descriptive d'une source analytique EMIX.
    """

    badge = dbc.Badge(
        (
            "Disponible"
            if available
            else "Non disponible"
        ),
        color=(
            "success"
            if available
            else "secondary"
        ),
        className="ms-2",
    )

    body = [
        html.Div(
            [
                html.H5(
                    label,
                    className="mb-0",
                ),
                badge,
            ],
            className=(
                "d-flex align-items-center "
                "justify-content-between"
            ),
        ),
        html.Hr(),
        html.P(
            [
                html.Strong("Moteur : "),
                stage.upper(),
            ],
            className="mb-1",
        ),
        html.P(
            [
                html.Strong(
                    "Famille méthodologique : "
                ),
                family,
            ],
            className="mb-1",
        ),
    ]

    if result_type:
        body.append(
            html.P(
                [
                    html.Strong(
                        "Type de résultat : "
                    ),
                    result_type,
                ],
                className="mb-1",
            )
        )

    if description:
        body.append(
            html.P(
                description,
                className=(
                    "text-muted small mb-0 mt-2"
                ),
            )
        )

    return dbc.Card(
        dbc.CardBody(body),
        className="h-100 shadow-sm",
    )
