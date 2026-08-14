from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Dataset:

    id: Optional[int] = None

    project_id: Optional[int] = None

    name: str = ""

    original_filename: str = ""

    stored_filename: str = ""

    extension: str = ""

    separator: str = ","

    encoding: str = "utf-8"

    rows: int = 0

    columns: int = 0

    size: int = 0

    created_at: datetime = datetime.now()