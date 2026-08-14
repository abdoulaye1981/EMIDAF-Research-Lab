"""
=========================================================
EMIDAF Framework v1.0
Dataset Profiler
---------------------------------------------------------
Moteur principal de profilage.
=========================================================
"""

from __future__ import annotations

from time import perf_counter
from typing import Optional

import pandas as pd

from .profile_result import ProfileResult
from .profile_metadata import ProfileMetadata
from .profile_summary import ProfileSummary
from .profile_validator import ProfileValidator

from .analyzers.analyzer_registry import AnalyzerRegistry
from .analyzers.analyzer_result import AnalyzerResult

from .analyzers.structure_analyzer import StructureAnalyzer
from .analyzers.datatype_analyzer import DatatypeAnalyzer
from .analyzers.memory_analyzer import MemoryAnalyzer
from .analyzers.quality_analyzer import QualityAnalyzer
from .analyzers.missing_analyzer import MissingAnalyzer
from .analyzers.duplicate_analyzer import DuplicateAnalyzer
from .analyzers.cardinality_analyzer import CardinalityAnalyzer
from .analyzers.uniqueness_analyzer import UniquenessAnalyzer
from .analyzers.consistency_analyzer import ConsistencyAnalyzer
from .analyzers.numerical_analyzer import NumericalAnalyzer
from .analyzers.categorical_analyzer import CategoricalAnalyzer
from .analyzers.datetime_analyzer import DatetimeAnalyzer
from .analyzers.text_analyzer import TextAnalyzer
from .analyzers.distribution_analyzer import DistributionAnalyzer
from .analyzers.normality_analyzer import NormalityAnalyzer
from .analyzers.outlier_analyzer import OutlierAnalyzer
from .analyzers.correlation_analyzer import CorrelationAnalyzer
from .analyzers.multicollinearity_analyzer import (
    MulticollinearityAnalyzer,
)
from .profile_factory import ProfileFactory
from .profile_builder import ProfileBuilder
from .profile_context import ProfileContext


class DatasetProfiler:
    """
    Profiler principal du framework EMIDAF.
    """

    def __init__(self):

        self.validator = ProfileValidator()

        self.factory = ProfileFactory()

        self.registry = AnalyzerRegistry()

        self.builder = ProfileBuilder()

        self._register_default_analyzers()

    # =====================================================
    # REGISTRY
    # =====================================================

    def _register_default_analyzers(self):

        self.registry.register(
            StructureAnalyzer()
        )

        self.registry.register(
            DatatypeAnalyzer()
        )

        self.registry.register(
            MemoryAnalyzer()
        )

        self.registry.register(
            QualityAnalyzer()
        )

        self.registry.register(
            MissingAnalyzer()
        )

        self.registry.register(
            DuplicateAnalyzer()
        )

        self.registry.register(
            CardinalityAnalyzer()
        )

        self.registry.register(
            UniquenessAnalyzer()
        )

        self.registry.register(
            ConsistencyAnalyzer()
        )

        self.registry.register(
            NumericalAnalyzer()
        )

        self.registry.register(
            CategoricalAnalyzer()
        )

        self.registry.register(
            DatetimeAnalyzer()
        )

        self.registry.register(
            TextAnalyzer()
        )

        self.registry.register(
            DistributionAnalyzer()
        )

        self.registry.register(
            NormalityAnalyzer()
        )

        self.registry.register(
            OutlierAnalyzer()
        )

        self.registry.register(
            CorrelationAnalyzer()
        )

        self.registry.register(
            MulticollinearityAnalyzer()
        )

    # =====================================================
    # PUBLIC API
    # =====================================================

    def profile(
        self,
        dataframe: pd.DataFrame
    ) -> ProfileResult:

        return self.run(dataframe)

    def run(
        self,
        dataframe: pd.DataFrame
    ) -> ProfileResult:

        self.validator.validate(dataframe)

        return self._execute(dataframe)

    # =====================================================
    # REGISTRY API
    # =====================================================

    def register(self, analyzer):

        self.registry.register(analyzer)

    def unregister(self, analyzer_name: str):

        self.registry.unregister(analyzer_name)

    def enable(self, analyzer_name: str):

        self.registry.enable(analyzer_name)

    def disable(self, analyzer_name: str):

        self.registry.disable(analyzer_name)

    def analyzers(self):

        return self.registry.names()

    def clear(self):

        self.registry.clear()

    # =====================================================
    # INTERNAL
    # =====================================================


    # =====================================================
    # EXECUTION
    # =====================================================

   # =====================================================
# EXECUTION
# =====================================================

def _execute(
    self,
    dataframe: pd.DataFrame
) -> ProfileResult:
    """
    Lance complètement le moteur de profilage.
    """

    start = perf_counter()

    # Validation
    self.validator.validate(dataframe)

    # Création du contexte
    context = self.factory.create_context(
        dataframe=dataframe
    )

    # Exécution des analyzers
    analyzer_results = self._run_analyzers(
        context
    )

    # Construction du profil
    profile = self.builder.build(
        analyzer_results=analyzer_results,
        metadata=self.factory.create_metadata(context),
        summary=self.factory.create_summary(context)
    )

    # Métadonnées d'exécution
    profile.metadata.execution_time = round(
        perf_counter() - start,
        4
    )

    profile.metadata.success = profile.is_valid

    return profile


# =====================================================
# ANALYZERS
# =====================================================

def _run_analyzers(
    self,
    context: ProfileContext
) -> list[AnalyzerResult]:
    """
    Exécute tous les analyzers enregistrés.

    Retourne la liste des AnalyzerResult.
    """

    results: list[AnalyzerResult] = []

    for analyzer in self.registry:

        analyzer_result = analyzer(context)

        results.append(analyzer_result)

    return results
    # =====================================================
    # STORE RESULT
    # =====================================================

    def _store_result(
        self,
        analyzer_result: AnalyzerResult,
        profile: ProfileResult
    ) -> None:
        """
        Enregistre le résultat d'un analyzer.
        """

        attribute = self._attribute_name(

            analyzer_result.name

        )

        if hasattr(

            profile,

            attribute

        ):

            setattr(

                profile,

                attribute,

                analyzer_result.result

            )

        else:

            profile.extras[attribute] = (

                analyzer_result.result

            )

        # ----------------------------------------------

        if analyzer_result.score is not None:

            profile.set_score(

                analyzer_result.name,

                analyzer_result.score

            )

        # ----------------------------------------------

        for warning in analyzer_result.warnings:

            profile.add_warning(

                warning

            )

        # ----------------------------------------------

        for error in analyzer_result.errors:

            profile.add_error(

                f"{analyzer_result.name} : {error}"

            )

        # ----------------------------------------------

        for recommendation in analyzer_result.recommendations:

            profile.add_recommendation(

                {

                    "analyzer": analyzer_result.name,

                    "message": recommendation

                }

            )

    # =====================================================
    # SUMMARY
    # =====================================================

    def _compute_summary(
        self,
        profile: ProfileResult
    ) -> None:
        """
        Calcule le résumé global.
        """

        summary = profile.summary

        # ----------------------------------------------

        if profile.datatypes:

            count = profile.datatypes.get(

                "count",

                {}

            )

            summary.numeric_columns = count.get(

                "numeric",

                0

            )

            summary.categorical_columns = count.get(

                "categorical",

                0

            )

            summary.boolean_columns = count.get(

                "boolean",

                0

            )

            summary.datetime_columns = count.get(

                "datetime",

                0

            )

            summary.text_columns = count.get(

                "text",

                0

            )

        # ----------------------------------------------

        if profile.missing:

            summary.missing_values = (

                profile.missing.get(

                    "total_missing",

                    0

                )

            )

            summary.missing_percentage = (

                profile.missing.get(

                    "missing_rate",

                    0

                )

            )

        # ----------------------------------------------

        if profile.duplicates:

            summary.duplicate_rows = (

                profile.duplicates.get(

                    "duplicate_rows",

                    0

                )

            )

            summary.duplicate_percentage = (

                profile.duplicates.get(

                    "duplicate_rate",

                    0

                )

            )

        # ----------------------------------------------

        if profile.quality:

            score = profile.quality.get(

                "quality_score",

                100

            )

            summary.quality_score = score

            summary.overall_score = score

        # ----------------------------------------------

        summary.warning_count = (

            profile.warning_count

        )

        summary.recommendation_count = (

            profile.recommendation_count

        )

        summary.critical_count = (

            profile.error_count

        )

        summary.analyzed_variables = (

            summary.columns

        )

    # =====================================================
    # METADATA
    # =====================================================

        # =====================================================
    # SUMMARY
    # =====================================================


    # =====================================================
    # ATTRIBUTE NAME
    # =====================================================

    @staticmethod
    def _attribute_name(
        analyzer_name: str
    ) -> str:
        """
        Convertit

        StructureAnalyzer

        en

        structure
        """

        return (

            analyzer_name

            .replace("Analyzer", "")

            .replace("analyzer", "")

            .strip()

            .lower()

        )

    # =====================================================
    # EXPORT
    # =====================================================

    def export_dict(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Retourne le profil sous forme
        de dictionnaire.
        """

        profile = self.profile(
            dataframe
        )

        return profile.to_dict()

    # =====================================================
    # EXPORT JSON
    # =====================================================

    def export_json(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Alias de export_dict().
        """

        return self.export_dict(
            dataframe
        )

    # =====================================================
    # INFORMATION
    # =====================================================

    def analyzer_count(self) -> int:
        """
        Nombre d'analyzers enregistrés.
        """

        return len(
            self.registry
        )

    def analyzer_names(
        self
    ) -> list[str]:
        """
        Liste des analyzers.
        """

        return self.registry.names()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self) -> None:
        """
        Réinitialise complètement
        le Profiler.
        """

        self.registry.clear()

        self._register_default_analyzers()

    # =====================================================
    # ENABLE / DISABLE
    # =====================================================

    def enable_all(self) -> None:
        """
        Active tous les analyzers.
        """

        for name in self.registry.names():

            self.registry.enable(name)

    def disable_all(self) -> None:
        """
        Désactive tous les analyzers.
        """

        for name in self.registry.names():

            self.registry.disable(name)

    # =====================================================
    # ITERATOR
    # =====================================================

    def __iter__(self):

        return iter(

            self.registry

        )

    # =====================================================
    # SIZE
    # =====================================================

    def __len__(self):

        return len(

            self.registry

        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (

            f"DatasetProfiler("

            f"{len(self.registry)} analyzers)"

        )

    def __repr__(self):

        return (

            f"DatasetProfiler("

            f"analyzers={len(self.registry)})"

        )