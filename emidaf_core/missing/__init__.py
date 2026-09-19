"""
=========================================================
EMIDAF Framework v1.0
Missing Data Public API
---------------------------------------------------------
Lazy public API for the missing-data subsystem.
=========================================================
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any


__all__ = [
    "MissingPipeline",
    "MissingPipelineResult",
    "ColumnImputationDecision",
    "ImputationPlan",
    "ImputationPlanBuilder",
    "ImputationPlanExecutor",
    "MissingImputer",
    "SimpleImputer",
    "KNNImputer",
    "MICEImputer",
    "MissingReporter",
]


_LAZY_EXPORTS: dict[
    str,
    tuple[str, str],
] = {
    "MissingPipeline": (
        "emidaf_core.missing.missing_pipeline",
        "MissingPipeline",
    ),

    "MissingPipelineResult": (
        "emidaf_core.missing.missing_pipeline",
        "MissingPipelineResult",
    ),

    "ColumnImputationDecision": (
        "emidaf_core.missing.imputation.imputation_plan",
        "ColumnImputationDecision",
    ),

    "ImputationPlan": (
        "emidaf_core.missing.imputation.imputation_plan",
        "ImputationPlan",
    ),

    "ImputationPlanBuilder": (
        "emidaf_core.missing.imputation.plan_builder",
        "ImputationPlanBuilder",
    ),

    "ImputationPlanExecutor": (
        "emidaf_core.missing.imputation.plan_executor",
        "ImputationPlanExecutor",
    ),

    "MissingImputer": (
        "emidaf_core.missing.imputation.missing_imputer",
        "MissingImputer",
    ),

    "SimpleImputer": (
        "emidaf_core.missing.imputation.simple_imputer",
        "SimpleImputer",
    ),

    "KNNImputer": (
        "emidaf_core.missing.imputation.knn_imputer",
        "KNNImputer",
    ),

    "MICEImputer": (
        "emidaf_core.missing.imputation.mice_imputer",
        "MICEImputer",
    ),

    "MissingReporter": (
        "emidaf_core.missing.reporting.missing_reporter",
        "MissingReporter",
    ),
}


def __getattr__(
    name: str,
) -> Any:
    """
    Charge les objets publics uniquement lorsqu'ils
    sont demandés.

    Cette stratégie évite les imports circulaires entre
    le profiler, MissingAnalyzer et MissingPipeline.
    """

    export = _LAZY_EXPORTS.get(
        name
    )

    if export is None:
        raise AttributeError(
            f"module {__name__!r} "
            f"has no attribute {name!r}"
        )

    module_name, attribute_name = export

    module = import_module(
        module_name
    )

    value = getattr(
        module,
        attribute_name,
    )

    globals()[name] = value

    return value


if TYPE_CHECKING:

    from emidaf_core.missing.missing_pipeline import (
        MissingPipeline,
        MissingPipelineResult,
    )

    from emidaf_core.missing.imputation.imputation_plan import (
        ColumnImputationDecision,
        ImputationPlan,
    )

    from emidaf_core.missing.imputation.plan_builder import (
        ImputationPlanBuilder,
    )

    from emidaf_core.missing.imputation.plan_executor import (
        ImputationPlanExecutor,
    )

    from emidaf_core.missing.imputation.missing_imputer import (
        MissingImputer,
    )

    from emidaf_core.missing.imputation.simple_imputer import (
        SimpleImputer,
    )

    from emidaf_core.missing.imputation.knn_imputer import (
        KNNImputer,
    )

    from emidaf_core.missing.imputation.mice_imputer import (
        MICEImputer,
    )

    from emidaf_core.missing.reporting.missing_reporter import (
        MissingReporter,
    )
