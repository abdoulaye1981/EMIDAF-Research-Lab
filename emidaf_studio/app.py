from dash import Dash
import dash_bootstrap_components as dbc

from emidaf_studio.layouts.main_layout import layout

import emidaf_studio.pages.projects.callbacks
import importlib

importlib.import_module(
    "emidaf_studio.pages.import.callbacks"
)
import emidaf_studio.pages.inspection.layout
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

app.title = "EMIDAF Research Lab"
app.layout = layout


if __name__ == "__main__":
    app.run(
        debug=True
    )
