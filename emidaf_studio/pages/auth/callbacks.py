from __future__ import annotations

from flask import session

from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import no_update

from emidaf_core.bootstrap.bootstrap import Bootstrap


bootstrap = Bootstrap()
bootstrap.initialize()

auth_service = bootstrap.auth_service


@callback(
    Output(
        "login-alert",
        "children",
    ),
    Output(
        "login-alert",
        "color",
    ),
    Output(
        "login-alert",
        "is_open",
    ),
    Output(
        "url",
        "pathname",
        allow_duplicate=True,
    ),
    Input(
        "login-submit",
        "n_clicks",
    ),
    State(
        "login-email",
        "value",
    ),
    State(
        "login-password",
        "value",
    ),
    prevent_initial_call=True,
)
def login_user(
    n_clicks,
    email,
    password,
):
    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if not email or not password:
        return (
            "Veuillez renseigner votre e-mail "
            "et votre mot de passe.",
            "warning",
            True,
            no_update,
        )

    user = auth_service.authenticate(
        email,
        password,
    )

    if user is None:
        return (
            "Identifiants incorrects ou compte inactif.",
            "danger",
            True,
            no_update,
        )

    session.clear()

    session["user_id"] = int(user.id)
    session["role"] = user.role

    session.permanent = True

    destination = (
        "/admin"
        if user.role in {
            "admin",
            "super_admin",
        }
        else "/dashboard"
    )

    return (
        "Connexion réussie.",
        "success",
        True,
        destination,
    )


@callback(
    Output(
        "register-alert",
        "children",
    ),
    Output(
        "register-alert",
        "color",
    ),
    Output(
        "register-alert",
        "is_open",
    ),
    Output(
        "url",
        "pathname",
        allow_duplicate=True,
    ),
    Input(
        "register-submit",
        "n_clicks",
    ),
    State(
        "register-first-name",
        "value",
    ),
    State(
        "register-last-name",
        "value",
    ),
    State(
        "register-email",
        "value",
    ),
    State(
        "register-institution",
        "value",
    ),
    State(
        "register-country",
        "value",
    ),
    State(
        "register-password",
        "value",
    ),
    State(
        "register-password-confirm",
        "value",
    ),
    State(
        "register-terms",
        "value",
    ),
    prevent_initial_call=True,
)
def register_user(
    n_clicks,
    first_name,
    last_name,
    email,
    institution,
    country,
    password,
    password_confirm,
    terms,
):
    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if not all(
        [
            first_name,
            last_name,
            email,
            password,
            password_confirm,
        ]
    ):
        return (
            "Veuillez compléter les champs obligatoires.",
            "warning",
            True,
            no_update,
        )

    if password != password_confirm:
        return (
            "Les mots de passe ne correspondent pas.",
            "danger",
            True,
            no_update,
        )

    if not terms:
        return (
            "Vous devez accepter les conditions "
            "d'utilisation.",
            "warning",
            True,
            no_update,
        )

    try:
        user = auth_service.register(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            institution=institution,
            country=country,
            role="user",
            is_verified=False,
        )

    except ValueError as exc:
        return (
            str(exc),
            "danger",
            True,
            no_update,
        )

    session.clear()

    session["user_id"] = int(user.id)
    session["role"] = user.role
    session.permanent = True

    return (
        "Compte créé avec succès.",
        "success",
        True,
        "/dashboard",
    )
