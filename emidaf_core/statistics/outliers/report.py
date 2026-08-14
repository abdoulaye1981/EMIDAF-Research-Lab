"""
=========================================================
EMIDAF Framework
Outlier Report
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Rapport complet des valeurs aberrantes.

=========================================================
"""

from __future__ import annotations

import pandas as pd

from ...common.results import ReportResult

from .statistical import StatisticalOutlierDetector
from .distance import DistanceOutlierDetector
from .density import DensityOutlierDetector
from .clustering import ClusteringOutlierDetector
from .ensemble import EnsembleOutlierDetector
from .multivariate import MultivariateOutlierDetector


class OutlierReport:
    """
    Générateur de rapport complet.
    """

    @staticmethod
    def generate(
        dataframe: pd.DataFrame,
        target: str | None = None,
    ) -> ReportResult:

        statistical = {}
        distance = {}
        density = {}
        clustering = {}
        ensemble = {}
        multivariate = {}

        numeric = dataframe.select_dtypes(include="number")

        # ============================================
        # Univarié
        # ============================================

        for column in numeric.columns:

            statistical[column] = (

                StatisticalOutlierDetector.compute(

                    numeric[column]

                )

            )

        # ============================================
        # Multivarié
        # ============================================

        if len(numeric.columns) > 1:

            distance = (

                DistanceOutlierDetector.compute(

                    numeric,

                    target

                )

            )

            density = (

                DensityOutlierDetector.compute(

                    numeric

                )

            )

            clustering = (

                ClusteringOutlierDetector.compute(

                    numeric

                )

            )

            ensemble = (

                EnsembleOutlierDetector.compute(

                    numeric

                )

            )

            multivariate = (

                MultivariateOutlierDetector.compute(

                    numeric

                )

            )

        # ============================================
        # Résultat
        # ============================================

        report = ReportResult(

            report_name="Outlier Detection Report",

            report_type="Outlier Analysis",

            title="Outlier Analysis Report",

            summary=(

                "Automatic report generated "

                "by EMIDAF."

            ),

            statistics={

                "statistical":

                    statistical,

                "distance":

                    distance,

                "density":

                    density,

                "clustering":

                    clustering,

                "ensemble":

                    ensemble,

                "multivariate":

                    multivariate

            }

        )

        report.add_section(

            "Statistical Detection"

        )

        report.add_section(

            "Distance Detection"

        )

        report.add_section(

            "Density Detection"

        )

        report.add_section(

            "Clustering Detection"

        )

        report.add_section(

            "Ensemble Detection"

        )

        report.add_section(

            "Multivariate Detection"

        )

        return report

    @staticmethod
    def summary(
        dataframe: pd.DataFrame,
        target: str | None = None,
    ):

        return OutlierReport.generate(

            dataframe,

            target

        ).summary()

    @staticmethod
    def statistics(
        dataframe: pd.DataFrame,
        target: str | None = None,
    ):

        return OutlierReport.generate(

            dataframe,

            target

        ).statistics

    @staticmethod
    def export(
        dataframe: pd.DataFrame,
        target: str | None = None,
    ):

        return OutlierReport.generate(

            dataframe,

            target

        )