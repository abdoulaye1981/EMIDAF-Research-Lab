from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import importlib
import os
import secrets

from dash import Dash
from flask import redirect
from flask import session

import dash_bootstrap_components as dbc


# ==========================================================
# ENVIRONNEMENT
# ==========================================================

EMIDAF_ENV = (
    os.environ.get(
        "EMIDAF_ENV",
        "development",
    )
    .strip()
    .lower()
)

IS_PRODUCTION = (
    EMIDAF_ENV == "production"
)

DEBUG_REQUESTED = (
    os.environ.get(
        "EMIDAF_DEBUG",
        "0",
    )
    .strip()
    .lower()
    in {
        "1",
        "true",
        "yes",
        "on",
    }
)

# Le mode debug est interdit en production.
DEBUG = (
    DEBUG_REQUESTED
    and not IS_PRODUCTION
)


# ==========================================================
# SECRET DE SESSION
# ==========================================================

secret_key = os.environ.get(
    "EMIDAF_SECRET_KEY"
)

if IS_PRODUCTION:
    if not secret_key:
        raise RuntimeError(
            "EMIDAF_SECRET_KEY est obligatoire "
            "en environnement de production."
        )

    if len(secret_key) < 32:
        raise RuntimeError(
            "EMIDAF_SECRET_KEY doit contenir "
            "au moins 32 caractères en production."
        )

elif not secret_key:
    # Développement local uniquement.
    #
    # La clé est générée en mémoire et change
    # au redémarrage de l'application.
    secret_key = secrets.token_hex(32)


# ==========================================================
# APPLICATION DASH
# ==========================================================

ASSETS_FOLDER = (
    Path(__file__).resolve().parent
    / "assets"
)


app = Dash(
    __name__,
    assets_folder=str(ASSETS_FOLDER),
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.BOOTSTRAP,
    ],
    suppress_callback_exceptions=True,
)

app.title = "EMIDAF Research Lab"

server = app.server


# ==========================================================
# CONFIGURATION FLASK / SESSION
# ==========================================================

server.config.update(
    SECRET_KEY=secret_key,

    SESSION_COOKIE_NAME="emidaf_session",

    SESSION_COOKIE_HTTPONLY=True,

    SESSION_COOKIE_SAMESITE="Lax",

    # HTTPS obligatoire en production.
    SESSION_COOKIE_SECURE=IS_PRODUCTION,

    PERMANENT_SESSION_LIFETIME=timedelta(
        hours=8
    ),
)


# ==========================================================
# DÉCONNEXION
# ==========================================================

@server.route("/logout")
def logout():
    session.clear()

    return redirect("/login")


# ==========================================================
# LAYOUT
#
# L'application Dash est créée AVANT l'import des modules
# contenant les décorateurs @callback.
# ==========================================================

from emidaf_studio.layouts.main_layout import (  # noqa: E402
    layout,
)


# ==========================================================
# CALLBACKS / PAGES
# ==========================================================

import emidaf_studio.pages.projects.callbacks  # noqa: E402,F401

importlib.import_module(
    "emidaf_studio.pages.import.callbacks"
)

# Inspection contient actuellement également des callbacks.
import emidaf_studio.pages.inspection.layout  # noqa: E402,F401

# Modules scientifiques.
import emidaf_studio.pages.eidpp.callbacks  # noqa: E402,F401
import emidaf_studio.pages.elae.callbacks  # noqa: E402,F401
import emidaf_studio.pages.ekde.callbacks  # noqa: E402,F401
import emidaf_studio.pages.eaie.callbacks  # noqa: E402,F401
import emidaf_studio.pages.exaie.callbacks  # noqa: E402,F401
import emidaf_studio.pages.edse.callbacks  # noqa: E402,F401
import emidaf_studio.pages.reports.callbacks  # noqa: E402,F401

# Composants.
import emidaf_studio.components.theme  # noqa: E402,F401
import emidaf_studio.components.user_menu  # noqa: E402,F401

# Authentification / administration / compte.
import emidaf_studio.pages.auth.callbacks  # noqa: E402,F401
import emidaf_studio.pages.admin.callbacks  # noqa: E402,F401
import emidaf_studio.pages.account.callbacks  # noqa: E402,F401


# ==========================================================
# LAYOUT PRINCIPAL
# ==========================================================

app.layout = layout


# ==========================================================
# EXÉCUTION LOCALE
# ==========================================================

if __name__ == "__main__":
    host = os.environ.get(
        "EMIDAF_HOST",
        "127.0.0.1",
    )

    port = int(
        os.environ.get(
            "EMIDAF_PORT",
            "8050",
        )
    )

    app.run(
        host=host,
        port=port,
        debug=DEBUG,
    )
