from emidaf_core.eaie.blocks import (
    FeatureBlocks,
    resolve_feature_blocks,
)


def test_feature_blocks_valid_configuration():

    predictors = [
        "age",
        "motivation",
        "parent_support",
        "feedback",
        "school_type",
    ]

    blocks = {
        "Élève": [
            "age",
            "motivation",
        ],
        "Famille": [
            "parent_support",
        ],
        "Pédagogie": [
            "feedback",
        ],
        "Institution": [
            "school_type",
        ],
    }

    result = FeatureBlocks.resolve(
        predictors=predictors,
        blocks=blocks,
        target="score",
        protected=[
            "id_eleve",
        ],
        require_all=True,
    )

    assert result.valid is True
    assert result.conflicts == []

    assert result.assigned == predictors
    assert result.unassigned == []


def test_feature_blocks_builds_cumulative_sets():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
            "x3",
            "x4",
        ],
        blocks={
            "A": [
                "x1",
            ],
            "B": [
                "x2",
            ],
            "C": [
                "x3",
                "x4",
            ],
        },
        require_all=True,
    )

    assert result.cumulative == {
        "A": [
            "x1",
        ],
        "B": [
            "x1",
            "x2",
        ],
        "C": [
            "x1",
            "x2",
            "x3",
            "x4",
        ],
    }


def test_feature_blocks_rejects_duplicate_variable():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
        ],
        blocks={
            "A": [
                "x1",
            ],
            "B": [
                "x1",
                "x2",
            ],
        },
    )

    assert result.valid is False

    assert any(
        "plusieurs blocs"
        in conflict
        for conflict
        in result.conflicts
    )


def test_feature_blocks_rejects_unknown_variable():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
        ],
        blocks={
            "A": [
                "x1",
                "unknown",
            ],
        },
    )

    assert result.valid is False

    assert any(
        "n'est pas un prédicteur admissible"
        in conflict
        for conflict
        in result.conflicts
    )


def test_feature_blocks_rejects_target():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
        ],
        blocks={
            "A": [
                "x1",
                "target",
            ],
        },
        target="target",
    )

    assert result.valid is False

    assert any(
        "cible"
        in conflict.lower()
        for conflict
        in result.conflicts
    )


def test_feature_blocks_rejects_protected_variable():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
        ],
        blocks={
            "A": [
                "x1",
                "id_eleve",
            ],
        },
        protected=[
            "id_eleve",
        ],
    )

    assert result.valid is False

    assert any(
        "protégée"
        in conflict
        for conflict
        in result.conflicts
    )


def test_feature_blocks_tracks_unassigned():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
            "x3",
        ],
        blocks={
            "A": [
                "x1",
            ],
            "B": [
                "x2",
            ],
        },
        require_all=False,
    )

    assert result.valid is True
    assert result.unassigned == [
        "x3",
    ]


def test_feature_blocks_can_require_all_predictors():

    result = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
            "x3",
        ],
        blocks={
            "A": [
                "x1",
            ],
            "B": [
                "x2",
            ],
        },
        require_all=True,
    )

    assert result.valid is False

    assert any(
        "aucun bloc"
        in conflict
        for conflict
        in result.conflicts
    )


def test_feature_blocks_preserves_predictor_order():

    result = FeatureBlocks.resolve(
        predictors=[
            "z",
            "a",
            "m",
        ],
        blocks={
            "Bloc": [
                "a",
                "m",
                "z",
            ],
        },
        require_all=True,
    )

    assert result.assigned == [
        "z",
        "a",
        "m",
    ]


def test_feature_blocks_to_dict():

    result = resolve_feature_blocks(
        predictors=[
            "x1",
            "x2",
        ],
        blocks={
            "A": [
                "x1",
            ],
            "B": [
                "x2",
            ],
        },
        target="y",
        require_all=True,
    )

    payload = result.to_dict()

    assert payload[
        "valid"
    ] is True

    assert payload[
        "target"
    ] == "y"

    assert payload[
        "cumulative"
    ]["B"] == [
        "x1",
        "x2",
    ]
