from dash import Dash
import dash_bootstrap_components as dbc

from emidaf_studio.layouts.main_layout import layout

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
)

app.title = "EMIDAF Research Lab"

app.layout = layout