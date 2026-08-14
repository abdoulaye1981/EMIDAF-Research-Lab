"""
=========================================================
EMIDAF Framework
Preprocessing Inspection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class DataInspector:

    name = "Data Inspector"

    def __init__(
        self,
        df=None
    ):

        self.df = df

    def fit(
        self,
        X,
        y=None
    ):

        self.df = X.copy()

        return self

    def transform(
        self,
        X
    ):

        return X.copy()

    def shape(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return data.shape

    def columns(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return list(
            data.columns
        )

    def dtypes(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return data.dtypes

    def numeric_columns(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return list(
            data.select_dtypes(
                include=np.number
            ).columns
        )

    def categorical_columns(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return list(
            data.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            ).columns
        )

    def datetime_columns(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return list(
            data.select_dtypes(
                include=[
                    "datetime",
                    "datetimetz"
                ]
            ).columns
        )

    def missing(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        result = pd.DataFrame({

            "variable":
                data.columns,

            "missing_count":
                data.isna().sum().values,

            "missing_percentage":
                (
                    data.isna()
                    .mean()
                    .values
                    * 100
                )

        })

        return result.sort_values(
            "missing_count",
            ascending=False
        ).reset_index(
            drop=True
        )

    def duplicates(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        count = int(
            data.duplicated().sum()
        )

        percentage = (
            count / len(data) * 100
            if len(data) > 0
            else 0
        )

        return {

            "count":
                count,

            "percentage":
                percentage

        }

    def unique_values(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return pd.DataFrame({

            "variable":
                data.columns,

            "unique":
                [
                    data[column]
                    .nunique(
                        dropna=True
                    )
                    for column
                    in data.columns
                ]

        })

    def describe(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return data.describe(
            include="all"
        ).transpose()

    def numeric_summary(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        numeric = data.select_dtypes(
            include=np.number
        )

        if numeric.empty:

            return pd.DataFrame()

        return numeric.describe().transpose()

    def categorical_summary(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        categorical = data.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        )

        if categorical.empty:

            return pd.DataFrame()

        rows = []

        for column in categorical.columns:

            series = categorical[column]

            rows.append({

                "variable":
                    column,

                "unique":
                    series.nunique(
                        dropna=True
                    ),

                "missing":
                    series.isna().sum(),

                "mode":
                    series.mode(
                        dropna=True
                    ).iloc[0]
                    if not series.mode(
                        dropna=True
                    ).empty
                    else np.nan

            })

        return pd.DataFrame(
            rows
        )

    def overview(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return {

            "rows":
                data.shape[0],

            "columns":
                data.shape[1],

            "numeric_variables":
                len(
                    self.numeric_columns(
                        data
                    )
                ),

            "categorical_variables":
                len(
                    self.categorical_columns(
                        data
                    )
                ),

            "datetime_variables":
                len(
                    self.datetime_columns(
                        data
                    )
                ),

            "missing_values":
                int(
                    data.isna()
                    .sum()
                    .sum()
                ),

            "duplicate_rows":
                int(
                    data.duplicated()
                    .sum()
                )

        }


    def summary(
        self,
        df=None
    ):

        data = (
            self.df
            if df is None
            else df
        )

        return {

            "overview":
                self.overview(data),

            "dtypes":
                self.dtypes(data),

            "missing":
                self.missing(data),

            "duplicates":
                self.duplicates(data),

            "unique_values":
                self.unique_values(data),

            "numeric_summary":
                self.numeric_summary(data),

            "categorical_summary":
                self.categorical_summary(data)

        }


class Inspection(
    DataInspector
):

    pass
