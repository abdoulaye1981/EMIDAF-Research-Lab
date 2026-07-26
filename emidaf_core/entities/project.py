from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Project:
    name: str
    description: str
    author: str
    workspace: str

    id: int | None = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)