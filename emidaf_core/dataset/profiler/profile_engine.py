"""
=========================================================
EMIDAF Framework v1.0
Profile Engine
---------------------------------------------------------
Moteur principal du Dataset Profiler.
=========================================================
"""

from __future__ import annotations

import pandas as pd

from emidaf_core.core.base_engine import BaseEngine

from .profile_builder import ProfileBuilder
from .profile_context import ProfileContext
from .profile_metadata import ProfileMetadata
from .profile_result import ProfileResult
from .profile_summary import ProfileSummary
from .registry.analyzer_registry import AnalyzerRegistry


class ProfileEngine(BaseEngine):
    """
    Moteur principal du Dataset Profiler.

    Il orchestre entièrement le processus :

        DataFrame
            ↓
        ProfileContext
            ↓
        AnalyzerRegistry
            ↓
        AnalyzerResults
            ↓
        ProfileBuilder
            ↓
        ProfileResult
    """

    def __init__(
        self,
        registry: AnalyzerRegistry,
        builder: ProfileBuilder,
    ) -> None:

        self.registry = registry

        self.builder = builder

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        if dataframe is None:

            raise ValueError(

                "dataframe cannot be None."

            )

        if not isinstance(dataframe, pd.DataFrame):

            raise TypeError(

                "dataframe must be a pandas.DataFrame."

            )

        if dataframe.empty:

            raise ValueError(

                "dataframe is empty."

            )

    # =====================================================
    # CONTEXT
    # =====================================================

    def create_context(
        self,
        dataframe: pd.DataFrame,
    ) -> ProfileContext:

        return ProfileContext(

            dataframe

        )

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(
        self,
        context: ProfileContext,
    ) -> ProfileResult:

        analyzer_results = []

        for analyzer in self.registry:

            result = analyzer.execute(

                context

            )

            analyzer_results.append(

                result

            )

            context.analyzer_executed(

                analyzer.name

            )

        metadata = ProfileMetadata()

        summary = ProfileSummary()

        summary.rows = context.rows

        summary.columns = context.columns

        summary.cells = (

            context.rows *

            context.columns

        )

        return self.builder.build(

            analyzer_results=analyzer_results,

            metadata=metadata,

            summary=summary,

        )

    # =====================================================
    # FINALIZATION
    # =====================================================

    def finalize(
        self,
        context: ProfileContext,
        result: ProfileResult,
    ) -> None:

        result.metadata.execution_time = (

            result.execution_time

        )

        result.metadata.success = (

            result.is_valid

        )

        context.logger.info(

            "Profile completed successfully."

        )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(analyzers={len(self.registry)})"

        )