from __future__ import annotations

import pandas as pd

from emidaf_core.statistics.outliers.ensemble import (
    EnsembleOutlierDetector,
)

from emidaf_core.statistics.outliers.multivariate import (
    MultivariateOutlierDetector,
)


def make_dataframe():

    return pd.DataFrame(
        {
            "x1": [
                0.0,
                0.1,
                -0.1,
                0.2,
                0.0,
                0.1,
                -0.1,
                0.2,
                5.0,
                5.2,
                5.1,
                5.3,
                10.0,
            ],
            "x2": [
                0.0,
                -0.1,
                0.1,
                0.2,
                0.1,
                0.0,
                -0.2,
                0.1,
                5.0,
                5.1,
                5.2,
                5.3,
                10.0,
            ],
        }
    )


def test_ensemble_service_works_without_pyod():

    dataframe = make_dataframe()

    result = EnsembleOutlierDetector.compute(
        dataframe
    )

    assert "isolation_forest" in result
    assert "one_class_svm" in result
    assert "elliptic_envelope" in result

    assert "hbos" not in result
    assert "abod" not in result
    assert "ecod" not in result
    assert "copod" not in result


def test_multivariate_service_works_without_pyod():

    dataframe = make_dataframe()

    result = MultivariateOutlierDetector.compute(
        dataframe
    )

    assert "pca" in result
    assert "robust_pca" in result
    assert "minimum_covariance" in result

    assert "feature_bagging" not in result
