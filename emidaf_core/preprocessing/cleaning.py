"""
=========================================================
EMIDAF Framework
Data Cleaning Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

import re
import unicodedata

import numpy as np
import pandas as pd

from ..common.results import CleaningResult
from .base import BasePreprocessor


class DataCleaner(BasePreprocessor):
    """
    Moteur principal de nettoyage.

    Toutes les opérations sont chaînables.
    """

    name = "Data Cleaner"

    def __init__(self):

        super().__init__()

        self.history = []

    #########################################################
    # FIT
    #########################################################

    def fit(

        self,

        X,

        y=None,

    ):

        self.fitted = True

        return self

    #########################################################
    # TRANSFORM
    #########################################################

    def transform(

        self,

        X,

    ):

        return X.copy()
    
    #########################################################
# DUPLICATES
#########################################################

    def remove_duplicates(

        self,

        dataframe,

        subset=None,

        keep="first",

    ):

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates(

            subset=subset,

            keep=keep

        )

        removed = before - len(dataframe)

        self.history.append(

            {

                "operation":"duplicates",

                "removed":removed

            }

        )

        return dataframe
    
    #########################################################
# DUPLICATED COLUMNS
#########################################################

    def remove_duplicated_columns(

        self,

        dataframe,

    ):

        dataframe = dataframe.loc[

            :,

            ~dataframe.columns.duplicated()

        ]

        self.history.append(

            {

                "operation":"duplicated_columns"

            }

        )

        return dataframe
    
    #########################################################
# STRIP
#########################################################

    def strip(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        object_columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in object_columns:

            dataframe[column] = (

                dataframe[column]

                .astype(str)

                .str.strip()

            )

        self.history.append(

            {

                "operation":"strip"

            }

        )

        return dataframe
    
    #########################################################
# UNICODE
#########################################################

    def normalize_unicode(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        object_columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in object_columns:

            dataframe[column] = dataframe[column].apply(

                lambda x:

                unicodedata.normalize(

                    "NFKC",

                    str(x)

                )

            )

        self.history.append(

            {

                "operation":"unicode"

            }

        )

        return dataframe
    
    #########################################################
# LOWERCASE
#########################################################

    def lowercase(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        object_columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in object_columns:

            dataframe[column] = (

                dataframe[column]

                .str.lower()

            )

        self.history.append(

            {

                "operation":"lowercase"

            }

        )

        return dataframe
    
    #########################################################
# UPPERCASE
#########################################################

    def uppercase(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        object_columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in object_columns:

            dataframe[column] = (

                dataframe[column]

                .str.upper()

            )

        self.history.append(

            {

                "operation":"uppercase"

            }

        )

        return dataframe
    
    #########################################################
# TITLE
#########################################################

    def title(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        object_columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in object_columns:

            dataframe[column] = (

                dataframe[column]

                .str.title()

            )

        self.history.append(

            {

                "operation":"title"

            }

        )

        return dataframe

    #########################################################
# MULTIPLE SPACES
#########################################################

    def remove_multiple_spaces(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in columns:

            dataframe[column] = dataframe[column].replace(

                r"\s+",

                " ",

                regex=True

            )

        self.history.append(

            {

                "operation":"multiple_spaces"

            }

        )

        return dataframe

    #########################################################
# SPECIAL CHARACTERS
#########################################################

    def remove_special_characters(

        self,

        dataframe,

        pattern=r"[^A-Za-zÀ-ÿ0-9 ]",

    ):

        dataframe = dataframe.copy()

        columns = dataframe.select_dtypes(

            include="object"

        ).columns

        for column in columns:

            dataframe[column] = dataframe[column].replace(

                pattern,

                "",

                regex=True

            )

        self.history.append(

            {

                "operation":"special_characters"

            }

        )

        return dataframe

    #########################################################
# IMPOSSIBLE VALUES
#########################################################

    def replace_impossible_values(

        self,

        dataframe,

        rules,

    ):

        dataframe = dataframe.copy()

        for column, condition in rules.items():

            dataframe.loc[

                condition(

                    dataframe[column]

                ),

                column

            ] = np.nan

        self.history.append(

            {

                "operation":"impossible_values"

            }

        )

        return dataframe

    #########################################################
# CONSTANT COLUMNS
#########################################################

    def remove_constant_columns(

        self,

        dataframe,

    ):

        dataframe = dataframe.loc[

            :,

            dataframe.nunique(

                dropna=False

            ) > 1

        ]

        self.history.append(

            {

                "operation":"constant_columns"

            }

        )

        return dataframe

    #########################################################
# QUASI CONSTANT
#########################################################

    def remove_quasi_constant(

        self,

        dataframe,

        threshold=0.99,

    ):

        keep = []

        for column in dataframe.columns:

            ratio = (

                dataframe[column]

                .value_counts(

                    normalize=True,

                    dropna=False

                )

                .max()

            )

            if ratio < threshold:

                keep.append(column)

        dataframe = dataframe[keep]

        self.history.append(

            {

                "operation":"quasi_constant"

            }

        )

        return dataframe

    #########################################################
# AUTO TYPE CONVERSION
#########################################################

    def auto_convert_types(

        self,

        dataframe,

        datetime_threshold=0.90,

        numeric_threshold=0.95,

    ):

        """
        Conversion automatique des colonnes.

        object -> numeric
        object -> datetime
        object -> category
        """

        dataframe = dataframe.copy()

        for column in dataframe.columns:

            if dataframe[column].dtype != object:

                continue

            # ------------------------------------------
            # Numeric
            # ------------------------------------------

            numeric = pd.to_numeric(

                dataframe[column],

                errors="coerce"

            )

            if numeric.notna().mean() >= numeric_threshold:

                dataframe[column] = numeric

                continue

            # ------------------------------------------
            # Datetime
            # ------------------------------------------

            dt = pd.to_datetime(

                dataframe[column],

                errors="coerce"

            )

            if dt.notna().mean() >= datetime_threshold:

                dataframe[column] = dt

                continue

            # ------------------------------------------
            # Category
            # ------------------------------------------

            if dataframe[column].nunique() < len(dataframe)*0.25:

                dataframe[column] = (

                    dataframe[column]

                    .astype("category")

                )

        self.history.append(

            {

                "operation":"auto_convert_types"

            }

        )

        return dataframe

    #########################################################
# EMPTY COLUMNS
#########################################################

    def remove_empty_columns(

        self,

        dataframe,

    ):

        dataframe = dataframe.dropna(

            axis=1,

            how="all"

        )

        self.history.append(

            {

                "operation":"empty_columns"

            }

        )

        return dataframe


    #########################################################
# EMPTY ROWS
#########################################################

    def remove_empty_rows(

        self,

        dataframe,

    ):

        dataframe = dataframe.dropna(

            axis=0,

            how="all"

        )

        self.history.append(

            {

                "operation":"empty_rows"

            }

        )

        return dataframe
    
    #########################################################
# INVISIBLE CHARACTERS
#########################################################

    def remove_invisible_characters(

        self,

        dataframe,

    ):

        dataframe = dataframe.copy()

        columns = dataframe.select_dtypes(

            include="object"

        ).columns

        pattern = r"[\u200B-\u200D\uFEFF]"

        for column in columns:

            dataframe[column] = dataframe[column].replace(

                pattern,

                "",

                regex=True

            )

        self.history.append(

            {

                "operation":"invisible_characters"

            }

        )

        return dataframe
    
    #########################################################
# CATEGORY STANDARDIZATION
#########################################################

    def standardize_categories(

        self,

        dataframe,

        mapping,

    ):

        dataframe = dataframe.copy()

        for column, values in mapping.items():

            dataframe[column] = (

                dataframe[column]

                .replace(values)

            )

        self.history.append(

            {

                "operation":"category_standardization"

            }

        )

        return dataframe


    #########################################################
# COLUMN NAMES
#########################################################

    def clean_column_names(

        self,

        dataframe,

        lowercase=True,

        separator="_",

    ):

        dataframe = dataframe.copy()

        columns = []

        for column in dataframe.columns:

            c = column.strip()

            c = re.sub(

                r"\s+",

                separator,

                c

            )

            c = re.sub(

                r"[^\w]",

                "",

                c

            )

            if lowercase:

                c = c.lower()

            columns.append(c)

        dataframe.columns = columns

        self.history.append(

            {

                "operation":"column_names"

            }

        )

        return dataframe

    #########################################################
# CONSISTENCY CHECK
#########################################################

    def check_consistency(

        self,

        dataframe,

        rules,

    ):

        report = {}

        for name, rule in rules.items():

            invalid = dataframe.loc[

                rule(dataframe)

            ]

            report[name] = invalid.index.tolist()

        return report

    #########################################################
# REPORT
#########################################################

    def report(

        self,

    ):

        return {

            "operations":

                self.history,

            "total_operations":

                len(self.history)

        }

    #########################################################
# AUTO CLEAN
#########################################################

    def auto_clean(

        self,

        dataframe,

    ):

        dataframe = (

            self

            .remove_empty_rows(dataframe)

        )

        dataframe = (

            self

            .remove_empty_columns(dataframe)

        )

        dataframe = (

            self

            .remove_duplicates(dataframe)

        )

        dataframe = (

            self

            .remove_duplicated_columns(dataframe)

        )

        dataframe = (

            self

            .remove_invisible_characters(dataframe)

        )

        dataframe = (

            self

            .strip(dataframe)

        )

        dataframe = (

            self

            .remove_multiple_spaces(dataframe)

        )

        dataframe = (

            self

            .normalize_unicode(dataframe)

        )

        dataframe = (

            self

            .clean_column_names(dataframe)

        )

        dataframe = (

            self

            .remove_constant_columns(dataframe)

        )

        dataframe = (

            self

            .auto_convert_types(dataframe)

        )

        return dataframe

    #########################################################
# SERVICE
#########################################################

class Cleaning:

    """
    API publique EMIDAF.
    """

    @staticmethod
    def clean(df):

        cleaner = DataCleaner()

        return cleaner.auto_clean(df)

    @staticmethod
    def report(df):

        cleaner = DataCleaner()

        cleaner.auto_clean(df)

        return cleaner.report()