"""
=========================================================
EMIDAF Framework
Numerical Processing Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Traitement des variables numériques.

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from .base import BasePreprocessor

# ==========================================================
# BASE
# ==========================================================

class BaseNumericalProcessor(

    BasePreprocessor

):

    """
    Classe mère.
    """

    name = "Base Numerical"

# ==========================================================
# DETECT
# ==========================================================

class DetectNumerical(

    BaseNumericalProcessor

):

    name = "Detect"

    def fit(

        self,

        X,

        y=None,

    ):

        self.columns = (

            X

            .select_dtypes(

                include=np.number

            )

            .columns

            .tolist()

        )

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        return X[self.columns]

# ==========================================================
# NUMERIC
# ==========================================================

class ToNumeric(

    BaseNumericalProcessor

):

    name = "Numeric"

    def __init__(

        self,

        errors="coerce",

    ):

        self.errors = errors

    def fit(

        self,

        X,

        y=None,

    ):

        self.columns = X.columns

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        X = X.copy()

        for column in self.columns:

            X[column] = pd.to_numeric(

                X[column],

                errors=self.errors

            )

        return X


# ==========================================================
# CLIP
# ==========================================================

class ClipValues(

    BaseNumericalProcessor

):

    name = "Clip"

    def __init__(

        self,

        lower=None,

        upper=None,

    ):

        self.lower = lower

        self.upper = upper

    def fit(

        self,

        X,

        y=None,

    ):

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        return X.clip(

            lower=self.lower,

            upper=self.upper

        )
    
# ==========================================================
# WINSORIZE
# ==========================================================

from scipy.stats.mstats import winsorize


class Winsorization(

    BaseNumericalProcessor

):

    name = "Winsorization"

    def __init__(

        self,

        limits=(0.05,0.05),

    ):

        self.limits = limits

    def fit(

        self,

        X,

        y=None,

    ):

        self.columns = X.columns

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        result = X.copy()

        for column in self.columns:

            result[column] = winsorize(

                X[column],

                limits=self.limits

            )

        return result

# ==========================================================
# NORMALITY
# ==========================================================

class NormalityCheck(

    BaseNumericalProcessor

):

    """
    Wrapper du module statistics.
    """

    name = "Normality"

    def fit(

        self,

        X,

        y=None,

    ):

        self.columns = X.columns

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        report = {}

        for column in self.columns:

            report[column] = {

                "skew":

                    X[column].skew(),

                "kurtosis":

                    X[column].kurtosis()

            }

        return report

# ==========================================================
# IQR
# ==========================================================

class IQRLimits(

    BaseNumericalProcessor

):

    name = "IQR"

    def fit(

        self,

        X,

        y=None,

    ):

        self.bounds = {}

        for column in X.columns:

            q1 = X[column].quantile(.25)

            q3 = X[column].quantile(.75)

            iqr = q3-q1

            self.bounds[column] = (

                q1-1.5*iqr,

                q3+1.5*iqr

            )

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        report = {}

        for column in X.columns:

            low, high = self.bounds[column]

            report[column] = {

                "lower":low,

                "upper":high,

                "outliers":

                    ((X[column]<low)

                    |

                    (X[column]>high))

                    .sum()

            }

        return report


# ==========================================================
# SUMMARY
# ==========================================================

class NumericalStatistics(

    BaseNumericalProcessor

):

    name = "Statistics"

    def fit(

        self,

        X,

        y=None,

    ):

        self.statistics = (

            X

            .describe()

            .T

        )

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        return self.statistics

# ==========================================================
# AUTO
# ==========================================================

class AutoNumerical(

    BaseNumericalProcessor

):

    """
    Pipeline automatique.

    Détection

    Conversion

    Bornes

    Winsorization

    Statistiques

    Contrôle de normalité
    """


# ==========================================================
# SERVICE
# ==========================================================

class Numerical:

    registry = {

        "detect":

            DetectNumerical,

        "numeric":

            ToNumeric,

        "clip":

            ClipValues,

        "winsorize":

            Winsorization,

        "normality":

            NormalityCheck,

        "iqr":

            IQRLimits,

        "statistics":

            NumericalStatistics,

        "auto":

            AutoNumerical

    }

    @classmethod
    def get(

        cls,

        method,

        **kwargs,

    ):

        return cls.registry[method](

            **kwargs

        )