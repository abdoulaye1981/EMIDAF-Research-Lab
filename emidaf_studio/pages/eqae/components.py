"""
=========================================================
EMIDAF Studio
EQAE - UI Components
=========================================================
"""

from __future__ import annotations

import dash_bootstrap_components as dbc

from dash import html


def eqae_intro_component(
    title: str,
    description: str,
    *,
    note: str | None = None,
):
    """
    Composant introductif homogène pour les onglets EQAE.
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
