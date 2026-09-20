from __future__ import annotations

from flask import session

from dash import Input
from dash import Output
from dash import callback
from dash import html

import dash_bootstrap_components as dbc

from emidaf_core.bootstrap.bootstrap import Bootstrap


def _current_user():
    user_id = session.get("user_id")

    if user_id is None:
        return None

    bootstrap = Bootstrap()
    bootstrap.initialize()

    return (
        bootstrap.auth_service
        .get_current_user(
            int(user_id)
        )
    )


def _anonymous_menu():
    return dbc.Button(
        [
            html.I(
                className="bi bi-box-arrow-in-right me-2"
            ),
            "Se connecter",
        ],
        href="/login",
        color="light",
        size="sm",
    )


def _authenticated_menu(user):
    full_name = (
        f"{user.first_name} "
        f"{user.last_name}"
    ).strip()

    items = [
        dbc.DropdownMenuItem(
            [
                html.I(
                    className="bi bi-speedometer2 me-2"
                ),
                "Tableau de bord",
            ],
            href="/dashboard",
        ),

        dbc.DropdownMenuItem(
            [
                html.I(
                    className="bi bi-folder2-open me-2"
                ),
                "Mes projets",
            ],
            href="/projects",
        ),
    ]

    if user.role in {
        "admin",
        "super_admin",
    }:
        items.extend(
            [
                dbc.DropdownMenuItem(
                    divider=True
                ),

                dbc.DropdownMenuItem(
                    [
                        html.I(
                            className="bi bi-shield-lock me-2"
                        ),
                        "Administration",
                    ],
                    href="/admin",
                ),
            ]
        )

    items.extend(
        [
            dbc.DropdownMenuItem(
                divider=True
            ),

            dbc.DropdownMenuItem(
                [
                    html.I(
                        className="bi bi-person-gear me-2"
                    ),
                    "Mon compte",
                ],
                href="/account",
            ),

            dbc.DropdownMenuItem(
                [
                    html.I(
                        className="bi bi-box-arrow-right me-2"
                    ),
                    "Déconnexion",
                ],
                href="/logout",
                external_link=True,
                className="text-danger fw-semibold",
            ),
        ]
    )

    return dbc.DropdownMenu(
        items,
        label=html.Span(
            [
                html.I(
                    className="bi bi-person-circle me-2"
                ),
                full_name,
            ]
        ),
        align_end=True,
        color="light",
        className="emidaf-user-menu",
    )


@callback(
    Output(
        "navbar-user-menu",
        "children",
    ),
    Input(
        "url",
        "pathname",
    ),
)
def update_navbar_user_menu(pathname):
    user = _current_user()

    if user is None:
        return _anonymous_menu()

    return _authenticated_menu(user)
