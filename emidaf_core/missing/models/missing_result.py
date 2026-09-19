from dataclasses import dataclass

from emidaf_core.missing.models.missing_summary import MissingSummary
from emidaf_core.missing.models.missing_statistics import MissingStatistics
from emidaf_core.missing.models.missing_mechanism import MissingMechanism
from emidaf_core.missing.models.missing_strategy import MissingStrategy
from emidaf_core.missing.models.missing_pattern import MissingPattern
from emidaf_core.missing.models.missing_recommendation import MissingRecommendation


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
