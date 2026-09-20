import base64
import io
from pathlib import Path

import pandas as pd
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html
import dash_bootstrap_components as dbc
from flask import session

from database.models.dataset_model import DatasetModel
from emidaf_core.bootstrap.bootstrap import Bootstrap


# ============================================================
# BOOTSTRAP
# ============================================================

_bootstrap = Bootstrap()
_container = _bootstrap.initialize()

_project_controller = _bootstrap.project_controller
_dataset_controller = _bootstrap.dataset_controller
_workspace_manager = _bootstrap.workspace_manager


def _current_user_id():
    value = session.get("user_id")

    if value is None:
        return None

    return int(value)


# ============================================================
# LECTURE DU DATASET
# ============================================================

@callback(
    Output("upload-status", "children"),
    Output("dataset-preview", "children"),
    Output("uploaded-dataset-data", "data"),
    Output("uploaded-dataset-filename", "data"),
    Output("uploaded-dataset-contents", "data"),
    Output("btn-save-dataset", "disabled"),
    Input("dataset-upload", "contents"),
    Input("dataset-upload", "filename"),
    prevent_initial_call=True
)
def read_uploaded_dataset(contents, filename):

    if not contents or not filename:
        return "", "", None, None, None, True

    try:
        content_type, content_string = contents.split(",", 1)

        decoded = base64.b64decode(content_string)

        extension = filename.lower().rsplit(".", 1)[-1]

        if extension == "csv":

            dataframe = pd.read_csv(
                io.StringIO(
                    decoded.decode("utf-8")
                )
            )

        elif extension in {"xlsx", "xls"}:

            dataframe = pd.read_excel(
                io.BytesIO(decoded)
            )

        else:

            return (
                dbc.Alert(
                    "Format de fichier non supporté.",
                    color="danger"
                ),
                "",
                None,
                None,
                None,
                True
            )

        preview = dataframe.head(10)

        table = dbc.Table.from_dataframe(
            preview,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True
        )

        status = dbc.Alert(
            [
                html.Strong("Fichier chargé : "),
                filename,
                html.Br(),
                f"{dataframe.shape[0]} lignes × "
                f"{dataframe.shape[1]} colonnes"
            ],
            color="success"
        )

        dataframe_json = dataframe.to_json(
            orient="split",
            date_format="iso"
        )

        return (
            status,
            table,
            dataframe_json,
            filename,
            contents,
            False
        )

    except Exception as exc:

        return (
            dbc.Alert(
                f"Erreur lors de la lecture du fichier : {exc}",
                color="danger"
            ),
            "",
            None,
            None,
            None,
            True
        )


# ============================================================
# ENREGISTREMENT DU DATASET
# ============================================================

@callback(
    Output("dataset-save-status", "children"),
    Input("btn-save-dataset", "n_clicks"),
    State("dataset-name", "value"),
    State("uploaded-dataset-data", "data"),
    State("uploaded-dataset-filename", "data"),
    State("uploaded-dataset-contents", "data"),
    State("current-project-id", "data"),
    prevent_initial_call=True
)
def save_dataset(
    n_clicks,
    dataset_name,
    dataframe_json,
    filename,
    contents,
    project_id
):

    if not n_clicks:
        return ""

    # --------------------------------------------------------
    # Vérification des informations
    # --------------------------------------------------------

    if not dataset_name or not dataset_name.strip():

        return dbc.Alert(
            "Veuillez saisir un nom pour le dataset.",
            color="warning"
        )

    if not dataframe_json or not filename or not contents:

        return dbc.Alert(
            "Aucun dataset à enregistrer.",
            color="warning"
        )

    if not project_id:

        return dbc.Alert(
            "Projet introuvable.",
            color="danger"
        )

    try:

        # ----------------------------------------------------
        # Récupération du projet
        # ----------------------------------------------------

        user_id = _current_user_id()

        if user_id is None:
            return dbc.Alert(
                (
                    "Votre session a expiré. "
                    "Veuillez vous reconnecter."
                ),
                color="danger",
            )

        project = _project_controller.get_for_user(
            int(project_id),
            user_id,
        )

        if project is None:

            return dbc.Alert(
                "Projet introuvable ou accès non autorisé.",
                color="danger"
            )

        # ----------------------------------------------------
        # Récupération du DataFrame
        # ----------------------------------------------------

        dataframe = pd.read_json(
            io.StringIO(dataframe_json),
            orient="split"
        )

        rows, columns = dataframe.shape

        # ----------------------------------------------------
        # Détermination du chemin du projet
        # ----------------------------------------------------

        project_path = _workspace_manager.get_project_path(
            project.name
        )

        datasets_path = project_path / "datasets"

        datasets_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # Décodage du fichier original
        # ----------------------------------------------------

        content_type, content_string = contents.split(",", 1)

        decoded = base64.b64decode(content_string)

        # ----------------------------------------------------
        # Nom du fichier stocké
        # ----------------------------------------------------

        original_path = Path(filename)

        extension = original_path.suffix.lower()

        # ----------------------------------------------------
        # Vérification des doublons dans le projet
        # ----------------------------------------------------

        current_project_id = int(project_id)

        normalized_filename = (
            Path(filename)
            .name
            .strip()
            .casefold()
        )

        duplicate = next(
            (
                existing
                for existing
                in _dataset_controller.get_all()
                if (
                    existing.project_id
                    == current_project_id
                    and
                    Path(
                        existing.original_filename
                    )
                    .name
                    .strip()
                    .casefold()
                    == normalized_filename
                )
            ),
            None,
        )

        if duplicate is not None:

            return dbc.Alert(
                [
                    html.Strong(
                        "Importation refusée : "
                    ),
                    (
                        "un jeu de données provenant "
                        "du même fichier existe déjà "
                        "dans ce projet."
                    ),
                    html.Br(),
                    f"Nom existant : {duplicate.name}",
                    html.Br(),
                    (
                        "Fichier : "
                        f"{duplicate.original_filename}"
                    ),
                    html.Br(),
                    f"Identifiant : {duplicate.id}",
                    html.Br(),
                    html.Small(
                        (
                            "Si le fichier correspond à "
                            "une nouvelle version, utilisez "
                            "un nom de fichier différent."
                        )
                    ),
                ],
                color="warning",
            )

        stored_filename = filename

        destination = datasets_path / stored_filename

        # ----------------------------------------------------
        # Éviter d'écraser un fichier existant
        # ----------------------------------------------------

        if destination.exists():

            stem = original_path.stem
            suffix = original_path.suffix

            counter = 1

            while destination.exists():

                stored_filename = (
                    f"{stem}_{counter}{suffix}"
                )

                destination = (
                    datasets_path / stored_filename
                )

                counter += 1

        # ----------------------------------------------------
        # Écriture du fichier original
        # ----------------------------------------------------

        with open(destination, "wb") as file:

            file.write(decoded)

        # ----------------------------------------------------
        # Détermination du séparateur
        # ----------------------------------------------------

        separator = ","

        if extension == ".csv":

            try:

                sample = decoded[:100000].decode(
                    "utf-8"
                )

                separators = [",", ";", "\t", "|"]

                separator = max(
                    separators,
                    key=sample.count
                )

            except Exception:

                separator = ","

        # ----------------------------------------------------
        # Création du DatasetModel
        # ----------------------------------------------------

        dataset = DatasetModel(
            project_id=int(project_id),
            name=dataset_name.strip(),
            original_filename=filename,
            stored_filename=stored_filename,
            extension=extension,
            separator=separator,
            encoding="utf-8",
            rows=int(rows),
            columns=int(columns),
            size=len(decoded)
        )

        # ----------------------------------------------------
        # Enregistrement en base
        # ----------------------------------------------------

        saved_dataset = _dataset_controller.create(
            dataset
        )

        # ----------------------------------------------------
        # Message de succès
        # ----------------------------------------------------

        return dbc.Alert(
            [
                html.Strong(
                    "Jeu de données enregistré avec succès."
                ),
                html.Br(),
                f"Nom : {saved_dataset.name}",
                html.Br(),
                f"Fichier : {stored_filename}",
                html.Br(),
                f"Dimensions : {rows} lignes × {columns} colonnes",
                html.Br(),
                f"Taille : {len(decoded)} octets"
            ],
            color="success"
        )

    except Exception as exc:

        return dbc.Alert(
            [
                html.Strong(
                    "Erreur lors de l'enregistrement : "
                ),
                str(exc)
            ],
            color="danger"
        )
