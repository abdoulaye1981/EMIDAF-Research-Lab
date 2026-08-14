"""
=========================================================
EMIDAF Framework
Base Outlier Detector
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd

from ...common.results import OutlierResult
from ..descriptive.validator import StatisticsValidator


class BaseOutlierDetector(ABC):
    """
    Classe mère de tous les détecteurs d'anomalies.
    """

    name = ""

    category = "Outlier Detection"

    @classmethod
    def validate(
        cls,
        values,
    ):

        return StatisticsValidator.require_numeric(

            values

        )

    @classmethod
    def build_result(

        cls,

        values,

        indices,

        scores=None,

        labels=None,

        threshold=None,

        parameters=None,

    ) -> OutlierResult:

        values = pd.Series(values)

        mask = values.index.isin(indices)

        outlier_values = values.loc[mask]

        result = OutlierResult(

            method=cls.name,

            variable=values.name or "",

            threshold=threshold,

            total_observations=len(values),

            outlier_count=len(indices),

            inlier_count=len(values)-len(indices),

            outlier_indices=list(indices),

            inlier_indices=list(

                values.index[~mask]

            ),

            outlier_values=outlier_values.tolist(),

            scores=[] if scores is None else list(scores),

            labels=[] if labels is None else list(labels),

            parameters={} if parameters is None else parameters

        )

        result.compute_percentages()

        return result

    @classmethod
    @abstractmethod
    def detect(

        cls,

        values,

        **kwargs,

    ) -> OutlierResult:

        raise NotImplementedError