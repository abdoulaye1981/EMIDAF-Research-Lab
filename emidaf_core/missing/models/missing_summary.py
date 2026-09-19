from dataclasses import dataclass
@dataclass(slots=True)
class MissingSummary:

    rows: int

    columns: int

    cells: int

    total_missing: int

    missing_rate: float

    completeness_score: float

    quality_score: float

    quality_level: str
