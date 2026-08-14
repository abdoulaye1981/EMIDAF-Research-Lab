"""
=========================================================
EMIDAF Framework
Estimator
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe de base de tous les estimateurs statistiques.

Exemples
---------
MeanEstimator
VarianceEstimator
MaximumLikelihoodEstimator
BayesianEstimator
BootstrapEstimator
=========================================================
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

import numpy as np
import pandas as pd

from .base_statistic import BaseStatistic


class Estimator(BaseStatistic):
    """
    Classe abstraite des estimateurs statistiques.

    Cette classe fournit les fonctionnalités communes
    à tous les estimateurs EMIDAF.
    """

    category: str = "Estimator"

    # =====================================================
    # API
    # =====================================================

    @classmethod
    @abstractmethod
    def compute(
        cls,
        values: Any,
        **kwargs,
    ):
        """
        Calcule un estimateur.

        Returns
        -------
        float | dict
        """

        raise NotImplementedError

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def validate_sample(
        cls,
        values: Any,
    ) -> pd.Series:
        """
        Valide un échantillon.
        """

        values = cls.validate(values)

        if cls.is_empty(values):

            raise ValueError(
                "Empty sample."
            )

        return values

    # =====================================================
    # Confidence Interval
    # =====================================================

    @classmethod
    def confidence_interval(
        cls,
        estimate: float,
        standard_error: float,
        z: float = 1.96,
    ) -> tuple[float, float]:
        """
        Intervalle de confiance.

        Parameters
        ----------
        estimate :
            Estimateur.

        standard_error :
            Erreur standard.

        z :
            Quantile de la loi normale.

        Returns
        -------
        tuple
        """

        lower = estimate - z * standard_error

        upper = estimate + z * standard_error

        return (

            float(lower),

            float(upper),

        )

    # =====================================================
    # Standard Error
    # =====================================================

    @classmethod
    def standard_error(
        cls,
        values: Any,
    ) -> float:
        """
        Erreur standard.
        """

        values = cls.validate_sample(values)

        std = values.std(ddof=1)

        n = len(values)

        return float(

            std / np.sqrt(n)

        )

    # =====================================================
    # Estimate Summary
    # =====================================================

    @classmethod
    def summary(
        cls,
        values: Any,
        estimate: float,
    ) -> dict:
        """
        Résumé d'un estimateur.
        """

        values = cls.validate_sample(values)

        se = cls.standard_error(values)

        ci = cls.confidence_interval(

            estimate,

            se

        )

        return {

            "estimator": cls.name,

            "estimate": float(estimate),

            "standard_error": se,

            "confidence_interval": {

                "lower": ci[0],

                "upper": ci[1]

            },

            "sample_size": len(values)

        }

    # =====================================================
    # Safe Compute
    # =====================================================

    @classmethod
    def safe_compute(
        cls,
        values,
        default=np.nan,
        **kwargs,
    ):
        """
        Calcul sécurisé.
        """

        try:

            return cls.compute(

                values,

                **kwargs

            )

        except Exception:

            return default

    # =====================================================
    # Information
    # =====================================================

    @classmethod
    def info(cls) -> dict:
        """
        Informations sur l'estimateur.
        """

        return {

            "name": cls.name,

            "description": cls.description,

            "category": cls.category,

            "version": cls.version

        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"category='{self.category}')"

        )

    def __str__(self):

        return self.__repr__()