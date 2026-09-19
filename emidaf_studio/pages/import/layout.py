from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def import_layout(project_id):
    return dbc.Container(
        [
            html.H2("📥 Importation des datasets"),
            html.Hr(),

            dbc.Alert(
                f"Projet sélectionné : {project_id}",
                color="primary"
            ),

            html.H4("Sélectionner un fichier"),

            dcc.Upload(
                id="dataset-upload",
                children=dbc.Button(
                    "📂 Choisir un fichier",
                    color="primary"
                ),
                multiple=False
            ),

            html.Br(),

            html.P(
                "Formats acceptés : CSV (.csv) et Excel (.xlsx, .xls).",
                className="text-muted"
            ),

            html.Div(
                id="upload-status",
                className="mt-3"
            ),

            html.Div(
                id="dataset-preview",
                className="mt-4"
            ),

            html.Hr(),

            html.H4("Informations du dataset"),

            dbc.Label("Nom du dataset"),
            dbc.Input(
                id="dataset-name",
                type="text",
                placeholder="Exemple : Données étudiants",
                className="mb-3"
            ),

            dbc.Button(
                " Enregistrer le dataset",
                id="btn-save-dataset",
                color="success",
                disabled=True
            ),

            html.Div(
                id="dataset-save-status",
                className="mt-3"
            ),

            dcc.Store(
                id="uploaded-dataset-data"
            ),

            dcc.Store(
                id="uploaded-dataset-filename"
            ),
            dcc.Store(
                id="uploaded-dataset-contents"
            ),
            dcc.Store(id="current-project-id",data=project_id
            ),
        ],
        fluid=True
    )
