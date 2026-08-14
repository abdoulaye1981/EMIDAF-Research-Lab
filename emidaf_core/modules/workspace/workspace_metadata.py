"""
=========================================================
Workspace Metadata
=========================================================
"""

from dataclasses import dataclass

from datetime import datetime


@dataclass(slots=True)
class WorkspaceMetadata:

    workspace_id: str

    name: str

    version: str

    author: str

    description: str

    created_at: datetime

    last_opened: datetime