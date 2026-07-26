from pathlib import Path


class ProjectValidator:

    @staticmethod
    def validate_name(name: str):

        if not name.strip():
            raise ValueError("Le nom du projet est obligatoire.")

        if len(name) < 3:
            raise ValueError(
                "Le nom doit contenir au moins 3 caractères."
            )

    @staticmethod
    def validate_workspace(path: str):

        if not Path(path).exists():
            raise ValueError(
                "Le dossier Workspace est introuvable."
            )