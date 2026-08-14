"""
=========================================================
EMIDAF Framework
Configuration
=========================================================

Configuration globale du framework.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field


# =========================================================
# ANALYSIS
# =========================================================

@dataclass(slots=True)
class AnalysisConfiguration:

    enable_parallel: bool = False

    max_workers: int = 1

    random_state: int = 42

    verbose: bool = True


# =========================================================
# STATISTICS
# =========================================================

@dataclass(slots=True)
class StatisticsConfiguration:

    alpha: float = 0.05

    confidence_level: float = 0.95

    decimal_places: int = 4


# =========================================================
# CACHE
# =========================================================

@dataclass(slots=True)
class CacheConfiguration:

    enabled: bool = True

    max_size: int = 512

    clear_after_execution: bool = False


# =========================================================
# REPORT
# =========================================================

@dataclass(slots=True)
class ReportingConfiguration:

    export_html: bool = True

    export_pdf: bool = False

    export_excel: bool = False

    export_json: bool = False

    export_markdown: bool = False


# =========================================================
# LOGGING
# =========================================================

@dataclass(slots=True)
class LoggingConfiguration:

    enabled: bool = True

    level: str = "INFO"


# =========================================================
# ROOT
# =========================================================

@dataclass(slots=True)
class Configuration:

    analysis: AnalysisConfiguration = field(

        default_factory=AnalysisConfiguration

    )

    statistics: StatisticsConfiguration = field(

        default_factory=StatisticsConfiguration

    )

    cache: CacheConfiguration = field(

        default_factory=CacheConfiguration

    )

    reporting: ReportingConfiguration = field(

        default_factory=ReportingConfiguration

    )

    logging: LoggingConfiguration = field(

        default_factory=LoggingConfiguration
    )