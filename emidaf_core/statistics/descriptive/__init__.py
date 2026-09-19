"""
=========================================================
EMIDAF Framework
Descriptive Statistics Package
=========================================================

Public API:
    High-level descriptive-statistics services.

Compatibility:
    Atomic statistics remain available through the
    historical wildcard imports and their dedicated
    submodules, but they are not part of the official
    package-level __all__ API.
=========================================================
"""

from ..base.descriptive_statistic import (
    DescriptiveStatistic,
)

# ==========================================================
# HISTORICAL / COMPATIBILITY IMPORTS
# ==========================================================

from .location import *
from .dispersion import *
from .position import *
from .shape import *
from .robust import *
from .weighted import *
from .circular import *
from .multivariate import *
from .profiling import *
from .summary import *
from .interpretation import *
from .report import *
from .frequency import *
from .distribution import *
from .summary_statistics import *

# Previously missing from package namespace
from .central_tendency import (
    CentralTendency,
)

from .validator import (
    StatisticsValidator,
)


# ==========================================================
# OFFICIAL PUBLIC API
# ==========================================================

__all__ = [
    # Core
    "DescriptiveStatistic",
    "StatisticsValidator",

    # Central tendency / location
    "CentralTendency",
    "LocationStatistics",

    # Univariate descriptive families
    "Dispersion",
    "Position",
    "Shape",
    "Robust",
    "Weighted",
    "Circular",

    # Multivariate
    "Multivariate",

    # Frequencies and distributions
    "FrequencyStatistics",
    "DistributionStatistics",

    # Profiling / summaries
    "StatisticalProfiler",
    "Profiling",
    "DescriptiveSummary",
    "Summary",
    "SummaryStatistics",

    # Interpretation / reporting
    "DescriptiveInterpreter",
    "Interpretation",
    "DescriptiveReport",
    "Report",
]
