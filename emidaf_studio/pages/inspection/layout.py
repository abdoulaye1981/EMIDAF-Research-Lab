from pathlib import Path

import pandas as pd
from dash import html, dcc, Input, Output, State, callback, no_update
import re
import dash_bootstrap_components as dbc

from emidaf_core.bootstrap import Bootstrap
from emidaf_core.dataset.profiler import DatasetProfiler


bootstrap = Bootstrap()
bootstrap.initialize()

project_controller = bootstrap.project_controller
dataset_controller = bootstrap.dataset_controller
workspace_manager = bootstrap.workspace_manager


def load_dataset(project_id, dataset_id):
    project = project_controller.get(project_id)

    if project is None:
        return None, None, "Projet introuvable."

    dataset = dataset_controller.get(dataset_id)

    if dataset is None:
        return project, None, "Dataset introuvable."

    if dataset.project_id != project_id:
        return project, None, "Le dataset n'est pas associé à ce projet."

    project_path = workspace_manager.get_project_path(project.name)
    dataset_path = project_path / "datasets" / dataset.stored_filename

    if not dataset_path.exists():
        return project, dataset, (
            "Le fichier physique du dataset est introuvable : "
            f"{dataset_path}"
        )

    try:
        extension = dataset.extension.lower()

        if extension == ".csv":
            dataframe = pd.read_csv(
                dataset_path,
                sep=dataset.separator,
                encoding=dataset.encoding
            )

        elif extension in {".xlsx", ".xls"}:
            dataframe = pd.read_excel(dataset_path)

        else:
            return project, dataset, (
                "Format de fichier non supporté : "
                f"{dataset.extension}"
            )

        return project, dataset, dataframe

    except Exception as exc:
        return project, dataset, (
            f"Erreur lors de la lecture du dataset : {exc}"
        )


def build_profile_summary(profile):
    summary = profile.summary

    return dbc.Container(
        [
            html.H4(
                "📊 Résumé du profil",
                className="mt-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Lignes"),
                                    html.H4(f"{summary.rows:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes"),
                                    html.H4(f"{summary.columns:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Cellules"),
                                    html.H4(f"{summary.cells:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Score global"),
                                    html.H4(
                                        f"{summary.overall_score:.1f}/100"
                                    )
                                ]
                            )
                        ),
                        width=3
                    )
                ],
                className="mb-3"
            ),

            dbc.Alert(
                [
                    html.Strong("Statut du profil : "),
                    summary.profile_status
                ],
                color="success"
            ),

            html.H5(
                "🔢 Types de variables",
                className="mt-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Numériques"),
                                    html.H4(summary.numeric_columns)
                                ]
                            )
                        ),
                        width=2
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Catégorielles"),
                                    html.H4(summary.categorical_columns)
                                ]
                            )
                        ),
                        width=2
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Datetimes"),
                                    html.H4(summary.datetime_columns)
                                ]
                            )
                        ),
                        width=2
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Booléennes"),
                                    html.H4(summary.boolean_columns)
                                ]
                            )
                        ),
                        width=2
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Texte"),
                                    html.H4(summary.text_columns)
                                ]
                            )
                        ),
                        width=2
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Inconnues"),
                                    html.H4(summary.unknown_columns)
                                ]
                            )
                        ),
                        width=2
                    )
                ],
                className="mb-3"
            ),

            html.H5(
                "🧹 Qualité des données",
                className="mt-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Valeurs manquantes"),
                                    html.H4(
                                        f"{summary.missing_values:,}"
                                    ),
                                    html.P(
                                        f"{summary.missing_percentage:.2f} %"
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Doublons"),
                                    html.H4(
                                        f"{summary.duplicate_rows:,}"
                                    ),
                                    html.P(
                                        f"{summary.duplicate_percentage:.2f} %"
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes constantes"),
                                    html.H4(
                                        summary.constant_columns
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes vides"),
                                    html.H4(
                                        summary.empty_columns
                                    )
                                ]
                            )
                        ),
                        width=3
                    )
                ],
                className="mb-3"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Score de qualité"),
                                    html.H4(
                                        f"{summary.quality_score:.1f}/100"
                                    )
                                ]
                            )
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Score de complétude"),
                                    html.H4(
                                        f"{summary.completeness_score:.1f}/100"
                                    )
                                ]
                            )
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Niveau de qualité"),
                                    html.H4(
                                        summary.quality_level
                                    )
                                ]
                            )
                        ),
                        width=4
                    )
                ],
                className="mb-3"
            )
        ],
        fluid=True
    )


def inspection_layout(project_id, dataset_id):

    project, dataset, result = load_dataset(
        project_id,
        dataset_id
    )

    if isinstance(result, str):
        return dbc.Container(
            [
                html.H2("🔎 Inspection du dataset"),
                html.Hr(),

                dbc.Alert(
                    result,
                    color="danger"
                ),

                dcc.Link(
                    dbc.Button(
                        "← Retour au projet",
                        color="secondary"
                    ),
                    href=f"/projects/{project_id}"
                )
            ],
            fluid=True
        )

    dataframe = result

    rows, columns = dataframe.shape
    size_kb = dataset.size / 1024

    format_name = {
        ".csv": "CSV",
        ".xlsx": "Excel",
        ".xls": "Excel"
    }.get(
        dataset.extension.lower(),
        dataset.extension.upper()
    )

    preview = dataframe.head(10)

    preview_table = dbc.Table.from_dataframe(
        preview,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True
    )

    # Profilage automatique du dataset
    profile_summary = html.Div(
        [
            html.P(
                "Cliquez sur « Profiler le dataset » pour lancer "
                "l'analyse complète.",
                className="text-muted"
            )
        ]
    )
    return dbc.Container(
        [
            html.H2("🔎 Inspection du dataset"),
            html.Hr(),

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects"
                    },
                    {
                        "label": project.name,
                        "href": f"/projects/{project_id}"
                    },
                    {
                        "label": dataset.name,
                        "active": True
                    }
                ]
            ),

            html.H4(
                "📋 Informations générales",
                className="mt-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Nom du dataset"),
                                    html.H5(dataset.name)
                                ]
                            )
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Fichier"),
                                    html.H5(
                                        dataset.original_filename
                                    )
                                ]
                            )
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Format"),
                                    html.H5(format_name)
                                ]
                            )
                        ),
                        width=4
                    )
                ],
                className="mb-3"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Lignes"),
                                    html.H4(f"{rows:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes"),
                                    html.H4(f"{columns:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Taille"),
                                    html.H4(
                                        f"{size_kb:.2f} Ko"
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Cellules"),
                                    html.H4(
                                        f"{rows * columns:,}"
                                    )
                                ]
                            )
                        ),
                        width=3
                    )
                ],
                className="mb-4"
            ),

            # ---------------------------------------------------------
            # Profilage du dataset
            # ---------------------------------------------------------
            dbc.Card(
              [
                dbc.CardHeader("Profilage du dataset"),
                dbc.CardBody(
                  [
                      dbc.Button(
                         "Profiler le dataset",
                         id="btn-profile-dataset",
                         color="primary",
                         className="mb-3",
                      ),
                      html.Div(
                         profile_summary,
                         id="profile-result",
                      ),
                  ]
                ),
              ],
              className="mb-4",
            ),
            html.H4(
                "👁️ Aperçu des données",
                className="mt-4"
            ),

            dbc.Alert(
                "Affichage des 10 premières lignes.",
                color="info"
            ),

            preview_table,

            html.Hr(),

            dcc.Link(
                dbc.Button(
                    "← Retour au projet",
                    color="secondary"
                ),
                href=f"/projects/{project_id}"
            ),

            dcc.Store(
                id="inspection-project-id",
                data=project_id,
            ),
            dcc.Store(
                id="inspection-dataset-id",
                data=dataset_id,
            ),
        ],
        fluid=True
    )

@callback(
    Output("profile-result", "children"),
    Input("btn-profile-dataset", "n_clicks"),
    State("inspection-project-id", "data"),
    State("inspection-dataset-id", "data"),
    prevent_initial_call=True,
)
def run_dataset_profile(n_clicks, project_id, dataset_id):
    """Lance le profilage complet du dataset à la demande."""

    if not n_clicks:
        return no_update

    project, dataset, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        return dbc.Alert(
            result,
            color="danger",
            className="mt-3",
        )

    try:
        profiler = DatasetProfiler()
        profile = profiler.profile(result)

        return build_profile_summary(profile)

    except Exception as exc:
        return dbc.Alert(
            [
                html.Strong("Erreur lors du profilage : "),
                html.Span(str(exc)),
            ],
            color="danger",
            className="mt-3",
        )
