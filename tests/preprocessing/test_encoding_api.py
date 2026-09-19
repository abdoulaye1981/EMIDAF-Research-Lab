from __future__ import annotations

import pandas as pd

from emidaf_core.preprocessing.encoding import (
    Encoder,
    Encoding,
)


def test_onehot_encode():

    dataframe = pd.DataFrame(
        {
            "city": [
                "Dakar",
                "Thiès",
                "Dakar",
            ],
            "age": [
                20,
                21,
                22,
            ],
        }
    )

    result, encoder = Encoding.onehot_encode(
        dataframe,
        columns=["city"],
    )

    assert encoder is not None
    assert "city" not in result.columns
    assert "age" in result.columns

    assert any(
        column.startswith("city_")
        for column in result.columns
    )


def test_onehot_preserves_index():

    dataframe = pd.DataFrame(
        {
            "city": [
                "Dakar",
                "Thiès",
            ]
        },
        index=["a", "b"],
    )

    result, _ = Encoding.onehot_encode(
        dataframe
    )

    assert result.index.tolist() == [
        "a",
        "b",
    ]


def test_onehot_handles_missing_values():

    dataframe = pd.DataFrame(
        {
            "city": [
                "Dakar",
                None,
            ]
        }
    )

    result, _ = Encoding.onehot_encode(
        dataframe
    )

    assert result.isna().sum().sum() == 0


def test_encoder_service_exposes_onehot():

    assert callable(
        Encoder.onehot
    )

    dataframe = pd.DataFrame(
        {
            "city": [
                "Dakar",
                "Thiès",
            ]
        }
    )

    direct, _ = Encoding.onehot_encode(
        dataframe
    )

    facade, _ = Encoder.onehot(
        dataframe
    )

    pd.testing.assert_frame_equal(
        facade,
        direct,
    )
