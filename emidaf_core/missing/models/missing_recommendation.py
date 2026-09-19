from dataclasses import dataclass
@dataclass(slots=True)
class MissingRecommendation:

    severity: str

    message: str

    priority: int
