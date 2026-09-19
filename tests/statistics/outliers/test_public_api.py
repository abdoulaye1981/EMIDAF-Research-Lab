from __future__ import annotations

import emidaf_core.statistics.outliers as outliers


def test_core_outlier_public_api():

    expected = [
        "ZScore",
        "ModifiedZScore",
        "IQR",
        "Mahalanobis",
        "RobustMahalanobis",
        "LOF",
        "DBSCANOutlier",
        "OPTICSOutlier",
        "IsolationForestDetector",
        "KMeansOutlier",
        "PCAOutlier",
        "OutlierTreatment",
        "OutlierReport",
    ]

    for name in expected:
        assert hasattr(
            outliers,
            name,
        )


def test_public_api_matches_all():

    for name in outliers.__all__:
        assert hasattr(
            outliers,
            name,
        )


def test_unimplemented_autoencoder_not_public():

    assert (
        "AutoEncoderOutlier"
        not in outliers.__all__
    )


def test_direct_public_imports():

    from emidaf_core.statistics.outliers import (
        IQR,
        LOF,
        Mahalanobis,
        OutlierReport,
        PCAOutlier,
        ZScore,
    )

    assert ZScore is not None
    assert IQR is not None
    assert Mahalanobis is not None
    assert LOF is not None
    assert PCAOutlier is not None
    assert OutlierReport is not None
