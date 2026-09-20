from __future__ import annotations

from dash import dcc
from dash import html

import dash_bootstrap_components as dbc


def _metric_card(
    label,
    value,
    icon,
):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.I(
                                    className=(
                                        f"bi {icon} me-2"
                                    )
                                ),
                                label,
                            ],
                            className="text-muted",
                        ),
                    ],
                    className=(
                        "d-flex justify-content-between "
                        "align-items-center"
                    ),
                ),
                html.H2(
                    str(value),
                    className="mt-2 mb-0",
                ),
            ]
        ),
        className="h-100",
    )


def _role_badge(role):
    if role == "super_admin":
        color = "danger"

    elif role == "admin":
        color = "warning"

    else:
        color = "secondary"

    return dbc.Badge(
        role,
        color=color,
        pill=True,
    )


def _admin_user_rows(
    current_user,
    users,
    project_counts,
):
    rows = []

    for item in users:
        is_self = (
            int(item.id)
            == int(current_user.id)
        )

        protected_super_admin = (
            item.role == "super_admin"
        )

        rows.append(
            html.Tr(
                [
                    html.Td(
                        str(item.id)
                    ),

                    html.Td(
                        [
                            html.Div(
                                (
                                    f"{item.first_name} "
                                    f"{item.last_name}"
                                ),
                                className="fw-semibold",
                            ),
                            html.Small(
                                (
                                    item.institution
                                    or "Institution non renseignée"
                                ),
                                className="text-muted",
                            ),
                        ]
                    ),

                    html.Td(
                        item.email
                    ),

                    html.Td(
                        _role_badge(
                            item.role
                        )
                    ),

                    html.Td(
                        dbc.Badge(
                            (
                                "Actif"
                                if item.is_active
                                else "Suspendu"
                            ),
                            color=(
                                "success"
                                if item.is_active
                                else "danger"
                            ),
                            pill=True,
                        )
                    ),

                    html.Td(
                        dbc.Badge(
                            (
                                "Vérifié"
                                if item.is_verified
                                else "Non vérifié"
                            ),
                            color=(
                                "primary"
                                if item.is_verified
                                else "secondary"
                            ),
                            pill=True,
                        )
                    ),

                    html.Td(
                        str(
                            project_counts.get(
                                int(item.id),
                                0,
                            )
                        )
                    ),

                    html.Td(
                        (
                            item.created_at.strftime(
                                "%d/%m/%Y %H:%M"
                            )
                            if item.created_at
                            else "—"
                        )
                    ),

                    html.Td(
                        (
                            item.last_login_at.strftime(
                                "%d/%m/%Y %H:%M"
                            )
                            if item.last_login_at
                            else "Jamais"
                        )
                    ),

                    html.Td(
                        dbc.ButtonGroup(
                            [
                                dbc.Button(
                                    (
                                        "Suspendre"
                                        if item.is_active
                                        else "Activer"
                                    ),
                                    id={
                                        "type": (
                                            "admin-toggle-active"
                                        ),
                                        "index": int(item.id),
                                    },
                                    size="sm",
                                    color=(
                                        "outline-danger"
                                        if item.is_active
                                        else "outline-success"
                                    ),
                                    disabled=(
                                        is_self
                                        or protected_super_admin
                                    ),
                                ),

                                dbc.Button(
                                    (
                                        "Dé-vérifier"
                                        if item.is_verified
                                        else "Vérifier"
                                    ),
                                    id={
                                        "type": (
                                            "admin-toggle-verified"
                                        ),
                                        "index": int(item.id),
                                    },
                                    size="sm",
                                    color="outline-primary",
                                    disabled=(
                                        is_self
                                        or protected_super_admin
                                    ),
                                ),

                                dbc.DropdownMenu(
                                    [
                                        dbc.DropdownMenuItem(
                                            "Utilisateur",
                                            id={
                                                "type": (
                                                    "admin-set-role-user"
                                                ),
                                                "index": int(item.id),
                                            },
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Administrateur",
                                            id={
                                                "type": (
                                                    "admin-set-role-admin"
                                                ),
                                                "index": int(item.id),
                                            },
                                        ),
                                    ],
                                    label="Rôle",
                                    size="sm",
                                    color="outline-secondary",
                                    disabled=(
                                        is_self
                                        or protected_super_admin
                                    ),
                                ),
                            ],
                            size="sm",
                        )
                    ),
                ]
            )
        )

    return rows


def admin_layout(
    user,
    users,
    project_counts,
):
    total_users = len(users)

    active_users = sum(
        1
        for item in users
        if item.is_active
    )

    verified_users = sum(
        1
        for item in users
        if item.is_verified
    )

    administrators = sum(
        1
        for item in users
        if item.role in {
            "admin",
            "super_admin",
        }
    )

    rows = _admin_user_rows(
        user,
        users,
        project_counts,
    )

    return dbc.Container(
        [
            # ==============================================
            # HERO
            # ==============================================

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "ADMINISTRATION EMIDAF",
                                className=(
                                    "module-home-v2-kicker"
                                ),
                            ),
                            html.H1(
                                "Centre d'administration",
                                className=(
                                    "module-home-v2-title"
                                ),
                            ),
                            html.P(
                                (
                                    "Supervision des utilisateurs, "
                                    "des accès et de l'activité "
                                    "de la plateforme."
                                ),
                                className=(
                                    "module-home-v2-subtitle"
                                ),
                            ),
                        ]
                    ),
                    html.Div(
                        html.I(
                            className=(
                                "bi bi-shield-lock "
                                "module-home-v2-hero-icon"
                            )
                        ),
                        className=(
                            "module-home-v2-hero-icon-box"
                        ),
                    ),
                ],
                className="module-home-v2-hero",
            ),

            # ==============================================
            # INDICATEURS
            # ==============================================

            dbc.Row(
                [
                    dbc.Col(
                        _metric_card(
                            "Utilisateurs",
                            total_users,
                            "bi-people",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _metric_card(
                            "Comptes actifs",
                            active_users,
                            "bi-person-check",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _metric_card(
                            "Comptes vérifiés",
                            verified_users,
                            "bi-patch-check",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        _metric_card(
                            "Administrateurs",
                            administrators,
                            "bi-shield-check",
                        ),
                        md=3,
                    ),
                ],
                className="g-3 mt-3",
            ),

            # ==============================================
            # UTILISATEURS
            # ==============================================

            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            "GESTION DES ACCÈS",
                                            className=(
                                                "module-home-v2-kicker"
                                            ),
                                        ),
                                        html.H3(
                                            "Utilisateurs",
                                            className="mb-1",
                                        ),
                                        html.P(
                                            (
                                                "Consultez les comptes, "
                                                "leurs rôles, leur activité "
                                                "et leurs projets."
                                            ),
                                            className="text-muted mb-0",
                                        ),
                                    ],
                                    md=7,
                                ),

                                dbc.Col(
                                    dbc.Input(
                                        id="admin-user-search",
                                        type="search",
                                        placeholder=(
                                            "Rechercher un utilisateur..."
                                        ),
                                    ),
                                    md=5,
                                    className="d-flex align-items-center",
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Alert(
                            id="admin-user-alert",
                            is_open=False,
                            className="mt-3",
                        ),

                        html.Div(
                            dbc.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [
                                                html.Th("ID"),
                                                html.Th("Utilisateur"),
                                                html.Th("E-mail"),
                                                html.Th("Rôle"),
                                                html.Th("État"),
                                                html.Th("Vérification"),
                                                html.Th("Projets"),
                                                html.Th("Création"),
                                                html.Th(
                                                    "Dernière connexion"
                                                ),
                                                html.Th("Actions"),
                                            ]
                                        )
                                    ),
                                    html.Tbody(
                                        rows,
                                        id=(
                                            "admin-users-table-body"
                                        ),
                                    ),
                                ],
                                hover=True,
                                responsive=True,
                                className="align-middle mb-0",
                            ),
                            className="table-responsive mt-4",
                        ),
                    ]
                ),
                className="mt-4",
            ),

            dcc.Store(
                id="admin-refresh-token",
                data=0,
            ),
        ],
        fluid=True,
        className="py-4",
    )
