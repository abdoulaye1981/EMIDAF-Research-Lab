from dash import (
    dcc,
    html,
)

import dash_bootstrap_components as dbc

from emidaf_studio.components.navbar import navbar
from emidaf_studio.components.sidebar import sidebar
from emidaf_studio.router import layout as router_layout


layout = html.Div(
    [
        dcc.Store(
            id="theme-preference",
            storage_type="local",
            data="scientific",
        ),

        navbar,

        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            sidebar,
                            id="emidaf-sidebar-column",
                            xs=12,
                            sm=12,
                            md=3,
                            lg=2,
                            xl=2,
                            className="px-0",
                        ),

                        dbc.Col(
                            router_layout,
                            id="emidaf-main-content",
                            xs=12,
                            sm=12,
                            md=9,
                            lg=10,
                            xl=10,
                            className="px-4 py-4",
                        ),
                    ],
                    className="g-0",
                    style={
                        "minHeight": "calc(100vh - 56px)",
                    },
                )
            ],
            fluid=True,
            className="px-0",
        ),
    ],
    id="emidaf-app-shell",
)
