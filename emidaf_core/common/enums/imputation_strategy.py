"""
=========================================================
EMIDAF Framework
Imputation Strategy
=========================================================
"""

from enum import Enum


class ImputationStrategy(str, Enum):

    NONE = "None"

    MEAN = "Mean"

    MEDIAN = "Median"

    MODE = "Mode"

    KNN = "KNN"

    MICE = "MICE"

    REGRESSION = "Regression"

    INTERPOLATION = "Interpolation"

    FORWARD_FILL = "Forward Fill"

    BACKWARD_FILL = "Backward Fill"

    DELETE = "Delete"

    CONSTANT = "Constant"

    REVIEW = "Review Variable"