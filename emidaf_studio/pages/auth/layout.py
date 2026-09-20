from __future__ import annotations

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def _auth_brand():
    return html.Div(
        [
            html.Div(
                html.I(
                    className="bi bi-hexagon-fill"
                ),
                className="auth-v1-brand-icon",
            ),
            html.Div(
                [
                    html.Div(
                        "EMIDAF",
                        className="auth-v1-brand-title",
                    ),
                    html.Div(
                        "Research Lab",
                        className="auth-v1-brand-subtitle",
                    ),
                ]
            ),
        ],
        className="auth-v1-brand",
    )


def login_layout():
    return html.Div(
        [
            html.Div(
                [
                    _auth_brand(),
                    html.Div(
                        "PLATEFORME SCIENTIFIQUE",
                        className="auth-v1-kicker",
                    ),
                    html.H1(
                        "Connexion",
                        className="auth-v1-title",
                    ),
                    html.P(
                        (
                            "Accédez à votre espace scientifique "
                            "EMIDAF, à vos projets et à vos analyses."
                        ),
                        className="auth-v1-subtitle",
                    ),
                    dbc.Alert(
                        id="login-alert",
                        is_open=False,
                        className="mt-3",
                    ),
                    dbc.Label(
                        "Adresse e-mail",
                        html_for="login-email",
                    ),
                    dbc.Input(
                        id="login-email",
                        type="email",
                        placeholder="nom@institution.org",
                        autocomplete="email",
                    ),
                    dbc.Label(
                        "Mot de passe",
                        html_for="login-password",
                        className="mt-3",
                    ),
                    dbc.Input(
                        id="login-password",
                        type="password",
                        placeholder="Votre mot de passe",
                        autocomplete="current-password",
                    ),
                    dbc.Button(
                        [
                            html.I(
                                className="bi bi-box-arrow-in-right me-2"
                            ),
                            "Se connecter",
                        ],
                        id="login-submit",
                        color="primary",
                        className="w-100 mt-4",
                    ),
                    html.Div(
                        [
                            "Vous n'avez pas encore de compte ? ",
                            dcc.Link(
                                "Créer un compte",
                                href="/register",
                            ),
                        ],
                        className="auth-v1-switch",
                    ),
                ],
                className="auth-v1-card",
            )
        ],
        className="auth-v1-page",
    )


def register_layout():
    return html.Div(
        [
            html.Div(
                [
                    _auth_brand(),
                    html.Div(
                        "CRÉATION DE COMPTE",
                        className="auth-v1-kicker",
                    ),
                    html.H1(
                        "Rejoindre EMIDAF",
                        className="auth-v1-title",
                    ),
                    html.P(
                        (
                            "Créez votre espace personnel pour "
                            "organiser vos projets et analyses."
                        ),
                        className="auth-v1-subtitle",
                    ),
                    dbc.Alert(
                        id="register-alert",
                        is_open=False,
                        className="mt-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label("Prénom(s)"),
                                    dbc.Input(
                                        id="register-first-name",
                                        type="text",
                                    ),
                                ],
                                md=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Nom"),
                                    dbc.Input(
                                        id="register-last-name",
                                        type="text",
                                    ),
                                ],
                                md=6,
                            ),
                        ],
                        className="g-3",
                    ),
                    dbc.Label(
                        "Adresse e-mail",
                        className="mt-3",
                    ),
                    dbc.Input(
                        id="register-email",
                        type="email",
                        autocomplete="email",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label(
                                        "Institution",
                                        className="mt-3",
                                    ),
                                    dbc.Input(
                                        id="register-institution",
                                        type="text",
                                    ),
                                ],
                                md=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label(
                                        "Pays",
                                        className="mt-3",
                                    ),
                                    dbc.Input(
                                        id="register-country",
                                        type="text",
                                    ),
                                ],
                                md=6,
                            ),
                        ],
                        className="g-3",
                    ),
                    dbc.Label(
                        "Mot de passe",
                        className="mt-3",
                    ),
                    dbc.Input(
                        id="register-password",
                        type="password",
                        autocomplete="new-password",
                    ),
                    dbc.Label(
                        "Confirmation du mot de passe",
                        className="mt-3",
                    ),
                    dbc.Input(
                        id="register-password-confirm",
                        type="password",
                        autocomplete="new-password",
                    ),
                    dbc.Checkbox(
                        id="register-terms",
                        label=(
                            "J'accepte les conditions "
                            "d'utilisation et la politique "
                            "de confidentialité."
                        ),
                        className="mt-3",
                    ),
                    dbc.Button(
                        [
                            html.I(
                                className="bi bi-person-plus me-2"
                            ),
                            "Créer mon compte",
                        ],
                        id="register-submit",
                        color="primary",
                        className="w-100 mt-4",
                    ),
                    html.Div(
                        [
                            "Vous avez déjà un compte ? ",
                            dcc.Link(
                                "Se connecter",
                                href="/login",
                            ),
                        ],
                        className="auth-v1-switch",
                    ),
                ],
                className="auth-v1-card auth-v1-card-wide",
            )
        ],
        className="auth-v1-page",
    )
