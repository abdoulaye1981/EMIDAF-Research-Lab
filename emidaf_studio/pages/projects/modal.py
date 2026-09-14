from dash import html
import dash_bootstrap_components as dbc


def project_modal():

    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "Nouveau Projet"
                )
            ),

            dbc.ModalBody(
                [
                    dbc.Label(
                        "Nom du projet"
                    ),

                    dbc.Input(
                        id="project-name",
                        placeholder="Nom du projet",
                        type="text"
                    ),

                    html.Br(),

                    dbc.Label(
                        "Workspace"
                    ),

                    dbc.Select(
                        id="project-workspace",
                        options=[],
                        placeholder="Sélectionner un workspace"
                    ),

                    html.Br(),

                    dbc.Label(
                        "Description"
                    ),

                    dbc.Textarea(
                        id="project-description",
                        placeholder="Description du projet"
                    )
                ]
            ),

            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Créer",
                        id="btn-create-project",
                        color="primary"
                    ),

                    dbc.Button(
                        "Annuler",
                        id="btn-close-project",
                        color="secondary"
                    )
                ]
            )
        ],

        id="project-modal",
        size="lg",
        centered=True,
        backdrop="static",
        is_open=False
    )

# ==========================================================
# Modale de confirmation de suppression
# ==========================================================

def delete_project_modal():

    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "Confirmer la suppression"
                )
            ),

            dbc.ModalBody(
                [
                    html.P(
                        id="delete-project-message"
                    )
                ]
            ),

            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Annuler",
                        id="btn-cancel-delete-project",
                        color="secondary"
                    ),

                    dbc.Button(
                        "Supprimer",
                        id="btn-confirm-delete-project",
                        color="danger"
                    )
                ]
            )
        ],

        id="delete-project-modal",
        centered=True,
        backdrop="static",
        is_open=False
    )
