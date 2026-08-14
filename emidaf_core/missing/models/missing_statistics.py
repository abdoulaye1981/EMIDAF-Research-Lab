@dataclass(slots=True)
class MissingStatistics:

    complete_rows: int

    rows_with_missing: int

    empty_rows: int

    complete_columns: int

    partial_columns: int

    empty_columns: int

    missing_density: float

    pattern_count: int