from __future__ import annotations

from dash import dcc
from dash import html

import dash_bootstrap_components as dbc


def _format_date(value):
    if value is None:
        return "—"

    return value.strftime(
        "%d/%m/%Y à %H:%M"
    )


def _status_badge(
    text,
    color,
    icon,
):
    return dbc.Badge(
        [
            html.I(
                className=f"bi {icon} me-1"
            ),
            text,
        ],
        color=color,
        pill=True,
        className="me-2",
    )


def account_layout(user):
    full_name = (
        f"{user.first_name} "
        f"{user.last_name}"
    ).strip()

    role_labels = {
        "user": "Utilisateur",
        "admin": "Administrateur",
        "super_admin": "Super administrateur",
    }

    role_label = role_labels.get(
        user.role,
        user.role,
    )

    return dbc.Container(
        [
            dcc.Location(
                id="account-refresh",
                refresh=True,
            ),

            # ==============================================
            # EN-TÊTE
            # ==============================================

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "ESPACE PERSONNEL",
                                className=(
                                    "module-home-v2-kicker"
                                ),
                            ),

                            html.H1(
                                "Mon compte",
                                className=(
                                    "module-home-v2-title"
                                ),
                            ),

                            html.P(
                                (
                                    "Gérez vos informations "
                                    "personnelles et la sécurité "
                                    "de votre compte EMIDAF."
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
                                "bi bi-person-gear "
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

            dbc.Row(
                [
                    # ======================================
                    # IDENTITÉ
                    # ======================================

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-person-circle"
                                            )
                                        ),
                                        className=(
                                            "account-avatar"
                                        ),
                                    ),

                                    html.H3(
                                        full_name,
                                        className=(
                                            "text-center mt-3 mb-1"
                                        ),
                                    ),

                                    html.Div(
                                        user.email,
                                        className=(
                                            "text-muted "
                                            "text-center"
                                        ),
                                    ),

                                    html.Div(
                                        [
                                            _status_badge(
                                                role_label,
                                                "secondary",
                                                "bi-shield",
                                            ),

                                            _status_badge(
                                                (
                                                    "Actif"
                                                    if user.is_active
                                                    else "Suspendu"
                                                ),
                                                (
                                                    "success"
                                                    if user.is_active
                                                    else "danger"
                                                ),
                                                (
                                                    "bi-check-circle"
                                                    if user.is_active
                                                    else "bi-x-circle"
                                                ),
                                            ),

                                            _status_badge(
                                                (
                                                    "Vérifié"
                                                    if user.is_verified
                                                    else "Non vérifié"
                                                ),
                                                (
                                                    "primary"
                                                    if user.is_verified
                                                    else "secondary"
                                                ),
                                                "bi-patch-check",
                                            ),
                                        ],
                                        className=(
                                            "text-center mt-3"
                                        ),
                                    ),

                                    html.Hr(),

                                    html.Div(
                                        [
                                            html.Small(
                                                "Institution",
                                                className=(
                                                    "text-muted"
                                                ),
                                            ),
                                            html.Div(
                                                user.institution
                                                or "Non renseignée",
                                                className=(
                                                    "fw-semibold mb-3"
                                                ),
                                            ),

                                            html.Small(
                                                "Pays",
                                                className=(
                                                    "text-muted"
                                                ),
                                            ),
                                            html.Div(
                                                user.country
                                                or "Non renseigné",
                                                className=(
                                                    "fw-semibold mb-3"
                                                ),
                                            ),

                                            html.Small(
                                                "Compte créé",
                                                className=(
                                                    "text-muted"
                                                ),
                                            ),
                                            html.Div(
                                                _format_date(
                                                    user.created_at
                                                ),
                                                className=(
                                                    "fw-semibold mb-3"
                                                ),
                                            ),

                                            html.Small(
                                                "Dernière connexion",
                                                className=(
                                                    "text-muted"
                                                ),
                                            ),
                                            html.Div(
                                                _format_date(
                                                    user.last_login_at
                                                ),
                                                className=(
                                                    "fw-semibold"
                                                ),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            className="h-100",
                        ),
                        lg=4,
                    ),

                    # ======================================
                    # FORMULAIRES
                    # ======================================

                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            "PROFIL",
                                            className=(
                                                "module-home-v2-kicker"
                                            ),
                                        ),

                                        html.H3(
                                            "Informations personnelles",
                                            className="mb-3",
                                        ),

                                        dbc.Alert(
                                            id=(
                                                "account-profile-alert"
                                            ),
                                            is_open=False,
                                        ),

                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Prénom"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-first-name"
                                                            ),
                                                            value=(
                                                                user.first_name
                                                            ),
                                                        ),
                                                    ],
                                                    md=6,
                                                ),

                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Nom"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-last-name"
                                                            ),
                                                            value=(
                                                                user.last_name
                                                            ),
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
                                                            "Adresse e-mail"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-email"
                                                            ),
                                                            type="email",
                                                            value=(
                                                                user.email
                                                            ),
                                                        ),
                                                    ],
                                                    md=12,
                                                ),

                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Institution"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-institution"
                                                            ),
                                                            value=(
                                                                user.institution
                                                                or ""
                                                            ),
                                                            placeholder=(
                                                                "Université, "
                                                                "école, "
                                                                "laboratoire..."
                                                            ),
                                                        ),
                                                    ],
                                                    md=6,
                                                ),

                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Pays"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-country"
                                                            ),
                                                            value=(
                                                                user.country
                                                                or ""
                                                            ),
                                                        ),
                                                    ],
                                                    md=6,
                                                ),
                                            ],
                                            className="g-3 mt-1",
                                        ),

                                        dbc.Button(
                                            [
                                                html.I(
                                                    className=(
                                                        "bi bi-check2-circle "
                                                        "me-2"
                                                    )
                                                ),
                                                "Enregistrer les modifications",
                                            ],
                                            id=(
                                                "account-profile-save"
                                            ),
                                            color="primary",
                                            className="mt-4",
                                        ),
                                    ]
                                )
                            ),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            "SÉCURITÉ",
                                            className=(
                                                "module-home-v2-kicker"
                                            ),
                                        ),

                                        html.H3(
                                            "Changer le mot de passe",
                                            className="mb-1",
                                        ),

                                        html.P(
                                            (
                                                "Le nouveau mot de passe "
                                                "doit contenir au moins "
                                                "10 caractères."
                                            ),
                                            className="text-muted",
                                        ),

                                        dbc.Alert(
                                            id=(
                                                "account-password-alert"
                                            ),
                                            is_open=False,
                                        ),

                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Mot de passe actuel"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-current-password"
                                                            ),
                                                            type="password",
                                                        ),
                                                    ],
                                                    md=12,
                                                ),

                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Nouveau mot de passe"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-new-password"
                                                            ),
                                                            type="password",
                                                        ),
                                                    ],
                                                    md=6,
                                                ),

                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Confirmer"
                                                        ),
                                                        dbc.Input(
                                                            id=(
                                                                "account-confirm-password"
                                                            ),
                                                            type="password",
                                                        ),
                                                    ],
                                                    md=6,
                                                ),
                                            ],
                                            className="g-3",
                                        ),

                                        dbc.Button(
                                            [
                                                html.I(
                                                    className=(
                                                        "bi bi-key me-2"
                                                    )
                                                ),
                                                "Changer le mot de passe",
                                            ],
                                            id=(
                                                "account-password-save"
                                            ),
                                            color="secondary",
                                            className="mt-4",
                                        ),
                                    ]
                                ),
                                className="mt-4",
                            ),
                        ],
                        lg=8,
                    ),
                ],
                className="g-4 mt-1",
            ),
        ],
        fluid=True,
        className="py-4",
    )
