"""
=========================================================
EMIDAF Framework v1.0
Profile Builder
---------------------------------------------------------
Construction du ProfileResult à partir des
AnalyzerResult.
=========================================================
"""

from __future__ import annotations

from typing import Iterable

from .profile_metadata import ProfileMetadata
from .profile_result import ProfileResult
from .profile_summary import ProfileSummary

from .analyzers.analyzer_result import AnalyzerResult


from emidaf_core.core.base_builder import BaseBuilder

class ProfileBuilder(BaseBuilder):
    """
    Construit un ProfileResult.

    Cette classe ne lance aucun Analyzer.

    Elle assemble uniquement les résultats.
    """

    def __init__(self):

        super().__init__()

        self._profile = ProfileResult()

    # =====================================================
    # PUBLIC
    # =====================================================

    def build(
        self,
        analyzer_results: Iterable[AnalyzerResult],
        metadata: ProfileMetadata,
        summary: ProfileSummary
    ) -> ProfileResult:
        """
        Construit complètement le ProfileResult.
        """

        self.reset()

        self._profile.metadata = metadata

        self._profile.summary = summary

        self._populate(analyzer_results)

        self._finalize()

        return self._profile

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        super().reset()

        self._profile = ProfileResult()

    # =====================================================
    # POPULATE
    # =====================================================

    def _populate(
        self,
        analyzer_results: Iterable[AnalyzerResult]
    ) -> None:

        for analyzer in analyzer_results:

            self._add_result(analyzer)

            self._add_warnings(analyzer)

            self._add_errors(analyzer)

            self._add_recommendations(analyzer)

            self._add_scores(analyzer)

    # =====================================================
    # RESULT
    # =====================================================

    def _add_result(
        self,
        analyzer: AnalyzerResult
    ) -> None:

        attribute = self._attribute_name(

            analyzer.name

        )

        if hasattr(

            self._profile,

            attribute

        ):

            setattr(

                self._profile,

                attribute,

                analyzer.result

            )

        else:

            self._profile.extras[attribute] = (

                analyzer.result

            )

        # =====================================================
    # WARNINGS
    # =====================================================

    def _add_warnings(
        self,
        analyzer: AnalyzerResult
    ) -> None:
        """
        Ajoute les avertissements.
        """

        if not analyzer.warnings:
            return

        for warning in analyzer.warnings:

            self._profile.add_warning(
                warning
            )

    # =====================================================
    # ERRORS
    # =====================================================

    def _add_errors(
        self,
        analyzer: AnalyzerResult
    ) -> None:
        """
        Ajoute les erreurs.
        """

        if not analyzer.errors:
            return

        for error in analyzer.errors:

            self._profile.add_error(

                f"{analyzer.name}: {error}"

            )

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _add_recommendations(
        self,
        analyzer: AnalyzerResult
    ) -> None:
        """
        Ajoute les recommandations.
        """

        if not analyzer.recommendations:
            return

        for recommendation in analyzer.recommendations:

            self._profile.add_recommendation(

                {

                    "analyzer": analyzer.name,

                    "message": recommendation,

                    "priority": "MEDIUM"

                }

            )

    # =====================================================
    # SCORES
    # =====================================================

    def _add_scores(
        self,
        analyzer: AnalyzerResult
    ) -> None:
        """
        Enregistre les scores.
        """

        if analyzer.score is None:

            return

        self._profile.set_score(

            analyzer.name,

            analyzer.score

        )

    # =====================================================
    # ATTRIBUTE NAME
    # =====================================================

    @staticmethod
    def _attribute_name(
        analyzer_name: str
    ) -> str:

        mapping = {
            "StructureAnalyzer": "structure",
            "structure": "structure",

            "DatatypeAnalyzer": "datatypes",
            "datatype": "datatypes",

            "MemoryAnalyzer": "memory",
            "memory": "memory",

            "QualityAnalyzer": "quality",
            "quality": "quality",

            "MissingAnalyzer": "missing",
            "missing": "missing",

            "DuplicateAnalyzer": "duplicates",
            "duplicates": "duplicates",

            "CardinalityAnalyzer": "cardinality",
            "cardinality": "cardinality",

            "UniquenessAnalyzer": "uniqueness",
            "uniqueness": "uniqueness",

            "ConsistencyAnalyzer": "consistency",
            "consistency": "consistency",

            "NumericalAnalyzer": "numerical",
            "numerical": "numerical",

            "CategoricalAnalyzer": "categorical",
            "categorical": "categorical",

            "DatetimeAnalyzer": "datetime",
            "datetime": "datetime",

            "TextAnalyzer": "text",
            "text": "text",

            "DistributionAnalyzer": "distributions",
            "distribution": "distributions",
            "distributions": "distributions",

            "NormalityAnalyzer": "normality",
            "normality": "normality",

            "OutlierAnalyzer": "outliers",
            "outlier": "outliers",
            "Outlier Analysis": "outliers",

            "CorrelationAnalyzer": "correlations",
            "correlation": "correlations",
            "correlations": "correlations",

            "MulticollinearityAnalyzer": "multicollinearity",
            "multicollinearity": "multicollinearity"
        }

        return mapping.get(
            analyzer_name,
            analyzer_name
            .replace("Analyzer", "")
            .replace("analyzer", "")
            .strip()
            .lower()
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def _update_summary(
        self
    ) -> None:
        """
        Met à jour le résumé.
        """

        summary = self._profile.summary

        # ------------------------------------------

        if self._profile.datatypes:

            count = self._profile.datatypes.get(

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

        # ------------------------------------------

        if self._profile.missing:

            summary.missing_values = (

                self._profile.missing.get(

                    "total_missing",

                    0

                )

            )

            summary.missing_percentage = (

                self._profile.missing.get(

                    "missing_rate",

                    0

                )

            )

        # ------------------------------------------

        if self._profile.duplicates:

            summary.duplicate_rows = (

                self._profile.duplicates.get(

                    "duplicate_rows",

                    0

                )

            )

            summary.duplicate_percentage = (

                self._profile.duplicates.get(

                    "duplicate_rate",

                    0

                )

            )

        # ------------------------------------------

        if self._profile.quality:

            score = self._profile.quality.get(

                "quality_score",

                100

            )

            summary.quality_score = score

            summary.overall_score = score

        # ------------------------------------------

        summary.warning_count = (

            self._profile.warning_count

        )

        summary.recommendation_count = (

            self._profile.recommendation_count

        )

        summary.critical_count = (

            self._profile.error_count

        )

        summary.analyzed_variables = (

            summary.columns

        )

        # =====================================================
    # METADATA
    # =====================================================

    def _update_metadata(self) -> None:
        """
        Met à jour les métadonnées du profil.
        """

        metadata = self._profile.metadata
        summary = self._profile.summary

        metadata.warning_count = self._profile.warning_count
        metadata.error_count = self._profile.error_count

        metadata.analyzed_rows = summary.rows
        metadata.analyzed_columns = summary.columns
        metadata.analyzed_cells = summary.cells
        metadata.memory_usage = summary.memory_usage

        metadata.success = self._profile.is_valid

    # =====================================================
    # SCORES
    # =====================================================

    def _compute_scores(self) -> None:
        """
        Calcule les scores globaux.
        """

        summary = self._profile.summary

        quality = summary.quality_score

        completeness = max(
            0.0,
            100.0 - summary.missing_percentage
        )

        uniqueness = max(
            0.0,
            100.0 - summary.duplicate_percentage
        )

        consistency = quality

        validity = quality

        overall = round(

            (

                quality +

                completeness +

                uniqueness +

                consistency +

                validity

            ) / 5,

            2

        )

        summary.completeness_score = round(
            completeness,
            2
        )

        summary.uniqueness_score = round(
            uniqueness,
            2
        )

        summary.consistency_score = round(
            consistency,
            2
        )

        summary.validity_score = round(
            validity,
            2
        )

        summary.overall_score = overall

        self._profile.set_score(
            "quality",
            quality
        )

        self._profile.set_score(
            "completeness",
            completeness
        )

        self._profile.set_score(
            "uniqueness",
            uniqueness
        )

        self._profile.set_score(
            "consistency",
            consistency
        )

        self._profile.set_score(
            "validity",
            validity
        )

        self._profile.set_score(
            "overall",
            overall
        )

    # =====================================================
    # FINALIZE
    # =====================================================

    def _finalize(self) -> None:
        """
        Finalisation complète du ProfileResult.
        """

        self._update_summary()

        self._compute_scores()

        self._update_metadata()

        self._profile.summary.finalize()

    # =====================================================
    # EXPORT
    # =====================================================

    def to_profile(self) -> ProfileResult:
        """
        Retourne le ProfileResult construit.
        """

        return self._profile

    # =====================================================
    # RESET BUILDER
    # =====================================================

    def clear(self) -> None:
        """
        Réinitialise complètement le builder.
        """

        self.reset()

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __str__(self) -> str:

        return "ProfileBuilder"

    def __repr__(self) -> str:

        return (

            f"ProfileBuilder("

            f"warnings={self._profile.warning_count}, "

            f"errors={self._profile.error_count}, "

            f"recommendations={self._profile.recommendation_count})"

        )
