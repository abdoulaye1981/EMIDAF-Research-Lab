"""
=========================================================
EMIDAF Framework
Workspace Utils
=========================================================
"""

from pathlib import Path

import uuid


def generate_workspace_id() -> str:

    return str(uuid.uuid4())


def workspace_exists(path: Path) -> bool:

    return path.exists()


def normalize_path(path: str) -> Path:

    return Path(path).expanduser().resolve()


def get_workspace_size(path: Path) -> int:

    size = 0

    for file in path.rglob("*"):

        if file.is_file():

            size += file.stat().st_size

    return size