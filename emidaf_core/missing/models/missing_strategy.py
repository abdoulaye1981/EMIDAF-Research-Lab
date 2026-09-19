from dataclasses import dataclass
@dataclass(slots=True)
class MissingStrategy:

    strategy: str

    confidence: float

    applicable: bool

    reason: str
