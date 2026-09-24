"""
EMIDAF Framework
EAIE - Exploratory Artificial Intelligence Engine
"""

from .problem import (
    ProblemDetector,
    detect_problem,
)

from .preparation import (
    DataPreparation,
    PreparedData,
    prepare_data,
)

from .classification import (
    ClassificationModels,
)

from .regression import (
    RegressionModels,
)

from .ols import (
    OLSRegression,
)


from .logistic import (
    LogisticRegressionModel,
)


from .random_forest import (
    RandomForestModel,
)


from .xgboost_model import (
    XGBoostModel,
)

from .evaluation import (
    ModelEvaluator,
)

from .comparison import (
    ModelComparison,
)

from .engine import (
    EAIE,
    EAIEEngine,
)


__all__ = [
    "ProblemDetector",
    "detect_problem",
    "PreparedData",
    "DataPreparation",
    "prepare_data",
    "ClassificationModels",
    "RegressionModels",
    "OLSRegression",
    "LogisticRegressionModel",
    "RandomForestModel",
    "XGBoostModel",
    "ModelEvaluator",
    "ModelComparison",
    "EAIEEngine",
    "EAIE",
]
