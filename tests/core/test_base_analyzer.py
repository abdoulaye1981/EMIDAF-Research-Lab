import pandas as pd

from emidaf_core.core.base_context import BaseContext
from emidaf_core.core.base_analyzer import BaseAnalyzer


class DummyAnalyzer(BaseAnalyzer):

    name = "Dummy"

    def analyze(self, context):

        return {

            "rows": context.rows

        }


def test_execute():

    df = pd.DataFrame(

        {

            "A": [1, 2, 3]

        }

    )

    context = BaseContext(df)

    analyzer = DummyAnalyzer()

    result = analyzer.execute(

        context

    )

    assert result.success

    assert result.get("result")["rows"] == 3