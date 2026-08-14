"""
=========================================================
EMIDAF Framework
Correlation Package
=========================================================
"""

from .linear import *
from .categorical import *
from .mixed import *
from .association import *
from .matrix import *
from .multicollinearity import *

__all__ = [
    "Pearson",
    "Spearman",
    "Kendall",

    "PointBiserial",

    "CramerV",
    "PhiCoefficient",

    "EtaSquared",
    "CorrelationRatio",

    "CorrelationMatrix",

    "VarianceInflationFactor",
    "MulticollinearityAnalyzer",
]