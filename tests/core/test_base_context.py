import pandas as pd

from emidaf_core.core.base_context import BaseContext


def test_context_creation():

    df = pd.DataFrame({"A": [1, 2, 3]})

    context = BaseContext(df)

    assert context.rows == 3

    assert context.columns == 1


def test_cache():

    df = pd.DataFrame({"A": [1]})

    context = BaseContext(df)

    context.put_cache("mean", 15)

    assert context.get_cache("mean") == 15


def test_shared():

    df = pd.DataFrame({"A": [1]})

    context = BaseContext(df)

    context.put("x", 10)

    assert context.get("x") == 10


def test_results():

    df = pd.DataFrame({"A": [1]})

    context = BaseContext(df)

    context.add_result("summary", {"rows": 1})

    assert context.get_result("summary")["rows"] == 1