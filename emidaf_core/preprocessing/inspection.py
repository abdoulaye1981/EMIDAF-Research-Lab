"""
=========================================================
EMIDAF Framework
Dataset Inspection Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# DATASET INSPECTION
# ==========================================================

class DatasetInspection(
    BasePreprocessing
):

    """
    Automatic dataset inspection.
    """

    name="Inspection"

    def __init__(self):

        self.result=None

    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.result=self.inspect(X)

        return self

    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        return X

    # ==========================================================
# SHAPE
# ==========================================================

    @staticmethod
    def shape(df):

        return df.shape

    # ==========================================================
# MEMORY
# ==========================================================

    @staticmethod
    def memory(df):

        return float(

            df.memory_usage(

                deep=True

            ).sum()

            /

            1024**2

        )

    # ==========================================================
# DTYPES
# ==========================================================

    @staticmethod
    def dtypes(df):

        return df.dtypes.astype(str).to_dict()

    # ==========================================================
# NUMERIC
# ==========================================================

    @staticmethod
    def numeric(df):

        return list(

            df.select_dtypes(

                include=np.number

            ).columns

        )
    # ==========================================================
# CATEGORICAL
# ==========================================================

    @staticmethod
    def categorical(df):

        return list(

            df.select_dtypes(

                include="object"

            ).columns

        )
    # ==========================================================
# BOOLEAN
# ==========================================================

    @staticmethod
    def boolean(df):

        return list(

            df.select_dtypes(

                include="bool"

            ).columns

        )

    # ==========================================================
# DATETIME
# ==========================================================

    @staticmethod
    def datetime(df):

        return list(

            df.select_dtypes(

                include="datetime"

            ).columns

        )

    # ==========================================================
# MISSING
# ==========================================================

    @staticmethod
    def missing(df):

        return (

            df.isna()

            .sum()

            .to_dict()

        )

    # ==========================================================
# MISSING %
# ==========================================================

    @staticmethod
    def missing_percent(df):

        return (

            (

                df.isna().mean()

                *100

            )

            .round(2)

            .to_dict()

        )

    # ==========================================================
# UNIQUE
# ==========================================================

    @staticmethod
    def unique(df):

        return df.nunique().to_dict()

    # ==========================================================
# CARDINALITY
# ==========================================================

    @staticmethod
    def cardinality(df):

        return {

            c:df[c].nunique()

            for c

            in df.columns

        }

    # ==========================================================
# CONSTANT
# ==========================================================

    @staticmethod
    def constant(df):

        return [

            c

            for c

            in df.columns

            if df[c].nunique()==1

        ]

    # ==========================================================
# QUASI CONSTANT
# ==========================================================

    @staticmethod
    def quasi_constant(

        df,

        threshold=0.99

    ):

        cols=[]

        for c in df.columns:

            if (

                df[c]

                .value_counts(

                    normalize=True

                )

                .iloc[0]

                >=threshold

            ):

                cols.append(c)

        return cols

    # ==========================================================
# DUPLICATED COLUMNS
# ==========================================================

    @staticmethod
    def duplicated_columns(df):

        duplicates=[]

        cols=df.columns

        for i in range(len(cols)):

            for j in range(i+1,len(cols)):

                if df[cols[i]].equals(

                    df[cols[j]]

                ):

                    duplicates.append(

                        (

                            cols[i],

                            cols[j]

                        )

                    )

        return duplicates

    # ==========================================================
# IDENTIFIER
# ==========================================================

    @staticmethod
    def identifiers(df):

        return [

            c

            for c

            in df.columns

            if df[c].nunique()==len(df)

        ]

    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(df):

        result=PreprocessingResult(

            step="Inspection",

            input_shape=df.shape,

            output_shape=df.shape

        )

        result.statistics={

            "shape":

                DatasetInspection.shape(df),

            "memory_mb":

                DatasetInspection.memory(df),

            "dtypes":

                DatasetInspection.dtypes(df),

            "numeric":

                DatasetInspection.numeric(df),

            "categorical":

                DatasetInspection.categorical(df),

            "boolean":

                DatasetInspection.boolean(df),

            "datetime":

                DatasetInspection.datetime(df),

            "missing":

                DatasetInspection.missing(df),

            "missing_percent":

                DatasetInspection.missing_percent(df),

            "unique":

                DatasetInspection.unique(df),

            "cardinality":

                DatasetInspection.cardinality(df),

            "constant":

                DatasetInspection.constant(df),

            "quasi_constant":

                DatasetInspection.quasi_constant(df),

            "duplicated_columns":

                DatasetInspection.duplicated_columns(df),

            "identifiers":

                DatasetInspection.identifiers(df)

        }

        return result

# ==========================================================
# SERVICE
# ==========================================================

class Inspection:

    inspect=DatasetInspection.inspect