"""
=========================================================
EMIDAF Framework
Ensemble Outlier Detection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Détecteurs avancés d'anomalies.

Contient

- Isolation Forest
- One-Class SVM
- Elliptic Envelope
- HBOS
- ABOD
- ECOD
- COPOD

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest

from sklearn.svm import OneClassSVM

from sklearn.covariance import EllipticEnvelope

from .base import BaseOutlierDetector


# ==========================================================
# ISOLATION FOREST
# ==========================================================

class IsolationForestDetector(BaseOutlierDetector):

    name = "Isolation Forest"

    method_family = "ensemble"

    score_type = "negative_decision_function"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination="auto",

        random_state=42,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = IsolationForest(

            contamination=contamination,

            random_state=random_state

        )

        labels = model.fit_predict(

            dataframe

        )

        # Convention EMIDAF :
        # score élevé = observation plus atypique.
        #
        # decision_function() de scikit-learn utilise
        # l'orientation inverse : les valeurs faibles
        # correspondent aux observations anormales.
        scores = -model.decision_function(

            dataframe

        )

        indices = dataframe.index[

            labels == -1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels,

            parameters={

                "contamination": contamination

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# ONE CLASS SVM
# ==========================================================

class OneClassSVMDetector(BaseOutlierDetector):

    name = "One-Class SVM"

    method_family = "boundary"

    score_type = "negative_decision_function"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        nu=0.05,

        kernel="rbf",

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = OneClassSVM(

            nu=nu,

            kernel=kernel

        )

        labels = model.fit_predict(

            dataframe

        )

        # Convention EMIDAF :
        # score élevé = observation plus atypique.
        #
        # OneClassSVM.decision_function() produit
        # l'orientation inverse.
        scores = -model.decision_function(

            dataframe

        ).flatten()

        indices = dataframe.index[

            labels == -1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels,

            parameters={

                "nu": nu,

                "kernel": kernel

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# ELLIPTIC ENVELOPE
# ==========================================================

class EllipticEnvelopeDetector(BaseOutlierDetector):

    name = "Elliptic Envelope"

    method_family = "covariance"

    score_type = "negative_decision_function"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = EllipticEnvelope(

            contamination=contamination

        )

        labels = model.fit_predict(

            dataframe

        )

        # Convention EMIDAF :
        # score élevé = observation plus atypique.
        #
        # decision_function() de scikit-learn utilise
        # l'orientation inverse : les valeurs faibles
        # correspondent aux observations anormales.
        scores = -model.decision_function(

            dataframe

        )

        indices = dataframe.index[

            labels == -1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels,

            parameters={

                "contamination": contamination

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# HBOS
# ==========================================================

class HBOSDetector(BaseOutlierDetector):

    """
    Histogram Based Outlier Score.

    Version EMIDAF 1.0 :
    Wrapper pour PyOD.

    Nécessite :
        pip install pyod
    """

    name = "HBOS"

    method_family = "histogram"

    score_type = "hbos_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        try:
            from pyod.models.hbos import HBOS
        except ModuleNotFoundError as exc:
            raise ImportError(
                "PyOD is required for HBOSDetector. "
                "Install it with: pip install pyod"
            ) from exc

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = HBOS(

            contamination=contamination

        )

        model.fit(dataframe)

        labels = model.labels_

        scores = model.decision_scores_

        indices = dataframe.index[

            labels == 1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# ABOD
# ==========================================================

class ABODDetector(BaseOutlierDetector):

    """
    Angle Based Outlier Detection.

    Wrapper PyOD.
    """

    name = "ABOD"

    method_family = "angle"

    score_type = "abod_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        try:
            from pyod.models.abod import ABOD
        except ModuleNotFoundError as exc:
            raise ImportError(
                "PyOD is required for ABODDetector. "
                "Install it with: pip install pyod"
            ) from exc

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = ABOD(

            contamination=contamination

        )

        model.fit(dataframe)

        labels = model.labels_

        scores = model.decision_scores_

        indices = dataframe.index[

            labels == 1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# ECOD
# ==========================================================

class ECODDetector(BaseOutlierDetector):

    """
    Empirical Cumulative Distribution.

    Wrapper PyOD.
    """

    name = "ECOD"

    method_family = "distribution"

    score_type = "ecod_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        try:
            from pyod.models.ecod import ECOD
        except ModuleNotFoundError as exc:
            raise ImportError(
                "PyOD is required for ECODDetector. "
                "Install it with: pip install pyod"
            ) from exc

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = ECOD(

            contamination=contamination

        )

        model.fit(dataframe)

        labels = model.labels_

        scores = model.decision_scores_

        indices = dataframe.index[

            labels == 1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# COPOD
# ==========================================================

class COPODDetector(BaseOutlierDetector):

    """
    Copula Based Outlier Detection.

    Wrapper PyOD.
    """

    name = "COPOD"

    method_family = "copula"

    score_type = "copod_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        try:
            from pyod.models.copod import COPOD
        except ModuleNotFoundError as exc:
            raise ImportError(
                "PyOD is required for COPODDetector. "
                "Install it with: pip install pyod"
            ) from exc

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = COPOD(

            contamination=contamination

        )

        model.fit(dataframe)

        labels = model.labels_

        scores = model.decision_scores_

        indices = dataframe.index[

            labels == 1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# SERVICE
# ==========================================================

class EnsembleOutlierDetector:
    """
    Lance tous les détecteurs avancés.
    """

    @staticmethod
    def compute(
        dataframe,
    ):

        results = {
            "isolation_forest":
                IsolationForestDetector.detect(
                    dataframe
                ),

            "one_class_svm":
                OneClassSVMDetector.detect(
                    dataframe
                ),

            "elliptic_envelope":
                EllipticEnvelopeDetector.detect(
                    dataframe
                ),
        }

        optional_detectors = {
            "hbos": HBOSDetector,
            "abod": ABODDetector,
            "ecod": ECODDetector,
            "copod": COPODDetector,
        }

        for name, detector in optional_detectors.items():

            try:
                results[name] = detector.detect(
                    dataframe
                )

            except ImportError:
                continue

        return results
