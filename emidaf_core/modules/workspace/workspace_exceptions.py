"""
=========================================================
EMIDAF Framework
Workspace Exceptions
=========================================================
"""


class WorkspaceError(Exception):
    """
    Exception de base du module Workspace.
    """


class WorkspaceAlreadyExistsError(WorkspaceError):
    """
    Workspace déjà existant.
    """


class WorkspaceNotFoundError(WorkspaceError):
    """
    Workspace introuvable.
    """


class InvalidWorkspaceError(WorkspaceError):
    """
    Workspace invalide.
    """


class WorkspacePermissionError(WorkspaceError):
    """
    Permissions insuffisantes.
    """