from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        html.H2("Bienvenue dans EMIDAF Research Lab"),
        html.Hr(),
        html.P(
            "Plateforme intégrée pour le Learning Analytics, "
            "l'Educational Data Mining, le Machine Learning et "
            "l'Explainable AI."
        ),
    ],
    fluid=True,
)