import numpy as np
import pandas as pd

from emidaf_core.exaie.aggregation import (
    FeatureImportanceAggregator,
)


def test_original_numeric_feature():

    result = (
        FeatureImportanceAggregator
        .original_feature(
            "numeric__motivation",
            [
                "motivation",
                "stress",
            ],
        )
    )

    assert result == "motivation"


def test_original_categorical_feature():

    result = (
        FeatureImportanceAggregator
        .original_feature(
            "categorical__region_Dakar",
            [
                "region",
                "type_ecole",
            ],
        )
    )

    assert result == "region"


def test_longest_original_name_is_used():

    result = (
        FeatureImportanceAggregator
        .original_feature(
            "categorical__niveau_etude_College",
            [
                "niveau",
                "niveau_etude",
            ],
        )
    )

    assert result == "niveau_etude"


def test_modality_with_underscore():

    result = (
        FeatureImportanceAggregator
        .original_feature(
            "categorical__region_Saint_Louis",
            [
                "region",
            ],
        )
    )

    assert result == "region"


def test_global_importance_aggregation():

    table = pd.DataFrame(
        {
            "feature": [
                "numeric__motivation",
                "categorical__region_Dakar",
                "categorical__region_Thies",
                "numeric__stress",
            ],
            "importance": [
                1.2,
                0.3,
                0.2,
                0.8,
            ],
        }
    )

    result = (
        FeatureImportanceAggregator
        .global_importance(
            table,
            original_features=[
                "motivation",
                "region",
                "stress",
            ],
        )
    )

    values = dict(
        zip(
            result["feature"],
            result["importance"],
        )
    )

    assert np.isclose(
        values["motivation"],
        1.2,
    )

    assert np.isclose(
        values["region"],
        0.5,
    )

    assert np.isclose(
        values["stress"],
        0.8,
    )


def test_global_importance_preserves_mass():

    table = pd.DataFrame(
        {
            "feature": [
                "categorical__region_Dakar",
                "categorical__region_Thies",
                "numeric__stress",
            ],
            "importance": [
                0.3,
                0.2,
                0.8,
            ],
        }
    )

    result = (
        FeatureImportanceAggregator
        .global_importance(
            table,
            original_features=[
                "region",
                "stress",
            ],
        )
    )

    assert np.isclose(
        table["importance"].sum(),
        result["importance"].sum(),
    )

    assert np.isclose(
        result[
            "importance_share"
        ].sum(),
        1.0,
    )


def test_shap_importance_aggregation():

    result = (
        FeatureImportanceAggregator
        .shap_importance(
            {
                "numeric__motivation":
                    0.9,
                "categorical__region_Dakar":
                    0.4,
                "categorical__region_Thies":
                    0.25,
            },
            original_features=[
                "motivation",
                "region",
            ],
        )
    )

    values = dict(
        zip(
            result["feature"],
            result["importance"],
        )
    )

    assert np.isclose(
        values["region"],
        0.65,
    )

    assert np.isclose(
        values["motivation"],
        0.9,
    )


def test_local_contributions_preserve_sign():

    table = pd.DataFrame(
        {
            "feature": [
                "categorical__region_Dakar",
                "categorical__region_Thies",
                "numeric__stress",
            ],
            "contribution": [
                0.30,
                -0.10,
                -0.50,
            ],
        }
    )

    result = (
        FeatureImportanceAggregator
        .local_contributions(
            table,
            original_features=[
                "region",
                "stress",
            ],
        )
    )

    values = dict(
        zip(
            result["feature"],
            result["contribution"],
        )
    )

    assert np.isclose(
        values["region"],
        0.20,
    )

    assert np.isclose(
        values["stress"],
        -0.50,
    )


def test_unknown_transformed_feature_is_not_invented():

    name = "variable_17"

    result = (
        FeatureImportanceAggregator
        .original_feature(
            name,
            [
                "motivation",
                "stress",
            ],
        )
    )

    assert result == name


def test_shap_global_aggregates_signed_values_before_absolute_mean():

    # Deux modalités provenant de la même variable.
    #
    # Observation 1 :
    # +1.0 + (-1.0) = 0
    #
    # Observation 2 :
    # +2.0 + (-1.0) = 1
    #
    # Importance correcte :
    # mean(|0|, |1|) = 0.5
    #
    # Une somme naïve des mean(abs(.))
    # donnerait 2.5 et serait incorrecte.

    shap_values = np.array(
        [
            [1.0, -1.0],
            [2.0, -1.0],
        ]
    )

    result = (
        FeatureImportanceAggregator
        .shap_global_from_values(
            shap_values,
            transformed_features=[
                "categorical__region_Dakar",
                "categorical__region_Thies",
            ],
            original_features=[
                "region",
            ],
        )
    )

    assert len(result) == 1

    assert (
        result.iloc[0]["feature"]
        == "region"
    )

    assert np.isclose(
        result.iloc[0]["importance"],
        0.5,
    )

    assert np.isclose(
        result.iloc[0]["importance_share"],
        1.0,
    )


def test_shap_global_numeric_feature_is_preserved():

    shap_values = np.array(
        [
            [1.0, -2.0],
            [-1.0, 4.0],
        ]
    )

    result = (
        FeatureImportanceAggregator
        .shap_global_from_values(
            shap_values,
            transformed_features=[
                "numeric__motivation",
                "numeric__stress",
            ],
            original_features=[
                "motivation",
                "stress",
            ],
        )
    )

    values = dict(
        zip(
            result["feature"],
            result["importance"],
        )
    )

    assert np.isclose(
        values["motivation"],
        1.0,
    )

    assert np.isclose(
        values["stress"],
        3.0,
    )


def test_shap_global_multiclass_signed_aggregation():

    shap_values = np.array(
        [
            [
                [1.0, -1.0],
                [-1.0, 1.0],
            ],
            [
                [2.0, -2.0],
                [-1.0, 1.0],
            ],
        ]
    )

    result = (
        FeatureImportanceAggregator
        .shap_global_from_values(
            shap_values,
            transformed_features=[
                "categorical__region_Dakar",
                "categorical__region_Thies",
            ],
            original_features=[
                "region",
            ],
        )
    )

    # Observation 1 :
    # [0, 0]
    #
    # Observation 2 :
    # [1, -1]
    #
    # mean(abs(.)) = 0.5

    assert np.isclose(
        result.iloc[0]["importance"],
        0.5,
    )
