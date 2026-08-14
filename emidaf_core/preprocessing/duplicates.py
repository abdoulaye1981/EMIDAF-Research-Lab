"""
=========================================================
EMIDAF Framework
Duplicate Data Detection and Treatment
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# DUPLICATES
# ==========================================================

class DuplicateDetection(
    BasePreprocessing
):

    """
    Complete duplicate detection and treatment engine.
    """

    name = "Duplicate Detection"

    def __init__(
        self,
        keep="first"
    ):

        self.keep = keep
        self.result = None

    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.result = self.inspect(X)

        return self

    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        return self.remove(
            X,
            keep=self.keep
        )

    # ==========================================================
# DUPLICATE COUNT
# ==========================================================

    @staticmethod
    def count(
        df,
        keep="first"
    ):

        return int(
            df.duplicated(
                keep=keep
            ).sum()
        )

    # ==========================================================
# DUPLICATE PERCENTAGE
# ==========================================================

    @staticmethod
    def percentage(
        df,
        keep="first"
    ):

        if len(df) == 0:

            return 0.0

        return (
            DuplicateDetection.count(
                df,
                keep=keep
            )
            / len(df)
            * 100
        )

    # ==========================================================
# DUPLICATE MASK
# ==========================================================

    @staticmethod
    def mask(
        df,
        keep="first"
    ):

        return df.duplicated(
            keep=keep
        )

    # ==========================================================
# GET DUPLICATES
# ==========================================================

    @staticmethod
    def get(
        df,
        keep=False
    ):

        return df.loc[
            df.duplicated(
                keep=keep
            )
        ].copy()

    # ==========================================================
# REMOVE DUPLICATES
# ==========================================================

    @staticmethod
    def remove(
        df,
        keep="first"
    ):

        return (
            df
            .drop_duplicates(
                keep=keep
            )
            .reset_index(
                drop=True
            )
        )

    # ==========================================================
# DUPLICATES BY COLUMNS
# ==========================================================

    @staticmethod
    def by_columns(
        df,
        columns,
        keep=False
    ):

        columns = list(columns)

        missing_columns = [
            column
            for column in columns
            if column not in df.columns
        ]

        if missing_columns:

            raise KeyError(
                f"Colonnes inexistantes : "
                f"{missing_columns}"
            )

        return df.loc[
            df.duplicated(
                subset=columns,
                keep=keep
            )
        ].copy()

    # ==========================================================
# REMOVE BY COLUMNS
# ==========================================================

    @staticmethod
    def remove_by_columns(
        df,
        columns,
        keep="first"
    ):

        columns = list(columns)

        missing_columns = [
            column
            for column in columns
            if column not in df.columns
        ]

        if missing_columns:

            raise KeyError(
                f"Colonnes inexistantes : "
                f"{missing_columns}"
            )

        return (
            df
            .drop_duplicates(
                subset=columns,
                keep=keep
            )
            .reset_index(
                drop=True
            )
        )

    # ==========================================================
# DUPLICATE GROUPS
# ==========================================================

    @staticmethod
    def groups(
        df,
        columns=None
    ):

        if columns is None:

            columns = list(df.columns)

        duplicated_mask = (
            df.duplicated(
                subset=columns,
                keep=False
            )
        )

        duplicates = df.loc[
            duplicated_mask
        ].copy()

        if duplicates.empty:

            return pd.DataFrame(
                columns=[
                    *columns,
                    "duplicate_group",
                    "group_size"
                ]
            )

        duplicates["duplicate_group"] = (
            duplicates
            .groupby(columns, dropna=False)
            .ngroup()
        )

        duplicates["group_size"] = (
            duplicates
            .groupby(
                "duplicate_group"
            )["duplicate_group"]
            .transform("size")
        )

        return duplicates

    # ==========================================================
# CLEAN
# ==========================================================

    @staticmethod
    def clean(
        df,
        keep="first"
    ):

        before = len(df)

        duplicate_count = (
            DuplicateDetection.count(
                df,
                keep=keep
            )
        )

        cleaned = (
            DuplicateDetection.remove(
                df,
                keep=keep
            )
        )

        after = len(cleaned)

        return cleaned

    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        duplicate_count = (
            DuplicateDetection.count(
                df
            )
        )

        percentage = (
            DuplicateDetection.percentage(
                df
            )
        )

        duplicate_rows = (
            DuplicateDetection.get(
                df,
                keep=False
            )
        )

        result = PreprocessingResult(

            step="Duplicate Detection",

            input_shape=df.shape,

            output_shape=(
                df.drop_duplicates().shape
            ),

            variables=list(
                df.columns
            )
        )

        result.statistics = {

            "duplicate_count":
                duplicate_count,

            "duplicate_percent":
                percentage,

            "unique_rows":
                int(
                    df.drop_duplicates()
                    .shape[0]
                ),

            "duplicate_rows":
                duplicate_rows

        }

        return result

# ==========================================================
# SERVICE
# ==========================================================

class Duplicates:

    count = DuplicateDetection.count

    percentage = (
        DuplicateDetection.percentage
    )

    mask = DuplicateDetection.mask

    get = DuplicateDetection.get

    remove = DuplicateDetection.remove

    by_columns = (
        DuplicateDetection.by_columns
    )

    remove_by_columns = (
        DuplicateDetection.remove_by_columns
    )

    groups = DuplicateDetection.groups

    clean = DuplicateDetection.clean

    inspect = DuplicateDetection.inspect