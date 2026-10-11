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


from .multilevel import (
    MultilevelLinearModel,
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

from .roles import (
    FeatureRoleResult,
    FeatureRoles,
    resolve_feature_roles,
)

from .blocks import (
    FeatureBlockResult,
    FeatureBlocks,
    resolve_feature_blocks,
)

from .block_comparison import (
    BlockComparisonEngine,
    BlockComparisonResult,
    BlockPerformance,
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
    "MultilevelLinearModel",
    "ModelEvaluator",
    "ModelComparison",
    "EAIEEngine",
    "EAIE",
    "FeatureRoleResult",
    "FeatureRoles",
    "resolve_feature_roles",
    "FeatureBlockResult",
    "FeatureBlocks",
    "resolve_feature_blocks",
    "BlockComparisonEngine",
    "BlockComparisonResult",
    "BlockPerformance",
]
