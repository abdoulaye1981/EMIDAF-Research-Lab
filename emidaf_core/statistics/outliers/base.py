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

    method_family = ""

    score_type = ""

    score_direction = "none"

    scaling_sensitive = False

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
        """
        Construit un résultat standardisé de détection
        des valeurs aberrantes.

        Deux contextes sont supportés :

        1. Détection univariée
           `values` contient les observations numériques
           sous forme de Series ou structure assimilable.

        2. Détection multivariée
           `values` peut être un pandas.Index représentant
           directement les identifiants des observations.

        Cette distinction est importante afin de préserver
        les index pandas personnalisés.
        """

        # =================================================
        # CAS MULTIVARIÉ : values EST UN INDEX
        # =================================================

        if isinstance(
            values,
            pd.Index,
        ):
            observation_index = values.copy()

            mask = observation_index.isin(
                indices
            )

            variable = ""

            # Ici les "values" sont en réalité les
            # identifiants des observations.
            outlier_values = list(
                observation_index[mask]
            )

        # =================================================
        # CAS UNIVARIÉ : values CONTIENT LES MESURES
        # =================================================

        else:
            if isinstance(
                values,
                pd.Series,
            ):
                series = values.copy()

            else:
                series = pd.Series(
                    values
                )

            observation_index = (
                series.index
            )

            mask = observation_index.isin(
                indices
            )

            variable = (
                series.name or ""
            )

            outlier_values = (
                series.loc[mask]
                .tolist()
            )

        # =================================================
        # NORMALISATION DES INDICES
        # =================================================

        outlier_indices = list(
            indices
        )

        inlier_indices = list(
            observation_index[~mask]
        )

        # =================================================
        # RESULTAT
        # =================================================

        result = OutlierResult(
            method=cls.name,
            variable=variable,
            threshold=threshold,
            total_observations=len(
                observation_index
            ),
            outlier_count=len(
                outlier_indices
            ),
            inlier_count=len(
                inlier_indices
            ),
            outlier_indices=outlier_indices,
            inlier_indices=inlier_indices,
            outlier_values=outlier_values,
            scores=(
                []
                if scores is None
                else list(scores)
            ),
            labels=(
                []
                if labels is None
                else list(labels)
            ),
            score_type=cls.score_type,

            score_direction=cls.score_direction,

            method_family=cls.method_family,

            scaling_sensitive=cls.scaling_sensitive,

            parameters=(
                {}
                if parameters is None
                else parameters
            ),
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
