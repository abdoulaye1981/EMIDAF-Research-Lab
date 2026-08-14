"""
=========================================================
EMIDAF Framework
Descriptive Statistics Package
=========================================================
"""

from .base import (
    BaseStatistic,
    StatisticResult
)

from .central_tendency import *
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

__all__ = [

    "BaseStatistic",

    "StatisticResult",

    "CentralTendency",

    "Dispersion",

    "Position",

    "Shape",

    "Robust",

    "Weighted",

    "Circular",

    "Multivariate",

    "Profiling",

    "Summary",

    "Interpretation",

    "Report"

]