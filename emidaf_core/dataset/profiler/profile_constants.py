"""
=========================================================
EMIDAF Framework v1.0
Profile Constants
---------------------------------------------------------
Constantes utilisées par le moteur de profilage.
=========================================================
"""

from __future__ import annotations

from pathlib import Path


class ProfileConstants:
    """
    Constantes du moteur de profilage.
    """

    VERSION = "1.0.0"

    ENGINE_NAME = "EMIDAF Profiler"

    REPORT_DIRECTORY = "profiles"

    DEFAULT_REPORT_NAME = "profile.json"

    DEFAULT_ENCODING = "utf-8"

    MAX_PREVIEW_ROWS = 20

    MAX_TEXT_PREVIEW = 150

    MAX_CATEGORY_VALUES = 50

    MAX_UNIQUE_DISPLAY = 25

    SAMPLE_SIZE = 10000

    RANDOM_STATE = 42

    CORRELATION_THRESHOLD = 0.80

    HIGH_CORRELATION_THRESHOLD = 0.95

    OUTLIER_ZSCORE = 3.0

    OUTLIER_IQR = 1.5

    MISSING_WARNING = 0.10

    MISSING_CRITICAL = 0.30

    DUPLICATE_WARNING = 0.05

    DUPLICATE_CRITICAL = 0.15

    MEMORY_WARNING_MB = 500

    MEMORY_CRITICAL_MB = 1024

    DEFAULT_DATE_FORMATS = [

        "%Y-%m-%d",

        "%d/%m/%Y",

        "%m/%d/%Y",

        "%d-%m-%Y",

        "%Y/%m/%d",

        "%Y-%m-%d %H:%M:%S",

        "%d/%m/%Y %H:%M:%S",

    ]

    NUMERIC_DTYPES = {

        "int8",

        "int16",

        "int32",

        "int64",

        "float16",

        "float32",

        "float64",

    }

    BOOLEAN_DTYPES = {

        "bool"

    }

    DATETIME_DTYPES = {

        "datetime64[ns]",

        "datetime64"

    }

    TEXT_DTYPES = {

        "object",

        "string"

    }

    EXPORT_FORMATS = [

        "json",

        "html",

        "pdf",

        "markdown"

    ]

    PROFILE_DIRECTORY = Path("profiles")