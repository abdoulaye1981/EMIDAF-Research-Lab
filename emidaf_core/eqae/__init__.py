"""
EMIDAF Qualitative Analysis Engine - EQAE.
"""

from .engine import EQAEEngine

from .result import (
    CodebookResult,
    CodingAssignmentResult,
    QualitativeCodeResult,
)

from .coding import (
    AssistedCodingManager,
    Codebook,
    CodingSuggestion,
    QualitativeCoder,
)

from .corpus import (
    QualitativeSegment,
)

from .themes import (
    QualitativeTheme,
    ThematicAnalysis,
)

from .quotations import (
    QualitativeQuotation,
    QuotationManager,
)

from .cooccurrence import (
    CodeCooccurrence,
    CooccurrenceAnalyzer,
)


from .memos import (
    AnalyticalMemo,
    MemoManager,
)

from .summary import (
    CodeSummary,
    QualitativeSummaryBuilder,
    ThemeSummary,
)

__all__ = [
    "QualitativeSummaryBuilder",
    "ThemeSummary",
    "CodeSummary",
    "CodingSuggestion",
    "AssistedCodingManager",
    "MemoManager",
    "AnalyticalMemo",
    "EQAEEngine",
    "Codebook",
    "QualitativeCoder",
    "QualitativeSegment",
    "QualitativeTheme",
    "ThematicAnalysis",
    "QualitativeQuotation",
    "QuotationManager",
    "CodeCooccurrence",
    "CooccurrenceAnalyzer",
    "CodebookResult",
    "QualitativeCodeResult",
    "CodingAssignmentResult",
]
