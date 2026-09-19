from dash import Dash
import dash_bootstrap_components as dbc


# ==========================================================
# APPLICATION DASH
# ==========================================================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY
    ],
    suppress_callback_exceptions=True,
)

app.title = "EMIDAF Research Lab"


# ==========================================================
# LAYOUT
#
# Important :
# l'application Dash est créée AVANT l'import des modules
# contenant des décorateurs @callback.
# ==========================================================

from emidaf_studio.layouts.main_layout import layout  # noqa: E402


# ==========================================================
# CALLBACKS / PAGES
# ==========================================================

import emidaf_studio.pages.projects.callbacks  # noqa: E402,F401

import importlib  # noqa: E402

importlib.import_module(
    "emidaf_studio.pages.import.callbacks"
)

# Inspection contient actuellement également des callbacks
import emidaf_studio.pages.inspection.layout  # noqa: E402,F401

# EIDPP
import emidaf_studio.pages.eidpp.callbacks  # noqa: E402,F401
import emidaf_studio.pages.elae.callbacks  # noqa: E402,F401
import emidaf_studio.pages.ekde.callbacks  # noqa: E402,F401


# ==========================================================
# LAYOUT PRINCIPAL
# ==========================================================

app.layout = layout


# ==========================================================
# EXECUTION
# ==========================================================

if __name__ == "__main__":
    app.run(
        debug=True
    )
