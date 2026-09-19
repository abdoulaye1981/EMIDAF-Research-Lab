"""
=========================================================
EMIDAF Framework v1.0
Numerical Analyzer
---------------------------------------------------------
Analyse statistique complète des variables numériques.
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext
from ....common.enums.data_quality import DataQuality

class NumericalAnalyzer(BaseAnalyzer):
    """
    Analyse complète des variables numériques.
    """

    name = "NumericalAnalyzer"

    version = "1.0.0"

    description = "Advanced Numerical Variable Analysis"

    CV_LOW = 15

    CV_MEDIUM = 30

    CV_HIGH = 60

    # =====================================================
    # PUBLIC
    # =====================================================

    def analyze(
        self,
        context: ProfileContext
    ) -> dict[str, Any]:
        """
        Analyse toutes les variables numériques.
        """

        dataframe = context.dataframe

        datatype_result = context.results.get("DatatypeAnalyzer")

        if datatype_result is None:
            result = {
                "variables": {},
                "summary": {},
                "quality_score": 100.0,
                "warnings": [],
                "recommendations": []
            }

            context.add_result(self.name, result)
            context.put_cache(self.name, result)

            return result
        datatype = datatype_result.result

        numeric_columns = datatype.get(
             "numeric",
             []
        )


        report = {

            "variables": {},

            "summary": {},

            "quality_score": 100.0,

            "warnings": [],

            "recommendations": []

        }

        for column in numeric_columns:

            report["variables"][column] = self._analyze_variable(

                dataframe[column]

            )

        self._build_summary(

            report

        )

        self._quality_analysis(

            report

        )

        self._build_recommendations(

            report

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
    # VARIABLE
    # =====================================================

    def _analyze_variable(
        self,
        series: pd.Series
    ) -> dict[str, Any]:
        """
        Analyse complète d'une variable numérique.
        """


        values = series.dropna()

        finite_values = values[
             np.isfinite(values)
        ]

        infinite_count = int(
              np.isinf(values).sum()
        )

        report = {
              "name": series.name,
              "dtype": str(series.dtype),
              "count": int(values.count()),
              "finite_count": int(finite_values.count()),
              "missing": int(series.isna().sum()),
              "unique": int(finite_values.nunique()),
              "zeros": int((finite_values == 0).sum()),
              "negative": int((finite_values < 0).sum()),
              "positive": int((finite_values > 0).sum()),
              "infinite": int(np.isinf(values).sum()),

        }

        report.update(
               self._descriptive_statistics(
                    finite_values
               )
        )

        report.update(
               self._dispersion_statistics(
                    finite_values
               )
        )

        report.update(
               self._quantile_statistics(
                    finite_values
               )
        )

        report.update(
               self._distribution_statistics(
                    finite_values
               )
        )

        report.update(
               self._shape_statistics(
                    finite_values
               )
        )

        report.update(
               self._value_statistics(
                    values,
                    finite_values
               )
        )

        return report

        # =====================================================
    # DESCRIPTIVE STATISTICS
    # =====================================================

    def _descriptive_statistics(
        self,
        values: pd.Series,
    ) -> dict[str, Any]:
        """
        Statistiques descriptives classiques.
        """

        if values.empty:

            return {

                "sum": 0.0,

                "mean": np.nan,

                "median": np.nan,

                "mode": np.nan,

                "min": np.nan,

                "max": np.nan,

                "range": np.nan,

            }

        mode = values.mode(dropna=True)

        return {

            "sum": float(values.sum()),

            "mean": float(values.mean()),

            "median": float(values.median()),

            "mode": (

                float(mode.iloc[0])

                if not mode.empty

                else np.nan

            ),

            "min": float(values.min()),

            "max": float(values.max()),

            "range": float(

                values.max() -

                values.min()

            ),

        }

    # =====================================================
    # DISPERSION
    # =====================================================

    def _dispersion_statistics(
        self,
        values: pd.Series,
    ) -> dict[str, Any]:
        """
        Mesures de dispersion.
        """

        if values.empty:

            return {

                "variance": np.nan,

                "std": np.nan,

                "iqr": np.nan,

                "mad": np.nan,

                "cv": np.nan,

            }

        variance = float(

            values.var()

        )

        std = float(

            values.std()

        )

        q1 = float(

            values.quantile(

                0.25

            )

        )

        q3 = float(

            values.quantile(

                0.75

            )

        )

        iqr = q3 - q1

        median = float(

            values.median()

        )

        mad = float(

            np.median(

                np.abs(

                    values - median

                )

            )

        )

        mean = float(

            values.mean()

        )

        if mean == 0:

            cv = np.nan

        else:

            cv = (

                std /

                abs(mean)

            ) * 100

        return {

            "variance": variance,

            "std": std,

            "iqr": iqr,

            "mad": mad,

            "cv": cv,

        }

        # =====================================================
    # QUANTILES
    # =====================================================

    def _quantile_statistics(
        self,
        values: pd.Series,
    ) -> dict[str, Any]:
        """
        Calcule les principaux quantiles.
        """

        if values.empty:

            return {

                "q1": np.nan,

                "q2": np.nan,

                "q3": np.nan,

                "p1": np.nan,

                "p5": np.nan,

                "p10": np.nan,

                "p25": np.nan,

                "p50": np.nan,

                "p75": np.nan,

                "p90": np.nan,

                "p95": np.nan,

                "p99": np.nan,

            }

        return {

            "q1": float(values.quantile(0.25)),

            "q2": float(values.quantile(0.50)),

            "q3": float(values.quantile(0.75)),

            "p1": float(values.quantile(0.01)),

            "p5": float(values.quantile(0.05)),

            "p10": float(values.quantile(0.10)),

            "p25": float(values.quantile(0.25)),

            "p50": float(values.quantile(0.50)),

            "p75": float(values.quantile(0.75)),

            "p90": float(values.quantile(0.90)),

            "p95": float(values.quantile(0.95)),

            "p99": float(values.quantile(0.99))

        }

    # =====================================================
    # DISTRIBUTION
    # =====================================================

    def _distribution_statistics(
        self,
        values: pd.Series,
    ) -> dict[str, Any]:
        """
        Statistiques décrivant la distribution.
        """

        if values.empty:

            return {

                "skewness": np.nan,

                "kurtosis": np.nan,

                "entropy": np.nan,

            }

        skewness = float(

            values.skew()

        )

        kurtosis = float(

            values.kurt()

        )

        frequencies = (

            values

            .value_counts(

                normalize=True,

                dropna=True

            )

        )

        entropy = float(

            -(

                frequencies *

                np.log2(

                    frequencies

                )

            ).sum()

        )

        return {

            "skewness": skewness,

            "kurtosis": kurtosis,

            "entropy": entropy,

        }

        # =====================================================
    # SHAPE ANALYSIS
    # =====================================================

    def _shape_statistics(
        self,
        values: pd.Series,
    ) -> dict[str, Any]:
        """
        Analyse la forme de la variable.
        """

        if values.empty:

            return {

                "constant": False,

                "quasi_constant": False,

                "binary": False,

                "discrete": False,

                "continuous": False,

                "symmetric": False,

                "right_skewed": False,

                "left_skewed": False,

                "leptokurtic": False,

                "platykurtic": False,

                "mesokurtic": False,

            }

        unique = values.nunique()

        skewness = float(values.skew())

        kurtosis = float(values.kurt())

        constant = unique == 1

        quasi_constant = unique <= 2

        binary = unique == 2

        discrete = (

            pd.api.types.is_integer_dtype(

                values

            )

            or

            unique <= 20

        )

        continuous = not discrete

        symmetric = abs(skewness) < 0.5

        right_skewed = skewness >= 0.5

        left_skewed = skewness <= -0.5

        leptokurtic = kurtosis > 0

        platykurtic = kurtosis < 0

        mesokurtic = abs(kurtosis) < 0.25

        return {

            "constant": constant,

            "quasi_constant": quasi_constant,

            "binary": binary,

            "discrete": discrete,

            "continuous": continuous,

            "symmetric": symmetric,

            "right_skewed": right_skewed,

            "left_skewed": left_skewed,

            "leptokurtic": leptokurtic,

            "platykurtic": platykurtic,

            "mesokurtic": mesokurtic,

        }

    # =====================================================
    # VALUE ANALYSIS
    # =====================================================

    def _value_statistics(
            self,
            values: pd.Series,
            finite_values: pd.Series,
         ) -> dict[str, Any]:
            """
            Analyse les caractéristiques des valeurs.
            """

            if values.empty:
                return {
                    "positive": 0,
                    "negative": 0,
                    "zeros": 0,
                    "positive_rate": 0.0,
                    "negative_rate": 0.0,
                    "zero_rate": 0.0,
                    "finite": 0,
                    "infinite": 0,
                    "finite_rate": 0.0,
                    "infinite_rate": 0.0,
                }

            total = len(values)

            positive = int(
                (finite_values > 0).sum()
            )

            negative = int(
                (finite_values < 0).sum()
            )

            zeros = int(
                (finite_values == 0).sum()
            )

            infinite = int(
                np.isinf(values).sum()
            )

            finite = len(finite_values)

            finite_total = len(finite_values)

            if finite_total == 0:
                positive_rate = 0.0
                negative_rate = 0.0
                zero_rate = 0.0
            else:
                positive_rate = (
                    100 * positive / finite_total
                )
                negative_rate = (
                    100 * negative / finite_total
                )
                zero_rate = (
                    100 * zeros / finite_total
                )

            return {
                "positive": positive,
                "negative": negative,
                "zeros": zeros,
                "positive_rate": round(
                    positive_rate,
                    2
                ),
                "negative_rate": round(
                   negative_rate,
                   2
                ),
                "zero_rate": round(
                   zero_rate,
                   2
                ),
                "finite": finite,
                "infinite": infinite,
                "finite_rate": round(
                    100 * finite / total,
                    2
                ),
                "infinite_rate": round(
                    100 * infinite / total,
                    2
                ),
        }
        # =====================================================
    # SUMMARY
    # =====================================================

    def _build_summary(
        self,
        report: dict[str, Any],
    ) -> None:
        """
        Construit le résumé global des variables numériques.
        """

        variables = report["variables"]

        summary = {

            "variable_count": len(variables),

            "constant_variables": 0,

            "quasi_constant_variables": 0,

            "binary_variables": 0,

            "discrete_variables": 0,

            "continuous_variables": 0,

            "variables_with_missing": 0,

            "variables_with_infinite": 0,

            "variables_with_negative": 0,

            "variables_with_zero": 0,

            "right_skewed": 0,

            "left_skewed": 0,

            "symmetric": 0,

            "leptokurtic": 0,

            "platykurtic": 0,

            "mesokurtic": 0,

            "average_cv": 0.0,

            "average_skewness": 0.0,

            "average_kurtosis": 0.0

        }

        cvs = []

        skews = []

        kurtosis_values = []

        for stats in variables.values():

            summary["constant_variables"] += int(stats["constant"])

            summary["quasi_constant_variables"] += int(stats["quasi_constant"])

            summary["binary_variables"] += int(stats["binary"])

            summary["discrete_variables"] += int(stats["discrete"])

            summary["continuous_variables"] += int(stats["continuous"])

            summary["variables_with_missing"] += int(stats["missing"] > 0)

            summary["variables_with_infinite"] += int(stats["infinite"] > 0)

            summary["variables_with_negative"] += int(stats["negative"] > 0)

            summary["variables_with_zero"] += int(stats["zeros"] > 0)

            summary["right_skewed"] += int(stats["right_skewed"])

            summary["left_skewed"] += int(stats["left_skewed"])

            summary["symmetric"] += int(stats["symmetric"])

            summary["leptokurtic"] += int(stats["leptokurtic"])

            summary["platykurtic"] += int(stats["platykurtic"])

            summary["mesokurtic"] += int(stats["mesokurtic"])

            if not np.isnan(stats["cv"]):

                cvs.append(stats["cv"])

            if not np.isnan(stats["skewness"]):

                skews.append(stats["skewness"])

            if not np.isnan(stats["kurtosis"]):

                kurtosis_values.append(stats["kurtosis"])

        summary["average_cv"] = round(

            float(np.mean(cvs)),

            2

        ) if cvs else np.nan

        summary["average_skewness"] = round(

            float(np.mean(skews)),

            3

        ) if skews else np.nan

        summary["average_kurtosis"] = round(

            float(np.mean(kurtosis_values)),

            3

        ) if kurtosis_values else np.nan

        report["summary"] = summary

    # =====================================================
    # QUALITY
    # =====================================================

    def _quality_analysis(
        self,
        report: dict[str, Any],
    ) -> None:
        """
        Calcule le score de qualité
        des variables numériques.
        """

        summary = report["summary"]

        score = 100.0

        score -= summary["constant_variables"] * 8

        score -= summary["quasi_constant_variables"] * 4

        score -= summary["variables_with_missing"] * 2

        score -= summary["variables_with_infinite"] * 5

        score = max(

            0.0,

            min(

                100.0,

                score

            )

        )

        report["quality_score"] = round(

            score,

            2

        )

        if score >= 90:

            level = DataQuality.EXCELLENT.value

        elif score >= 80:

            level = DataQuality.VERY_GOOD.value

        elif score >= 70:

            level = DataQuality.GOOD.value

        elif score >= 60:

            level = DataQuality.FAIR.value

        elif score >= 40:

            level = DataQuality.POOR.value

        else:

            level = DataQuality.CRITICAL.value

        summary["quality_level"] = level

        # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _build_recommendations(
        self,
        report: dict[str, Any],
    ) -> None:
        """
        Génère automatiquement les recommandations.
        """

        summary = report["summary"]

        recommendations = report["recommendations"]

        warnings = report["warnings"]

        # ================================================
        # VARIABLES CONSTANTES
        # ================================================

        if summary["constant_variables"] > 0:

            recommendations.append(

                "Supprimer les variables constantes car elles n'apportent aucune information."

            )

            warnings.append(

                f"{summary['constant_variables']} variable(s) constante(s) détectée(s)."

            )

        # ================================================
        # VARIABLES QUASI CONSTANTES
        # ================================================

        if summary["quasi_constant_variables"] > 0:

            recommendations.append(

                "Examiner les variables quasi constantes avant la modélisation."

            )

        # ================================================
        # VARIABLES AVEC VALEURS MANQUANTES
        # ================================================

        if summary["variables_with_missing"] > 0:

            recommendations.append(

                "Traiter les valeurs manquantes avant toute analyse statistique."

            )

        # ================================================
        # VARIABLES AVEC INFINIS
        # ================================================

        if summary["variables_with_infinite"] > 0:

            warnings.append(

                "Des valeurs infinies ont été détectées."

            )

            recommendations.append(

                "Remplacer ou supprimer les valeurs infinies."

            )

        # ================================================
        # ASYMETRIE
        # ================================================

        if summary["right_skewed"] > 0:

            recommendations.append(

                "Certaines variables sont fortement asymétriques à droite. Une transformation logarithmique ou Box-Cox peut être envisagée."

            )

        if summary["left_skewed"] > 0:

            recommendations.append(

                "Certaines variables présentent une asymétrie à gauche."

            )

        # ================================================
        # COEFFICIENT DE VARIATION
        # ================================================

        average_cv = summary["average_cv"]

        if not np.isnan(average_cv):

            if average_cv > self.CV_HIGH:

                warnings.append(

                    "La variabilité moyenne des variables numériques est très élevée."

                )

            elif average_cv > self.CV_MEDIUM:

                recommendations.append(

                    "La dispersion des variables numériques est importante."

                )

        # ================================================
        # SCORE GLOBAL
        # ================================================

        score = report["quality_score"]

        if score >= 90:

            recommendations.append(

                "Les variables numériques présentent une excellente qualité."

            )

        elif score >= 75:

            recommendations.append(

                "Les variables numériques sont adaptées aux analyses statistiques."

            )

        elif score >= 60:

            recommendations.append(

                "Un nettoyage complémentaire est recommandé avant la modélisation."

            )

        else:

            warnings.append(

                "Les variables numériques nécessitent un nettoyage approfondi."

            )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"version='{self.version}')"

        )
