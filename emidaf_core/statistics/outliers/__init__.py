"""
=========================================================
EMIDAF Framework
Outlier Detection Public API
=========================================================

API publique du sous-système de détection et de traitement
des valeurs aberrantes.
"""

from .base import BaseOutlierDetector

from .statistical import (
    HampelFilter,
    IQR,
    ModifiedZScore,
    Percentile,
    StatisticalOutlierDetector,
    ThreeSigma,
    TukeyFence,
    ZScore,
)

from .distance import (
    CookDistance,
    DistanceOutlierDetector,
    Leverage,
    Mahalanobis,
    RobustMahalanobis,
)

from .density import (
    DBSCANOutlier,
    DensityOutlierDetector,
    LOF,
    OPTICSOutlier,
)

from .ensemble import (
    ABODDetector,
    COPODDetector,
    ECODDetector,
    EllipticEnvelopeDetector,
    EnsembleOutlierDetector,
    HBOSDetector,
    IsolationForestDetector,
    OneClassSVMDetector,
)

from .clustering import (
    BirchOutlier,
    ClusteringOutlierDetector,
    GaussianMixtureOutlier,
    KMeansOutlier,
    MiniBatchKMeansOutlier,
)

from .multivariate import (
    FeatureBaggingOutlier,
    MinimumCovarianceDeterminant,
    MultivariateOutlierDetector,
    PCAOutlier,
    RobustPCAOutlier,
)

from .treatment import (
    AdaptiveTreatment,
    Capping,
    Flooring,
    MeanReplacement,
    MedianReplacement,
    OutlierTreatment,
    QuantileCapping,
    RemoveOutliers,
    Winsorization,
)

from .report import OutlierReport


__all__ = [
    # Base
    "BaseOutlierDetector",

    # Statistical
    "ZScore",
    "ModifiedZScore",
    "IQR",
    "TukeyFence",
    "Percentile",
    "ThreeSigma",
    "HampelFilter",
    "StatisticalOutlierDetector",

    # Distance / influence
    "Mahalanobis",
    "RobustMahalanobis",
    "CookDistance",
    "Leverage",
    "DistanceOutlierDetector",

    # Density
    "LOF",
    "DBSCANOutlier",
    "OPTICSOutlier",
    "DensityOutlierDetector",

    # Ensemble
    "IsolationForestDetector",
    "OneClassSVMDetector",
    "EllipticEnvelopeDetector",
    "HBOSDetector",
    "ABODDetector",
    "ECODDetector",
    "COPODDetector",
    "EnsembleOutlierDetector",

    # Clustering
    "KMeansOutlier",
    "MiniBatchKMeansOutlier",
    "BirchOutlier",
    "GaussianMixtureOutlier",
    "ClusteringOutlierDetector",

    # Multivariate
    "PCAOutlier",
    "RobustPCAOutlier",
    "FeatureBaggingOutlier",
    "MinimumCovarianceDeterminant",
    "MultivariateOutlierDetector",

    # Treatment
    "RemoveOutliers",
    "Winsorization",
    "Capping",
    "Flooring",
    "MeanReplacement",
    "MedianReplacement",
    "QuantileCapping",
    "AdaptiveTreatment",
    "OutlierTreatment",

    # Reporting
    "OutlierReport",
]
