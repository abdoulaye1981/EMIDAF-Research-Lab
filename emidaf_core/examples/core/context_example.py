import pandas as pd

from emidaf_core.core.base_context import BaseContext


df = pd.DataFrame(

    {

        "Age": [20, 25, 30],

        "Salaire": [1000, 1500, 2000]

    }

)

context = BaseContext(df)

context.put_cache("mean_age", 25)

context.add_result("summary", {"rows": context.rows})

print(context.to_dict())