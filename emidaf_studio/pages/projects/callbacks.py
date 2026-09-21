from dash import Input
from dash import ALL
from dash import Output
from dash import State
from dash import callback
from dash import no_update
from dash import ctx
from flask import session

from database.models.project_model import ProjectModel
from emidaf_core.bootstrap import Bootstrap

from emidaf_studio.components.cards import ProjectCard


def _current_user_id() -> int:
    user_id = session.get("user_id")

    if user_id is None:
        raise PermissionError(
            "Utilisateur non authentifié."
        )

    return int(user_id)


# ==========================================================
# Gestion des projets
# ==========================================================

@callback(

    Output("project-modal", "is_open"),

    Output("project-workspace", "options"),

    Output("projects-container", "children"),

    Output("project-alert", "children"),

    Output("project-alert", "is_open"),

    Input("btn-new-project", "n_clicks"),    Input("btn-create-project", "n_clicks"),
    Input("btn-close-project", "n_clicks"),

    State("project-name", "value"),
    State("project-workspace", "value"),
    State("project-description", "value"),

    prevent_initial_call=True
)
def manage_projects(
    new_clicks,
    create_clicks,
    close_clicks,
    project_name,
    workspace_id,
    project_description
):

    triggered = ctx.triggered_id

    # ======================================================
    # Initialisation du Core
    # ======================================================

    bootstrap = Bootstrap()
    bootstrap.initialize()

    workspace_controller = bootstrap.workspace_controller
    project_controller = bootstrap.project_controller

    # ======================================================
    # NOUVEAU PROJET
    # ======================================================

    if triggered == "btn-new-project":

        workspaces = workspace_controller.get_all()

        options = [
            {
                "label": workspace.name,
                "value": str(workspace.id)
            }
            for workspace in workspaces
        ]

        return (
            True,
            options,
            no_update,
            "",
            False
        )

    # ======================================================
    # ANNULER
    # ======================================================

    if triggered == "btn-close-project":

        return (
            False,
            no_update,
            no_update,
            "",
            False
        )

    # ======================================================
    # CRÉER LE PROJET
    # ======================================================

    if triggered == "btn-create-project":

        # --------------------------------------------------
        # Validation du nom
        # --------------------------------------------------

        if not project_name or not project_name.strip():

            return (
                True,
                no_update,
                no_update,
                "Le nom du projet est obligatoire.",
                True
            )

        # --------------------------------------------------
        # Validation du Workspace
        # --------------------------------------------------

        if not workspace_id:

            return (
                True,
                no_update,
                no_update,
                "Veuillez sélectionner un espace de travail.",
                True
            )

        # --------------------------------------------------
        # Conversion Workspace ID
        # --------------------------------------------------

        try:
            workspace_id = int(workspace_id)

        except (TypeError, ValueError):

            return (
                True,
                no_update,
                no_update,
                "L’espace de travail sélectionné est invalide.",
                True
            )

        # --------------------------------------------------
        # Vérification du Workspace
        # --------------------------------------------------

        if not workspace_controller.exists(workspace_id):

            return (
                True,
                no_update,
                no_update,
                "L’espace de travail sélectionné n’existe pas.",
                True
            )

        # --------------------------------------------------
        # Création du ProjectModel
        # --------------------------------------------------

        project = ProjectModel(
            workspace_id=workspace_id,
            user_id=_current_user_id(),
            name=project_name.strip(),
            description=(project_description or "").strip()
        )

        # --------------------------------------------------
        # Persistance via le Controller
        # --------------------------------------------------

        try:

            project_controller.create(project)

        except Exception as exc:

            return (
                True,
                no_update,
                no_update,
                f"Erreur lors de la création : {exc}",
                True
            )

        # --------------------------------------------------
        # Actualisation de la liste
        # --------------------------------------------------

        projects = project_controller.get_all_for_user(_current_user_id())

        project_cards = [
            ProjectCard.create(project)
            for project in projects
        ]

        # --------------------------------------------------
        # Succès
        # --------------------------------------------------

        return (
            False,
            no_update,
            project_cards,
            "Projet créé avec succès.",
            True
        )

    return (
        no_update,
        no_update,
        no_update,
        no_update,
        no_update
    )

    # ==========================================================
# Sélection d'un projet
# ==========================================================

@callback(
    Output(
        "selected-project",
        "data",
    ),
    Output(
        "selected-project-info",
        "children",
    ),
    Output(
        "url",
        "pathname",
        allow_duplicate=True,
    ),
    Input(
        {
            "type": "select-project",
            "index": ALL,
        },
        "n_clicks",
    ),
    prevent_initial_call=True,
)
def select_project(n_clicks):

    triggered = ctx.triggered_id

    if not triggered:
        return (
            no_update,
            no_update,
            no_update,
        )

    project_id = int(
        triggered["index"]
    )

    bootstrap = Bootstrap()
    bootstrap.initialize()

    project_controller = (
        bootstrap.project_controller
    )

    project = (
        project_controller.get_for_user(
            project_id,
            _current_user_id(),
        )
    )

    if project is None:
        return (
            no_update,
            "Projet introuvable.",
            no_update,
        )

    return (
        project_id,
        (
            f"Projet sélectionné : "
            f"{project.name} "
            f"(ID : {project.id})"
        ),
        f"/projects/{project_id}",
    )


@callback(
    Output("url", "pathname"),
    Input("btn-open-project", "n_clicks"),
    State("selected-project", "data"),
    prevent_initial_call=True
)
def open_project(n_clicks, project_id):

    if not project_id:
        return no_update

    return f"/projects/{project_id}"


# ==========================================================
# Demande de confirmation de suppression
# ==========================================================

@callback(
    Output("delete-project-modal", "is_open"),
    Output("delete-project-message", "children"),
    Output("projects-container", "children", allow_duplicate=True),
    Output("selected-project", "data", allow_duplicate=True),
    Output("project-alert", "children", allow_duplicate=True),
    Output("project-alert", "is_open", allow_duplicate=True),

    Input("btn-delete-project", "n_clicks"),
    Input("btn-cancel-delete-project", "n_clicks"),
    Input("btn-confirm-delete-project", "n_clicks"),

    State("selected-project", "data"),

    prevent_initial_call=True
)

def request_delete_project(
    delete_clicks,
    cancel_clicks,
    confirm_clicks,
    project_id
):

    triggered = ctx.triggered_id

    bootstrap = Bootstrap()
    bootstrap.initialize()

    project_controller = bootstrap.project_controller

    # ======================================================
    # ANNULER
    # ======================================================

    if triggered == "btn-cancel-delete-project":

        return (
            False,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )

    # ======================================================
    # DEMANDER CONFIRMATION
    # ======================================================

    if triggered == "btn-delete-project":

        if not project_id:

            return (
                False,
                "Veuillez d'abord sélectionner un projet.",
                no_update,
                no_update,
                no_update,
                True
            )

        project = project_controller.get_for_user(project_id, _current_user_id())

        if project is None:

            return (
                False,
                "Le projet sélectionné n'existe plus.",
                no_update,
                None,
                no_update,
                True
            )

        return (
            True,
            f"Voulez-vous supprimer le projet « {project.name} » ?",
            no_update,
            no_update,
            no_update,
            no_update
        )

    # ======================================================
    # CONFIRMER LA SUPPRESSION
    # ======================================================

    if triggered == "btn-confirm-delete-project":

        if not project_id:

            return (
                False,
                no_update,
                no_update,
                None,
                "Aucun projet sélectionné.",
                True
            )

        project = project_controller.get_for_user(project_id, _current_user_id())

        if project is None:

            return (
                False,
                no_update,
                no_update,
                None,
                "Le projet n'existe plus.",
                True
            )

        project_name = project.name

        try:

            project_controller.delete_for_user(project_id, _current_user_id())

        except Exception as exc:

            return (
                True,
                f"Erreur lors de la suppression : {exc}",
                no_update,
                project_id,
                no_update,
                True
            )

        # --------------------------------------------------
        # Actualisation de la liste
        # --------------------------------------------------

        projects = project_controller.get_all_for_user(_current_user_id())

        project_cards = [
            ProjectCard.create(project)
            for project in projects
        ]

        return (
            False,
            no_update,
            project_cards,
            None,
            f"Projet « {project_name} » supprimé avec succès.",
            True
        )

    # ======================================================
    # CAS PAR DÉFAUT
    # ======================================================

    return (
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update
    )


# ==========================================================
# Navigation depuis l'espace de travail d'un projet
# ==========================================================

@callback(
    Output(
        "project-detail-inspection-link",
        "href",
    ),
    Output(
        "project-detail-eidpp-link",
        "href",
    ),
    Output(
        "project-detail-elae-link",
        "href",
    ),
    Output(
        "project-detail-ekde-link",
        "href",
    ),
    Output(
        "project-detail-eaie-link",
        "href",
    ),
    Output(
        "project-detail-exaie-link",
        "href",
    ),
    Output(
        "project-detail-edse-link",
        "href",
    ),
    Output(
        "project-detail-reports-link",
        "href",
    ),
    Input(
        "project-detail-dataset-selector",
        "value",
    ),
    State(
        "project-detail-project-id",
        "data",
    ),
)
def update_project_workspace_links(
    dataset_id,
    project_id,
):
    if (
        project_id is None
        or dataset_id is None
    ):
        return (
            "#",
            "#",
            "#",
            "#",
            "#",
            "#",
            "#",
            "#",
        )

    base = (
        f"/projects/{int(project_id)}"
        f"/datasets/{int(dataset_id)}"
    )

    return (
        base,
        base + "/eidpp",
        base + "/elae",
        base + "/ekde",
        base + "/eaie",
        base + "/exaie",
        base + "/edse",
        base + "/reports",
    )
