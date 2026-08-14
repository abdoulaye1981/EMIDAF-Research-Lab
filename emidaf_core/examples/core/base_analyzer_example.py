import pandas as pd

from emidaf_core.core.base_context import BaseContext
from emidaf_core.core.base_analyzer import BaseAnalyzer


class RowAnalyzer(BaseAnalyzer):

    name = "Rows"

    description = "Nombre de lignes"

    def analyze(self, context):

        return context.rows


df = pd.DataFrame(

    {

        "A": [1, 2, 3]

    }

)

context = BaseContext(df)

result = RowAnalyzer().execute(

    context

)

print(result.to_dict())