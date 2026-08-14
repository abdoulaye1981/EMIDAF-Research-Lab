@dataclass(slots=True)
class MissingResult:

    summary: MissingSummary

    statistics: MissingStatistics

    mechanism: MissingMechanism

    strategy: MissingStrategy

    patterns: list[MissingPattern]

    recommendations: list[MissingRecommendation]

    warnings: list[str]

    errors: list[str]

    execution_time: float

    score: float