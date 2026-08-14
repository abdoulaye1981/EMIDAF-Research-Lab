"""
=========================================================
EMIDAF Framework
Datetime Processing Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

from abc import ABC

import pandas as pd
import numpy as np

from .base import BasePreprocessor

# ==========================================================
# BASE
# ==========================================================

class BaseDatetimeProcessor(BasePreprocessor):

    """
    Classe mère.
    """

    name = "Datetime Processor"

# ==========================================================
# TO DATETIME
# ==========================================================

class DatetimeConverter(

    BaseDatetimeProcessor

):

    name = "Datetime Converter"

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

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        X = X.copy()

        for column in X.columns:

            X[column] = pd.to_datetime(

                X[column],

                errors=self.errors

            )

        return X

# ==========================================================
# DATE FEATURES
# ==========================================================

class DateFeatureExtractor(

    BaseDatetimeProcessor

):

    name = "Date Feature Extractor"

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

        X = X.copy()

        for column in X.columns:

            dt = X[column]

            X[f"{column}_year"] = dt.dt.year

            X[f"{column}_quarter"] = dt.dt.quarter

            X[f"{column}_month"] = dt.dt.month

            X[f"{column}_week"] = dt.dt.isocalendar().week

            X[f"{column}_day"] = dt.dt.day

            X[f"{column}_dayofweek"] = dt.dt.dayofweek

            X[f"{column}_dayofyear"] = dt.dt.dayofyear

            X[f"{column}_hour"] = dt.dt.hour

            X[f"{column}_minute"] = dt.dt.minute

            X[f"{column}_second"] = dt.dt.second

            X[f"{column}_weekend"] = (

                dt.dt.dayofweek >= 5

            ).astype(int)

        return X
    
# ==========================================================
# SEASON
# ==========================================================

class SeasonExtractor(

    BaseDatetimeProcessor

):

    name = "Season"

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

        X = X.copy()

        seasons = {

            12:"Winter",

            1:"Winter",

            2:"Winter",

            3:"Spring",

            4:"Spring",

            5:"Spring",

            6:"Summer",

            7:"Summer",

            8:"Summer",

            9:"Autumn",

            10:"Autumn",

            11:"Autumn"

        }

        for column in X.columns:

            X[f"{column}_season"] = (

                X[column]

                .dt.month

                .map(seasons)

            )

        return X
    
# ==========================================================
# DATE DIFFERENCE
# ==========================================================

class DateDifference(

    BaseDatetimeProcessor

):

    name = "Difference"

    def __init__(

        self,

        first,

        second,

    ):

        self.first = first

        self.second = second

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

        X = X.copy()

        X["difference_days"] = (

            X[self.second]

            -

            X[self.first]

        ).dt.days

        return X
    
# ==========================================================
# LAG
# ==========================================================

class LagFeature(

    BaseDatetimeProcessor

):

    name = "Lag"

    def __init__(

        self,

        column,

        lags=3,

    ):

        self.column = column

        self.lags = lags

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

        X = X.copy()

        for lag in range(

            1,

            self.lags+1

        ):

            X[

                f"{self.column}_lag_{lag}"

            ] = (

                X[self.column]

                .shift(lag)

            )

        return X
    
# ==========================================================
# ROLLING
# ==========================================================

class RollingFeature(

    BaseDatetimeProcessor

):

    name = "Rolling"

    def __init__(

        self,

        column,

        window=7,

    ):

        self.column = column

        self.window = window

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

        X = X.copy()

        X[f"{self.column}_rolling_mean"] = (

            X[self.column]

            .rolling(

                self.window

            )

            .mean()

        )

        X[f"{self.column}_rolling_std"] = (

            X[self.column]

            .rolling(

                self.window

            )

            .std()

        )

        return X
    
# ==========================================================
# SERVICE
# ==========================================================

class DateTime:

    registry = {

        "convert":

            DatetimeConverter,

        "features":

            DateFeatureExtractor,

        "season":

            SeasonExtractor,

        "difference":

            DateDifference,

        "lag":

            LagFeature,

        "rolling":

            RollingFeature

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