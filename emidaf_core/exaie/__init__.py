"""
EMIDAF - EXAIE

Explainable Artificial Intelligence Engine.
"""

from .importance import GlobalImportance
from .local import LocalExplanation
from .shap_explainer import ShapExplainer
from .interpretation import (
    ExplainabilityInterpreter,
    Interpretation,
)
from .engine import (
    EXAIEEngine,
    EXAIE,
)

from .aggregation import (
    FeatureImportanceAggregator,
    aggregate_global_importance,
    aggregate_local_contributions,
)


__all__ = [
    "GlobalImportance",
    "LocalExplanation",
    "ShapExplainer",
    "ExplainabilityInterpreter",
    "Interpretation",
    "EXAIEEngine",
    "EXAIE",
    "FeatureImportanceAggregator",
    "aggregate_global_importance",
    "aggregate_local_contributions",
]
