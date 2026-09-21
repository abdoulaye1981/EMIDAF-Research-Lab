import pandas as pd
import pytest

from sklearn.preprocessing import StandardScaler

from emidaf_core.preprocessing.dimensionality import (
    UMAPReduction,
)


def _scaled_dataframe():
    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0, 1.1, 0.9,
                5.0, 5.2, 4.8,
                9.0, 9.1, 8.9,
            ],
            "x2": [
                1.0, 0.9, 1.1,
                5.0, 4.9, 5.1,
                9.0, 8.9, 9.1,
            ],
            "x3": [
                0.9, 1.0, 1.1,
                4.9, 5.1, 5.0,
                8.8, 9.0, 9.2,
            ],
        }
    )

    return pd.DataFrame(
        StandardScaler().fit_transform(
            dataframe
        ),
        columns=dataframe.columns,
        index=dataframe.index,
    )


def test_umap_fit_transform_returns_dataframe():
    dataframe = _scaled_dataframe()

    model = UMAPReduction(
        n_components=2,
        n_neighbors=3,
        min_dist=0.1,
        random_state=42,
    )

    result = model.fit_transform(
        dataframe
    )

    assert model.fitted is True
    assert isinstance(
        result,
        pd.DataFrame,
    )

    assert result.shape == (
        len(dataframe),
        2,
    )

    assert result.columns.tolist() == [
        "UMAP1",
        "UMAP2",
    ]

    assert result.index.equals(
        dataframe.index
    )


def test_umap_transform_after_fit():
    dataframe = _scaled_dataframe()

    model = UMAPReduction(
        n_components=2,
        n_neighbors=3,
        min_dist=0.1,
        random_state=42,
    )

    model.fit(
        dataframe
    )

    result = model.transform(
        dataframe
    )

    assert result.shape == (
        len(dataframe),
        2,
    )

    assert result.columns.tolist() == [
        "UMAP1",
        "UMAP2",
    ]


@pytest.mark.parametrize(
    "kwargs,expected_message",
    [
        (
            {
                "n_components": 1,
            },
            "n_components",
        ),
        (
            {
                "n_neighbors": 1,
            },
            "n_neighbors",
        ),
        (
            {
                "min_dist": -0.1,
            },
            "min_dist",
        ),
    ],
)
def test_umap_rejects_invalid_parameters(
    kwargs,
    expected_message,
):
    with pytest.raises(
        ValueError,
        match=expected_message,
    ):
        UMAPReduction(
            **kwargs
        )
