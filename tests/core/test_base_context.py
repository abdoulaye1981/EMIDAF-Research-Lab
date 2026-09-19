import pandas as pd
import pytest

from emidaf_core.core.base_context import BaseContext


def create_context():

    df = pd.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [10, 20, 30],
        }
    )

    return BaseContext(df)


def test_context_creation():

    context = create_context()

    assert context.rows == 3
    assert context.columns == 2
    assert context.shape == (3, 2)


def test_column_names():

    context = create_context()

    assert context.column_names == ["A", "B"]


def test_dataframe_is_copied():

    df = pd.DataFrame(
        {
            "A": [1, 2, 3]
        }
    )

    context = BaseContext(df)

    df.loc[0, "A"] = 999

    assert context.dataframe.loc[0, "A"] == 1


def test_original_dataframe():

    context = create_context()

    assert context.original_dataframe.equals(
        context.dataframe
    )


def test_shared_data():

    context = create_context()

    context.put("test", 123)

    assert context.get("test") == 123
    assert context.get("unknown") is None
    assert context.get("unknown", 99) == 99


def test_results():

    context = create_context()

    context.add_result(
        "profile",
        {"rows": 3}
    )

    assert context.get_result("profile") == {"rows": 3}


def test_statistics():

    context = create_context()

    context.set_statistic(
        "mean",
        15
    )

    assert context.get_statistic("mean") == 15


def test_cache():

    context = create_context()

    context.put_cache(
        "test",
        100
    )

    assert context.has_cache("test")
    assert context.get_cache("test") == 100


def test_none_dataframe():

    with pytest.raises(ValueError):

        BaseContext(None)


def test_invalid_dataframe():

    with pytest.raises(TypeError):

        BaseContext([1, 2, 3])
