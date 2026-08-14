import pandas as pd

from emidaf_core.core.base_engine import BaseEngine
from emidaf_core.core.base_context import BaseContext
from emidaf_core.core.base_result import BaseResult


class RowEngine(BaseEngine):

    def create_context(self, dataframe):

        return BaseContext(dataframe)

    def run(self, context):

        result = BaseResult()

        result.put("rows", context.rows)

        return result


df = pd.DataFrame(

    {

        "A": [1, 2, 3, 4]

    }

)

engine = RowEngine()

result = engine.execute(df)

print(result.to_dict())