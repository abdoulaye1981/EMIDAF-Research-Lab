from dash import html
import dash_bootstrap_components as dbc

from emidaf_studio.components.navbar import navbar
from emidaf_studio.components.sidebar import sidebar
from emidaf_studio.router import layout as router_layout


layout = html.Div(
    [
        navbar,

        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            sidebar,
                            width=2
                        ),

                        dbc.Col(
                            router_layout,
                            width=10
                        ),
                    ]
                )
            ],
            fluid=True,
        ),
    ]
)
