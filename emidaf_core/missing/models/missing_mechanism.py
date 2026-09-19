from dataclasses import dataclass
@dataclass(slots=True)
class MissingMechanism:

    name: str

    detected: bool

    confidence: float

    pvalue: float | None

    statistic: float | None

    test_name: str

    explanation: str
