from dash import html
import dash_bootstrap_components as dbc

from emidaf_studio.components.navbar import navbar
from emidaf_studio.components.sidebar import sidebar
from emidaf_studio.layouts.home import layout as home

layout = html.Div(
    [
        navbar,

        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(sidebar, width=2),
                        dbc.Col(home, width=10),
                    ]
                )
            ],
            fluid=True,
        ),
    ]
)