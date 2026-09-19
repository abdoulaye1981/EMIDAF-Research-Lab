"""
=========================================================
EMIDAF Framework v1.0
Missing Analyzer
---------------------------------------------------------
Analyse avancée des valeurs manquantes.
=========================================================
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from emidaf_core.core.base_analyzer import BaseAnalyzer
from emidaf_core.missing.mechanism.mechanism_analyzer import (
    MechanismAnalyzer,
)

from ..profile_context import ProfileContext
from ....common.enums.data_quality import DataQuality
from ....common.enums.imputation_strategy import ImputationStrategy

class MissingAnalyzer(BaseAnalyzer):
    """
    Analyse complète des valeurs manquantes.

    Cette classe calcule :

    • statistiques globales
    • statistiques par variable
    • statistiques par ligne
    • patterns
    • score de complétude
    • recommandations
    • préparation MCAR/MAR/MNAR
    """

    name = "MissingAnalyzer"

    version = "1.0.0"

    description = "Advanced Missing Value Analysis"

    LOW_RATE = 5.0

    MEDIUM_RATE = 20.0

    HIGH_RATE = 40.0

    WARNING_RATE = 10.0

    MAX_PATTERNS = 20

    # =====================================================
    # PUBLIC
    # =====================================================

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:
        """
        Analyse complète des valeurs manquantes.
        """

        df = context.dataframe

        rows = context.rows

        columns = context.columns

        cells = rows * columns

        missing = df.isna()

        missing_per_column = missing.sum()

        missing_per_row = missing.sum(axis=1)

        total_missing = int(
            missing_per_column.sum()
        )

        global_rate = (
            round(
                100 * total_missing / cells,
                2
            )
            if cells > 0
            else 0.0
        )

        report = {

            "rows": rows,

            "columns": columns,

            "cells": cells,

            "total_missing": total_missing,

            "missing_rate": global_rate,

            "column_statistics": {},

            "row_statistics": {},

            "classification": {},

            "patterns": [],

            "co_occurrence": {},

            "imputation_candidates": [],

            "summary": {},

            "quality_score": 100.0,

            "missing_mechanism": {},

            "warnings": [],

            "recommendations": []

        }

        summary = report["summary"]

        # ---------------------------------------------

        self._analyze_columns(

            df=df,

            report=report,

            missing_per_column=missing_per_column,

            rows=rows

        )

        # ---------------------------------------------

        self._analyze_rows(

            report=report,

            missing_per_row=missing_per_row,

            rows=rows,

            columns=columns

        )

        # ---------------------------------------------

        self._compute_patterns(

            report=report,

            missing=missing,

            rows=rows

        )

        # ---------------------------------------------

        self._compute_density(

            summary=summary,

            total_missing=total_missing,

            cells=cells

        )

        # ---------------------------------------------

        self._compute_quality(

            report=report,

            global_rate=global_rate

        )

        # ---------------------------------------------

        self._compute_co_occurrence(

            report=report,

            dataframe=df,

            missing_per_column=missing_per_column

        )

        # ---------------------------------------------

        self._compute_imputation(

            report=report,

            dataframe=df

        )

        # ---------------------------------------------

        self._prepare_missing_mechanism(
            report=report,
            dataframe=df,
        )
        # ---------------------------------------------

        self._build_recommendations(

            report=report

        )

        context.add_result(

            self.name,

            report

        )

        context.put_cache(

            self.name,

            report

        )

        return report

    # =====================================================
    # COLUMN ANALYSIS
    # =====================================================

    def _analyze_columns(
        self,
        df,
        report: dict[str, Any],
        missing_per_column,
        rows: int
    ) -> None:
        """
        Analyse les valeurs manquantes par variable.
        """

        column_statistics = report["column_statistics"]

        summary = report["summary"]

        classification = {

            "perfect": [],

            "excellent": [],

            "acceptable": [],

            "critical": [],

            "empty": []

        }

        complete_columns = []

        partial_columns = []

        empty_columns = []

        for column in df.columns:

            missing_count = int(
                missing_per_column[column]
            )

            missing_percentage = (
                round(
                    100 * missing_count / rows,
                    2
                )
                if rows > 0
                else 0.0
            )

            non_missing = rows - missing_count

            completeness = round(
                100 - missing_percentage,
                2
            )

            info = {

                "dtype": str(df[column].dtype),

                "missing_count": missing_count,

                "missing_percentage": missing_percentage,

                "non_missing": non_missing,

                "non_missing_percentage": completeness,

                "complete": missing_count == 0,

                "empty": missing_count == rows,

                "unique_values": int(
                    df[column].nunique(
                        dropna=True
                    )
                )

            }

            column_statistics[column] = info

            if missing_count == 0:

                complete_columns.append(column)

                classification["perfect"].append(column)

            elif missing_percentage < self.LOW_RATE:

                partial_columns.append(column)

                classification["excellent"].append(column)

            elif missing_percentage < self.MEDIUM_RATE:

                partial_columns.append(column)

                classification["acceptable"].append(column)

            elif missing_percentage < 100:

                partial_columns.append(column)

                classification["critical"].append(column)

            else:

                empty_columns.append(column)

                classification["empty"].append(column)

        summary["complete_columns"] = len(
            complete_columns
        )

        summary["partial_columns"] = len(
            partial_columns
        )

        summary["empty_columns"] = len(
            empty_columns
        )

        summary["complete_column_names"] = complete_columns

        summary["empty_column_names"] = empty_columns

        report["classification"] = classification

        # =====================================================
    # ROW ANALYSIS
    # =====================================================

    def _analyze_rows(
        self,
        report: dict[str, Any],
        missing_per_row,
        rows: int,
        columns: int,
    ) -> None:
        """
        Analyse les valeurs manquantes par ligne.
        """

        complete_rows = int(
            (missing_per_row == 0).sum()
        )

        rows_with_missing = int(
            (missing_per_row > 0).sum()
        )

        empty_rows = int(
            (missing_per_row == columns).sum()
        )

        row_statistics = {

            "complete_rows": complete_rows,

            "rows_with_missing": rows_with_missing,

            "empty_rows": empty_rows,

            "complete_percentage": (
                round(
                    100 * complete_rows / rows,
                    2
                )
                if rows > 0
                else 0.0
            ),

            "rows_with_missing_percentage": (
                round(
                    100 * rows_with_missing / rows,
                    2
                )
                if rows > 0
                else 0.0
            ),

            "empty_rows_percentage": (
                round(
                    100 * empty_rows / rows,
                    2
                )
                if rows > 0
                else 0.0
            ),

            "max_missing_per_row": int(
                missing_per_row.max()
            ) if rows > 0 else 0,

            "mean_missing_per_row": round(
                float(
                    missing_per_row.mean()
                ),
                2
            ) if rows > 0 else 0.0,

            "median_missing_per_row": round(
                float(
                    missing_per_row.median()
                ),
                2
            ) if rows > 0 else 0.0,

        }

        report["row_statistics"] = row_statistics

    # =====================================================
    # MISSING PATTERNS
    # =====================================================

    def _compute_patterns(
        self,
        report: dict[str, Any],
        missing,
        rows: int,
    ) -> None:
        """
        Analyse les motifs (patterns)
        des valeurs manquantes.
        """

        patterns = Counter()

        for _, row in missing.iterrows():

            pattern = tuple(
                row.astype(int)
            )

            patterns[pattern] += 1

        report["patterns"] = [

            {

                "pattern": list(pattern),

                "count": count,

                "percentage": (
                    round(
                        100 * count / rows,
                        2
                    )
                    if rows > 0
                    else 0.0
                ),

            }

            for pattern, count

            in patterns.most_common(

                self.MAX_PATTERNS

            )

        ]

        report["summary"]["pattern_count"] = len(
            patterns
        )

    # =====================================================
    # MISSING DENSITY
    # =====================================================

    def _compute_density(
        self,
        summary: dict[str, Any],
        total_missing: int,
        cells: int,
    ) -> None:
        """
        Calcule la densité des valeurs
        manquantes.
        """

        density = (

            total_missing / cells

            if cells > 0

            else 0.0

        )

        summary["missing_density"] = round(
            density,
            4
        )

        # =====================================================
    # DATA QUALITY
    # =====================================================

    def _compute_quality(
        self,
        report: dict[str, Any],
        global_rate: float,
    ) -> None:
        """
        Calcule le score de qualité.
        """

        score = max(
            0.0,
            min(
                100.0,
                100.0 - global_rate
            )
        )

        score = round(
            score,
            2
        )

        report["quality_score"] = score

        report["summary"]["completeness_score"] = score

        if global_rate == 0:

            quality = DataQuality.EXCELLENT.value

        elif global_rate < self.LOW_RATE:

            quality = DataQuality.VERY_GOOD.value

        elif global_rate < self.MEDIUM_RATE:

            quality = DataQuality.GOOD.value

        elif global_rate < self.HIGH_RATE:

            quality = DataQuality.FAIR.value

        elif global_rate < 60:

            quality = DataQuality.POOR.value

        else:

            quality = DataQuality.CRITICAL.value

        report["summary"]["quality_level"] = quality

    # =====================================================
    # CO-OCCURRENCE
    # =====================================================

    def _compute_co_occurrence(
        self,
        report: dict[str, Any],
        dataframe,
        missing_per_column,
    ) -> None:
        """
        Calcule la matrice de co-occurrence
        des valeurs manquantes.
        """

        co_occurrence = {}

        missing_columns = [

            column

            for column in dataframe.columns

            if missing_per_column[column] > 0

        ]

        for column_a in missing_columns:

            co_occurrence[column_a] = {}

            mask_a = dataframe[column_a].isna()

            for column_b in missing_columns:

                mask_b = dataframe[column_b].isna()

                co_occurrence[column_a][column_b] = int(

                    (mask_a & mask_b).sum()

                )

        report["co_occurrence"] = co_occurrence

        report["summary"]["columns_with_missing"] = len(
            missing_columns
        )

    # =====================================================
    # IMPUTATION STRATEGY
    # =====================================================

    def _compute_imputation(
        self,
        report: dict[str, Any],
        dataframe,
    ) -> None:
        """
        Détermine automatiquement la stratégie
        d'imputation recommandée.
        """

        candidates = []

        for column, info in report["column_statistics"].items():

            rate = info["missing_percentage"]

            dtype = str(
                dataframe[column].dtype
            ).lower()

            if rate == 0:

                strategy = ImputationStrategy.NONE.value

            elif rate < self.LOW_RATE:

                if (

                    "int" in dtype

                    or

                    "float" in dtype

                ):

                    strategy = ImputationStrategy.MEAN.value

                else:

                    strategy = ImputationStrategy.MODE.value

            elif rate < self.MEDIUM_RATE:

                strategy = ImputationStrategy.KNN.value

            elif rate < self.HIGH_RATE:

                strategy = ImputationStrategy.MICE.value

            else:

                strategy = ImputationStrategy.REVIEW.value

            candidates.append({

                "column": column,

                "dtype": dtype,

                "missing_percentage": rate,

                "recommended_strategy": strategy

            })

        report["imputation_candidates"] = candidates

        # =====================================================
    # MISSING MECHANISM
    # =====================================================

    def _prepare_missing_mechanism(
        self,
        report: dict[str, Any],
        dataframe,
    ) -> None:

       analyzer = MechanismAnalyzer()

       report["missing_mechanism"] = analyzer.analyze(
          dataframe=dataframe
       )

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _build_recommendations(
        self,
        report: dict[str, Any],
    ) -> None:
        """
        Génère automatiquement les
        recommandations.
        """

        recommendations = report["recommendations"]

        warnings = report["warnings"]

        quality = report["summary"]["quality_level"]

        empty_columns = report["summary"]["empty_columns"]

        critical = len(

            report["classification"]["critical"]

        )

        missing_rate = report["missing_rate"]

        # ---------------------------------------------
        # RECOMMENDATIONS
        # ---------------------------------------------

        if missing_rate == 0:

            recommendations.append(

                "Aucune valeur manquante détectée."

            )

            return

        recommendations.append(

            "Identifier le mécanisme des valeurs manquantes (MCAR, MAR ou MNAR)."

        )

        recommendations.append(

            "Choisir une méthode d'imputation adaptée avant toute modélisation."

        )

        if critical > 0:

            recommendations.append(

                f"Examiner les {critical} variable(s) présentant plus de "

                f"{self.MEDIUM_RATE:.0f}% de valeurs manquantes."

            )

        if empty_columns > 0:

            recommendations.append(

                "Supprimer ou reconstruire les colonnes entièrement vides."

            )

        if quality in (

            DataQuality.POOR.value,

            DataQuality.CRITICAL.value,

        ):

            recommendations.append(

                "Une étape de nettoyage approfondi est fortement recommandée."

            )

        # ---------------------------------------------
        # WARNINGS
        # ---------------------------------------------

        if missing_rate > self.WARNING_RATE:

            warnings.append(

                f"Le dataset contient "

                f"{missing_rate:.2f}% "

                f"de valeurs manquantes."

            )

        if empty_columns > 0:

            warnings.append(

                f"{empty_columns} colonne(s) "

                f"entièrement vide(s)."

            )

        if critical > 0:

            warnings.append(

                f"{critical} variable(s) "

                f"présentent un taux critique "

                f"de valeurs manquantes."

            )
