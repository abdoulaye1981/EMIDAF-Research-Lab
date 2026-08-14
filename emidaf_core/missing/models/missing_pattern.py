@dataclass(slots=True)
class MissingPattern:

    pattern: list[int]

    count: int

    percentage: float