"""
=========================================================
EMIDAF Framework
Multivariate Descriptive Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.spatial.distance import (
    mahalanobis,
    euclidean,
    cityblock,
    minkowski,
    canberra,
    cosine
)

from .base import (
    BaseStatistic,
    StatisticResult
)

# ==========================================================
# COVARIANCE
# ==========================================================

class Covariance(

    BaseStatistic

):

    name="Covariance"

    def compute(

        self,

        x,

        y,

    ):

        value=np.cov(

            x,

            y,

            ddof=1

        )[0,1]

        return StatisticResult(

            statistic="Covariance",

            value=float(value)

        )

# ==========================================================
# COVARIANCE
# ==========================================================

class Covariance(

    BaseStatistic

):

    name="Covariance"

    def compute(

        self,

        x,

        y,

    ):

        value=np.cov(

            x,

            y,

            ddof=1

        )[0,1]

        return StatisticResult(

            statistic="Covariance",

            value=float(value)

        )

# ==========================================================
# CORRELATION
# ==========================================================

class Correlation(

    BaseStatistic

):

    name="Correlation"

    def compute(

        self,

        x,

        y,

    ):

        value=np.corrcoef(

            x,

            y

        )[0,1]

        return StatisticResult(

            statistic="Correlation",

            value=float(value)

        )

# ==========================================================
# CORRELATION MATRIX
# ==========================================================

class CorrelationMatrix(

    BaseStatistic

):

    name="Correlation Matrix"

    def compute(

        self,

        X,

    ):

        if isinstance(

            X,

            pd.DataFrame

        ):

            matrix=X.corr()

        else:

            matrix=np.corrcoef(

                X,

                rowvar=False

            )

        return StatisticResult(

            statistic="Correlation Matrix",

            value=matrix

        )
    
# ==========================================================
# CENTROID
# ==========================================================

class Centroid(

    BaseStatistic

):

    name="Centroid"

    def compute(

        self,

        X,

    ):

        center=np.mean(

            X,

            axis=0

        )

        return StatisticResult(

            statistic="Centroid",

            value=center.tolist()

        )

# ==========================================================
# VARIANCE-COVARIANCE MATRIX
# ==========================================================

class VarianceCovarianceMatrix(

    CovarianceMatrix

):

    name="Variance-Covariance Matrix"


# ==========================================================
# DETERMINANT
# ==========================================================

class CovarianceDeterminant(

    BaseStatistic

):

    name="Covariance Determinant"

    def compute(

        self,

        X,

    ):

        matrix=np.cov(

            X,

            rowvar=False

        )

        determinant=np.linalg.det(

            matrix

        )

        return StatisticResult(

            statistic="Covariance Determinant",

            value=float(determinant)

        )

# ==========================================================
# GENERALIZED VARIANCE
# ==========================================================

class GeneralizedVariance(

    BaseStatistic

):

    name="Generalized Variance"

    def compute(

        self,

        X,

    ):

        matrix=np.cov(

            X,

            rowvar=False

        )

        value=np.linalg.det(

            matrix

        )

        return StatisticResult(

            statistic="Generalized Variance",

            value=float(value)

        )

# ==========================================================
# MAHALANOBIS
# ==========================================================

class MahalanobisDistance(

    BaseStatistic

):

    name="Mahalanobis Distance"

    def compute(

        self,

        observation,

        X,

    ):

        covariance=np.cov(

            X,

            rowvar=False

        )

        inverse=np.linalg.inv(

            covariance

        )

        center=np.mean(

            X,

            axis=0

        )

        distance=mahalanobis(

            observation,

            center,

            inverse

        )

        return StatisticResult(

            statistic="Mahalanobis Distance",

            value=float(distance)

        )

# ==========================================================
# EUCLIDEAN
# ==========================================================

class EuclideanDistance(

    BaseStatistic

):

    name="Euclidean Distance"

    def compute(

        self,

        x,

        y,

    ):

        return StatisticResult(

            statistic="Euclidean Distance",

            value=float(

                euclidean(

                    x,

                    y

                )

            )

        )

# ==========================================================
# EUCLIDEAN
# ==========================================================

class EuclideanDistance(

    BaseStatistic

):

    name="Euclidean Distance"

    def compute(

        self,

        x,

        y,

    ):

        return StatisticResult(

            statistic="Euclidean Distance",

            value=float(

                euclidean(

                    x,

                    y

                )

            )

        )

# ==========================================================
# MINKOWSKI
# ==========================================================

class MinkowskiDistance(

    BaseStatistic

):

    name="Minkowski Distance"

    def __init__(

        self,

        p=2,

    ):

        self.p=p

    def compute(

        self,

        x,

        y,

    ):

        return StatisticResult(

            statistic="Minkowski Distance",

            value=float(

                minkowski(

                    x,

                    y,

                    self.p

                )

            )

        )


# ==========================================================
# CANBERRA
# ==========================================================

class CanberraDistance(

    BaseStatistic

):

    name="Canberra Distance"

    def compute(

        self,

        x,

        y,

    ):

        return StatisticResult(

            statistic="Canberra Distance",

            value=float(

                canberra(

                    x,

                    y

                )

            )

        )

# ==========================================================
# COSINE
# ==========================================================

class CosineDistance(

    BaseStatistic

):

    name="Cosine Distance"

    def compute(

        self,

        x,

        y,

    ):

        return StatisticResult(

            statistic="Cosine Distance",

            value=float(

                cosine(

                    x,

                    y

                )

            )

        )

# ==========================================================
# SERVICE
# ==========================================================

class Multivariate:

    registry={

        "covariance":Covariance,

        "covariance_matrix":CovarianceMatrix,

        "correlation":Correlation,

        "correlation_matrix":CorrelationMatrix,

        "centroid":Centroid,

        "variance_covariance":VarianceCovarianceMatrix,

        "determinant":CovarianceDeterminant,

        "generalized_variance":GeneralizedVariance,

        "mahalanobis":MahalanobisDistance,

        "euclidean":EuclideanDistance,

        "manhattan":ManhattanDistance,

        "minkowski":MinkowskiDistance,

        "canberra":CanberraDistance,

        "cosine":CosineDistance

    }

    @classmethod

    def get(

        cls,

        method,

        **kwargs

    ):

        return cls.registry[method](

            **kwargs

        )