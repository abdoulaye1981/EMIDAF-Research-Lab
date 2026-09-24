"""
EMIDAF - Common Results
=======================

Résultats communs du framework.
"""

from .base_result import BaseResult
from .statistic_result import StatisticResult
from .hypothesis_result import HypothesisResult

from .descriptive_result import DescriptiveResult
from .correlation_result import CorrelationResult
from .cleaning_result import CleaningResult
from .outlier_result import OutlierResult
from .report_result import ReportResult
from .visualization_result import VisualizationResult
from .model_result import ModelResult
from .ols_result import OLSResult
from .logistic_result import LogisticResult
from .multilevel_result import MultilevelResult
from .shap_result import ShapResult


__all__ = [
    "BaseResult",
    "StatisticResult",
    "HypothesisResult",
    "DescriptiveResult",
    "CorrelationResult",
    "CleaningResult",
    "OutlierResult",
    "ReportResult",
    "VisualizationResult",
    "ModelResult",
    "OLSResult",
    "LogisticResult",
    "MultilevelResult",
    "ShapResult",
]
