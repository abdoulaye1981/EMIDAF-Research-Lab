"""
=========================================================
EMIDAF Framework
Statistical Profiling Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from .central_tendency import CentralTendency
from .dispersion import Dispersion
from .position import Position
from .shape import Shape

# ==========================================================
# PROFILER
# ==========================================================

class StatisticalProfiler:

    """
    Profil statistique automatique
    d'un DataFrame.
    """

    def __init__(

        self,

        dataframe,

    ):

        self.df = dataframe.copy()

# ==========================================================
# GENERAL
# ==========================================================

    def general_information(

        self,

    ):

        return {

            "rows":

                self.df.shape[0],

            "columns":

                self.df.shape[1],

            "memory":

                self.df.memory_usage(

                    deep=True

                ).sum(),

            "duplicates":

                self.df.duplicated().sum()

        }

    # ==========================================================
# TYPES
# ==========================================================

    def variable_types(

        self,

    ):

        numeric = self.df.select_dtypes(

            include=np.number

        ).columns.tolist()

        categorical = self.df.select_dtypes(

            include=[

                "object",

                "category",

                "bool"

            ]

        ).columns.tolist()

        datetime = self.df.select_dtypes(

            include=[

                "datetime64"

            ]

        ).columns.tolist()

        return {

            "numeric":

                numeric,

            "categorical":

                categorical,

            "datetime":

                datetime

        }
    
    # ==========================================================
# MISSING
# ==========================================================

    def missing_values(

        self,

    ):

        count = self.df.isna().sum()

        percent = (

            count

            /

            len(self.df)

        ) * 100

        return pd.DataFrame({

            "Missing":

                count,

            "Percent":

                percent

        })

    # ==========================================================
# NUMERIC PROFILE
# ==========================================================

    def numeric_profile(

        self,

    ):

        report = {}

        columns = self.df.select_dtypes(

            include=np.number

        ).columns

        for column in columns:

            x = self.df[column].dropna()

            report[column] = {

                "central":

                    CentralTendency.all(

                        x

                    ),

                "dispersion":

                    Dispersion.all(

                        x

                    ),

                "position":

                    Position.all(

                        x

                    ),

                "shape":

                    Shape.all(

                        x

                    )

            }

        return report

    # ==========================================================
# CATEGORICAL PROFILE
# ==========================================================

    def categorical_profile(

        self,

    ):

        report = {}

        columns = self.df.select_dtypes(

            include=[

                "object",

                "category",

                "bool"

            ]

        ).columns

        for column in columns:

            report[column] = {

                "unique":

                    self.df[column]

                    .nunique(),

                "mode":

                    self.df[column]

                    .mode()

                    .iloc[0],

                "frequencies":

                    self.df[column]

                    .value_counts()

                    .to_dict()

            }

        return report
    
    # ==========================================================
# CORRELATION
# ==========================================================

    def correlation(

        self,

        method="pearson",

    ):

        return (

            self.df

            .select_dtypes(

                include=np.number

            )

            .corr(

                method=method

            )

        )
    
    # ==========================================================
# REPORT
# ==========================================================

    def report(

        self,

    ):

        return {

            "general":

                self.general_information(),

            "types":

                self.variable_types(),

            "missing":

                self.missing_values(),

            "numeric":

                self.numeric_profile(),

            "categorical":

                self.categorical_profile(),

            "correlation":

                self.correlation()

        }

    # ==========================================================
# SERVICE
# ==========================================================

class Profiling:

    @staticmethod

    def profile(

        dataframe,

    ):

        profiler = StatisticalProfiler(

            dataframe

        )

        return profiler.report()