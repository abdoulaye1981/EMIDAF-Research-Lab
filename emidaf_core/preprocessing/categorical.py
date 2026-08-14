"""
=========================================================
EMIDAF Framework
Categorical Processing Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Traitement des variables catégorielles.

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

class BaseCategoricalProcessor(

    BasePreprocessor

):

    """
    Classe mère.
    """

    name = "BaseCategorical"

# ==========================================================
# DETECTION
# ==========================================================

class DetectCategorical(

    BaseCategoricalProcessor

):

    name = "Detect"

    def fit(

        self,

        X,

        y=None,

    ):

        self.columns = (

            X.select_dtypes(

                include=[

                    "object",

                    "category",

                    "bool"

                ]

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
# CATEGORY
# ==========================================================

class ToCategory(

    BaseCategoricalProcessor

):

    name = "Category"

    def fit(

        self,

        X,

        y=None,

    ):

        self.columns = X.columns.tolist()

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        X = X.copy()

        for column in self.columns:

            X[column] = (

                X[column]

                .astype("category")

            )

        return X
    
# ==========================================================
# RARE LEVELS
# ==========================================================

class RareCategoryGrouping(

    BaseCategoricalProcessor

):

    name = "Rare Categories"

    def __init__(

        self,

        threshold=0.01,

        label="Other",

    ):

        self.threshold = threshold

        self.label = label

    def fit(

        self,

        X,

        y=None,

    ):

        self.mapping = {}

        for column in X.columns:

            freq = (

                X[column]

                .value_counts(

                    normalize=True

                )

            )

            rare = freq[

                freq < self.threshold

            ].index

            self.mapping[column] = rare

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        X = X.copy()

        for column in X.columns:

            X[column] = X[column].replace(

                self.mapping[column],

                self.label

            )

        return X

# ==========================================================
# MERGE LEVELS
# ==========================================================

class MergeCategories(

    BaseCategoricalProcessor

):

    name = "Merge"

    def __init__(

        self,

        mapping,

    ):

        self.mapping = mapping

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

        for column, values in self.mapping.items():

            X[column] = (

                X[column]

                .replace(values)

            )

        return X


# ==========================================================
# CLEAN
# ==========================================================

class CleanCategories(

    BaseCategoricalProcessor

):

    name = "Clean"

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

            X[column] = (

                X[column]

                .astype(str)

                .str.strip()

                .str.title()

            )

        return X

# ==========================================================
# FREQUENCIES
# ==========================================================

class CategoryStatistics(

    BaseCategoricalProcessor

):

    name = "Statistics"

    def fit(

        self,

        X,

        y=None,

    ):

        self.statistics = {}

        for column in X.columns:

            self.statistics[column] = {

                "count":

                    X[column].count(),

                "unique":

                    X[column].nunique(),

                "mode":

                    X[column].mode().iloc[0],

                "frequencies":

                    X[column]

                    .value_counts()

                    .to_dict()

            }

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        return self.statistics

# ==========================================================
# UNKNOWN
# ==========================================================

class UnknownCategoryDetector(

    BaseCategoricalProcessor

):

    name = "Unknown"

    def fit(

        self,

        X,

        y=None,

    ):

        self.levels = {}

        for column in X.columns:

            self.levels[column] = set(

                X[column]

            )

        self.fitted = True

        return self

    def transform(

        self,

        X,

    ):

        report = {}

        for column in X.columns:

            unknown = (

                set(

                    X[column]

                )

                -

                self.levels[column]

            )

            report[column] = list(

                unknown

            )

        return report
    
# ==========================================================
# AUTO
# ==========================================================

class AutoCategorical(

    BaseCategoricalProcessor

):

    """
    Pipeline automatique.

    - nettoyage

    - regroupement

    - conversion

    - statistiques
    """

# ==========================================================
# SERVICE
# ==========================================================

class Categorical:

    registry = {

        "detect":

            DetectCategorical,

        "category":

            ToCategory,

        "rare":

            RareCategoryGrouping,

        "merge":

            MergeCategories,

        "clean":

            CleanCategories,

        "statistics":

            CategoryStatistics,

        "unknown":

            UnknownCategoryDetector,

        "auto":

            AutoCategorical

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