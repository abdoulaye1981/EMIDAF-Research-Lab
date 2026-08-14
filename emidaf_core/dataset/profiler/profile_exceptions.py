"""
=========================================================
EMIDAF Framework v1.0
Profile Exceptions
---------------------------------------------------------
Exceptions du moteur de profilage.
=========================================================
"""

from __future__ import annotations


class ProfileError(Exception):
    """
    Exception de base du module Profiler.
    """

    def __init__(self, message: str = "Profile error"):

        super().__init__(message)


# ==========================================================
# DataFrame
# ==========================================================

class EmptyDatasetError(ProfileError):
    """
    Dataset vide.
    """

    def __init__(self):

        super().__init__(
            "The dataset is empty."
        )


class InvalidDatasetError(ProfileError):
    """
    Dataset invalide.
    """

    def __init__(self, reason: str = ""):

        message = "Invalid dataset."

        if reason:
            message += f" {reason}"

        super().__init__(message)


class InvalidDataFrameError(ProfileError):
    """
    Objet fourni n'est pas un DataFrame.
    """

    def __init__(self):

        super().__init__(
            "The provided object is not a pandas DataFrame."
        )


# ==========================================================
# Colonnes
# ==========================================================

class ColumnNotFoundError(ProfileError):
    """
    Colonne inexistante.
    """

    def __init__(self, column: str):

        super().__init__(
            f"Column '{column}' was not found."
        )


class InvalidColumnTypeError(ProfileError):
    """
    Type de colonne non supporté.
    """

    def __init__(self, column: str):

        super().__init__(
            f"Unsupported column type for '{column}'."
        )


# ==========================================================
# Analyse
# ==========================================================

class AnalyzerError(ProfileError):
    """
    Erreur provenant d'un Analyzer.
    """

    def __init__(
        self,
        analyzer: str,
        message: str
    ):

        super().__init__(
            f"{analyzer}: {message}"
        )


class AnalyzerNotFoundError(ProfileError):
    """
    Analyzer introuvable.
    """

    def __init__(self, analyzer: str):

        super().__init__(
            f"Analyzer '{analyzer}' not found."
        )


class ProfileBuildError(ProfileError):
    """
    Impossible de construire le ProfileResult.
    """

    def __init__(self):

        super().__init__(
            "Unable to build profile result."
        )


# ==========================================================
# Validation
# ==========================================================

class ValidationError(ProfileError):
    """
    Validation impossible.
    """

    def __init__(self, message: str):

        super().__init__(message)


# ==========================================================
# Recommandations
# ==========================================================

class RecommendationError(ProfileError):
    """
    Erreur du moteur de recommandations.
    """

    def __init__(self, message: str):

        super().__init__(message)


# ==========================================================
# Export
# ==========================================================

class ExportError(ProfileError):
    """
    Export impossible.
    """

    def __init__(self, format_name: str):

        super().__init__(
            f"Unable to export profile to '{format_name}'."
        )


# ==========================================================
# Persistance
# ==========================================================

class ProfileRepositoryError(ProfileError):
    """
    Erreur Repository.
    """

    def __init__(self, message: str):

        super().__init__(message)


class ProfileNotFoundError(ProfileError):
    """
    Profil inexistant.
    """

    def __init__(self, profile_id=None):

        if profile_id is None:

            message = "Profile not found."

        else:

            message = f"Profile '{profile_id}' not found."

        super().__init__(message)

class InvalidProfileError(ProfileError):
    """
    Profil invalide.
    """

    def __init__(
        self,
        message: str = "Invalid profile."
    ):

        super().__init__(message)