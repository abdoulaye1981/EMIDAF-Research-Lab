from dash import Dash
import dash_bootstrap_components as dbc

from emidaf_studio.layouts.main_layout import layout

import emidaf_studio.pages.projects.callbacks


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
