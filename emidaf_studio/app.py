from dash import Dash
from dash import html

import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY]
)

app.layout = dbc.Container(

    [

        html.H1(
            "EMIDAF Research Lab",
            className="text-center mt-5"
        ),

        html.Hr(),

        html.H3(
            "Educational Multidimensional Intelligent Decision Analytics Framework",
            className="text-center"
        ),

        html.Br(),

        dbc.Button(
            "Nouveau Projet",
            color="primary",
            size="lg"
        )

    ],

    fluid=True

)

if __name__ == "__main__":
    app.run(debug=True)