from __future__ import annotations

from flask import session

from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import no_update

from emidaf_core.bootstrap.bootstrap import Bootstrap


def _bootstrap():
    bootstrap = Bootstrap()
    bootstrap.initialize()
    return bootstrap


def _current_user_id():
    value = session.get("user_id")

    if value is None:
        return None

    return int(value)


@callback(
    Output(
        "account-profile-alert",
        "children",
    ),
    Output(
        "account-profile-alert",
        "color",
    ),
    Output(
        "account-profile-alert",
        "is_open",
    ),
    Output(
        "account-refresh",
        "href",
    ),

    Input(
        "account-profile-save",
        "n_clicks",
    ),

    State(
        "account-first-name",
        "value",
    ),
    State(
        "account-last-name",
        "value",
    ),
    State(
        "account-email",
        "value",
    ),
    State(
        "account-institution",
        "value",
    ),
    State(
        "account-country",
        "value",
    ),

    prevent_initial_call=True,
)
def save_profile(
    n_clicks,
    first_name,
    last_name,
    email,
    institution,
    country,
):
    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
        )

    user_id = _current_user_id()

    if user_id is None:
        return (
            "Votre session a expiré.",
            "danger",
            True,
            "/login",
        )

    bootstrap = _bootstrap()

    try:
        bootstrap.user_service.update_profile(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            institution=institution,
            country=country,
        )

    except (
        ValueError,
        TypeError,
    ) as exc:
        return (
            str(exc),
            "danger",
            True,
            no_update,
        )

    return (
        "Profil mis à jour avec succès.",
        "success",
        True,
        "/account",
    )


@callback(
    Output(
        "account-password-alert",
        "children",
    ),
    Output(
        "account-password-alert",
        "color",
    ),
    Output(
        "account-password-alert",
        "is_open",
    ),
    Output(
        "account-current-password",
        "value",
    ),
    Output(
        "account-new-password",
        "value",
    ),
    Output(
        "account-confirm-password",
        "value",
    ),

    Input(
        "account-password-save",
        "n_clicks",
    ),

    State(
        "account-current-password",
        "value",
    ),
    State(
        "account-new-password",
        "value",
    ),
    State(
        "account-confirm-password",
        "value",
    ),

    prevent_initial_call=True,
)
def change_password(
    n_clicks,
    current_password,
    new_password,
    confirm_password,
):
    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    user_id = _current_user_id()

    if user_id is None:
        return (
            "Votre session a expiré.",
            "danger",
            True,
            "",
            "",
            "",
        )

    if (
        not current_password
        or not new_password
        or not confirm_password
    ):
        return (
            "Veuillez renseigner les trois champs.",
            "warning",
            True,
            no_update,
            no_update,
            no_update,
        )

    if new_password != confirm_password:
        return (
            "Les nouveaux mots de passe "
            "ne correspondent pas.",
            "warning",
            True,
            no_update,
            no_update,
            no_update,
        )

    bootstrap = _bootstrap()

    try:
        bootstrap.user_service.change_password(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password,
        )

    except (
        ValueError,
        TypeError,
    ) as exc:
        return (
            str(exc),
            "danger",
            True,
            no_update,
            no_update,
            no_update,
        )

    return (
        "Mot de passe modifié avec succès.",
        "success",
        True,
        "",
        "",
        "",
    )
