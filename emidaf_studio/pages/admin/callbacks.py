from __future__ import annotations

from flask import session

from dash import ALL
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import ctx
from dash import no_update

from emidaf_core.bootstrap.bootstrap import Bootstrap


def _bootstrap():
    bootstrap = Bootstrap()
    bootstrap.initialize()
    return bootstrap


def _current_admin():
    user_id = session.get("user_id")

    if user_id is None:
        return None

    bootstrap = _bootstrap()

    user = (
        bootstrap.auth_service
        .get_current_user(
            int(user_id)
        )
    )

    if user is None:
        return None

    if user.role not in {
        "admin",
        "super_admin",
    }:
        return None

    return user


@callback(
    Output(
        "admin-user-alert",
        "children",
    ),
    Output(
        "admin-user-alert",
        "color",
    ),
    Output(
        "admin-user-alert",
        "is_open",
    ),
    Output(
        "admin-refresh-token",
        "data",
    ),

    Input(
        {
            "type": "admin-toggle-active",
            "index": ALL,
        },
        "n_clicks",
    ),
    Input(
        {
            "type": "admin-toggle-verified",
            "index": ALL,
        },
        "n_clicks",
    ),
    Input(
        {
            "type": "admin-set-role-user",
            "index": ALL,
        },
        "n_clicks",
    ),
    Input(
        {
            "type": "admin-set-role-admin",
            "index": ALL,
        },
        "n_clicks",
    ),

    State(
        "admin-refresh-token",
        "data",
    ),

    prevent_initial_call=True,
)
def manage_admin_users(
    active_clicks,
    verified_clicks,
    role_user_clicks,
    role_admin_clicks,
    refresh_token,
):
    admin = _current_admin()

    if admin is None:
        return (
            "Accès administrateur requis.",
            "danger",
            True,
            no_update,
        )

    triggered = ctx.triggered_id

    if not isinstance(
        triggered,
        dict,
    ):
        return (
            no_update,
            no_update,
            no_update,
            no_update,
        )

    target_id = int(
        triggered["index"]
    )

    if target_id == int(admin.id):
        return (
            (
                "Votre propre compte administrateur "
                "ne peut pas être modifié depuis cette page."
            ),
            "warning",
            True,
            no_update,
        )

    bootstrap = _bootstrap()

    target = (
        bootstrap.user_service
        .get(target_id)
    )

    if target is None:
        return (
            "Utilisateur introuvable.",
            "danger",
            True,
            no_update,
        )

    if target.role == "super_admin":
        return (
            (
                "Un compte super administrateur "
                "ne peut pas être modifié ici."
            ),
            "warning",
            True,
            no_update,
        )

    action = triggered["type"]

    try:
        if action == "admin-toggle-active":
            new_value = not target.is_active

            bootstrap.user_service.set_active(
                target_id,
                new_value,
            )

            message = (
                "Compte activé."
                if new_value
                else "Compte suspendu."
            )

        elif action == "admin-toggle-verified":
            new_value = not target.is_verified

            bootstrap.user_service.set_verified(
                target_id,
                new_value,
            )

            message = (
                "Compte vérifié."
                if new_value
                else "Vérification retirée."
            )

        elif action == "admin-set-role-user":
            bootstrap.user_service.set_role(
                target_id,
                "user",
            )

            message = (
                "Rôle utilisateur appliqué."
            )

        elif action == "admin-set-role-admin":
            bootstrap.user_service.set_role(
                target_id,
                "admin",
            )

            message = (
                "Rôle administrateur appliqué."
            )

        else:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
            )

    except Exception as exc:
        return (
            f"Erreur : {exc}",
            "danger",
            True,
            no_update,
        )

    return (
        message,
        "success",
        True,
        int(refresh_token or 0) + 1,
    )


@callback(
    Output(
        "admin-users-table-body",
        "children",
    ),

    Input(
        "admin-user-search",
        "value",
    ),
    Input(
        "admin-refresh-token",
        "data",
    ),
)
def refresh_admin_users(
    search,
    refresh_token,
):
    admin = _current_admin()

    if admin is None:
        return []

    bootstrap = _bootstrap()

    users = (
        bootstrap.user_service
        .get_all()
    )

    query = (
        search or ""
    ).strip().lower()

    if query:
        users = [
            item
            for item in users
            if (
                query
                in (
                    f"{item.first_name} "
                    f"{item.last_name}"
                ).lower()
                or query
                in item.email.lower()
                or query
                in item.role.lower()
            )
        ]

    project_counts = {
        int(item.id): (
            bootstrap.project_controller
            .count_for_user(
                int(item.id)
            )
        )
        for item in users
    }

    from emidaf_studio.pages.admin.layout import (
        _admin_user_rows,
    )

    return _admin_user_rows(
        admin,
        users,
        project_counts,
    )
