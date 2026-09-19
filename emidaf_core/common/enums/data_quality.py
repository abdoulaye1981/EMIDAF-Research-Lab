"""
=========================================================
EMIDAF Framework
Data Quality
=========================================================
"""

from enum import Enum


class DataQuality(str, Enum):

    EXCELLENT = "Excellent"

    VERY_GOOD = "Very Good"

    GOOD = "Good"

    FAIR = "Fair"

    POOR = "Poor"

    CRITICAL = "Critical"
