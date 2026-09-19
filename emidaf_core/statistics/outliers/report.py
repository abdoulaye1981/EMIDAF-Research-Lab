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

import numpy as np
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

        errors = {}

        numeric = dataframe.select_dtypes(
            include="number"
        )

        # ============================================
        # Validation globale
        # ============================================

        if target is not None:

            if target not in dataframe.columns:
                raise ValueError(
                    f"Unknown target column: {target}"
                )

        if not numeric.empty:

            numeric_values = numeric.to_numpy(
                dtype=float
            )

            if np.isinf(
                numeric_values
            ).any():

                raise ValueError(
                    "Infinite values are not supported "
                    "in outlier reports."
                )

        # ============================================
        # Univarié
        # ============================================

        for column in numeric.columns:

            try:

                statistical[column] = (
                    StatisticalOutlierDetector.compute(
                        numeric[column]
                    )
                )

            except ValueError as exc:

                statistical[column] = {}

                errors[
                    f"statistical.{column}"
                ] = str(exc)

        # ============================================
        # Multivarié
        # ============================================

        if len(numeric.columns) > 1:

            try:

                distance = (
                    DistanceOutlierDetector.compute(
                        numeric,
                        target
                    )
                )

            except ValueError as exc:

                errors["distance"] = str(exc)

            try:

                density = (
                    DensityOutlierDetector.compute(
                        numeric
                    )
                )

            except ValueError as exc:

                errors["density"] = str(exc)

            try:

                clustering = (
                    ClusteringOutlierDetector.compute(
                        numeric
                    )
                )

            except ValueError as exc:

                errors["clustering"] = str(exc)

            try:

                ensemble = (
                    EnsembleOutlierDetector.compute(
                        numeric
                    )
                )

            except ValueError as exc:

                errors["ensemble"] = str(exc)

            try:

                multivariate = (
                    MultivariateOutlierDetector.compute(
                        numeric
                    )
                )

            except ValueError as exc:

                errors["multivariate"] = str(exc)

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

        report.metadata[
            "errors"
        ] = errors

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

        ).summary_info()

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
