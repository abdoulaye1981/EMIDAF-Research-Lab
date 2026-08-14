"""
=========================================================
EMIDAF Framework
Data Validation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Validation complète des jeux de données.

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


# ==========================================================
# VALIDATION RESULT
# ==========================================================

@dataclass(slots=True)
class ValidationResult:

    valid: bool = True

    rows: int = 0

    columns: int = 0

    duplicated_rows: int = 0

    duplicated_columns: int = 0

    missing_values: int = 0

    missing_rate: float = 0.0

    numeric_columns: list = field(default_factory=list)

    categorical_columns: list = field(default_factory=list)

    datetime_columns: list = field(default_factory=list)

    boolean_columns: list = field(default_factory=list)

    constant_columns: list = field(default_factory=list)

    duplicated_column_names: list = field(default_factory=list)

    warnings: list = field(default_factory=list)

    errors: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_warning(self, message):

        self.warnings.append(message)

    def add_error(self, message):

        self.errors.append(message)

        self.valid = False

    def summary(self):

        return {

            "Valid": self.valid,

            "Rows": self.rows,

            "Columns": self.columns,

            "Missing": self.missing_values,

            "MissingRate": self.missing_rate,

            "Warnings": len(self.warnings),

            "Errors": len(self.errors)

        }
    
    # ==========================================================
# VALIDATOR
# ==========================================================

class DatasetValidator:

    """
    Validation générale d'un DataFrame.
    """

    @classmethod
    def validate(

        cls,

        dataframe: pd.DataFrame,

    ) -> ValidationResult:

        result = ValidationResult()

        # ============================================
        # Dimensions
        # ============================================

        result.rows = dataframe.shape[0]

        result.columns = dataframe.shape[1]

        # ============================================
        # Colonnes
        # ============================================

        result.numeric_columns = (

            dataframe

            .select_dtypes(include=np.number)

            .columns

            .tolist()

        )

        result.categorical_columns = (

            dataframe

            .select_dtypes(include="object")

            .columns

            .tolist()

        )

        result.datetime_columns = (

            dataframe

            .select_dtypes(

                include="datetime"

            )

            .columns

            .tolist()

        )

        result.boolean_columns = (

            dataframe

            .select_dtypes(

                include="bool"

            )

            .columns

            .tolist()

        )

        # ============================================
        # Missing
        # ============================================

        result.missing_values = (

            dataframe

            .isna()

            .sum()

            .sum()

        )

        result.missing_rate = (

            result.missing_values

            /

            dataframe.size

        )

        # ============================================
        # Duplicates
        # ============================================

        result.duplicated_rows = (

            dataframe

            .duplicated()

            .sum()

        )

        result.duplicated_columns = (

            dataframe.columns

            .duplicated()

            .sum()

        )

        if result.duplicated_rows > 0:

            result.add_warning(

                f"{result.duplicated_rows} duplicated rows."

            )

        if result.duplicated_columns > 0:

            result.add_warning(

                f"{result.duplicated_columns} duplicated column names."

            )

        # ============================================
        # Colonnes constantes
        # ============================================

        for column in dataframe.columns:

            if dataframe[column].nunique(

                dropna=False

            ) == 1:

                result.constant_columns.append(

                    column

                )

        if len(result.constant_columns):

            result.add_warning(

                "Constant columns detected."

            )

        # ============================================
        # Colonnes vides
        # ============================================

        for column in dataframe.columns:

            if dataframe[column].isna().all():

                result.add_error(

                    f"{column} contains only missing values."

                )

        # ============================================
        # Métadonnées
        # ============================================

        result.metadata = {

            "memory_usage":

                dataframe.memory_usage(

                    deep=True

                ).sum(),

            "dtypes":

                dataframe.dtypes.astype(str).to_dict()

        }

        return result
    
    # ==========================================================
# RULE VALIDATOR
# ==========================================================

class RuleValidator:

    """
    Validation métier.
    """

    @staticmethod
    def required_columns(

        dataframe,

        columns,

    ):

        missing = [

            c

            for c in columns

            if c not in dataframe.columns

        ]

        if len(missing):

            raise ValueError(

                f"Missing columns : {missing}"

            )

    @staticmethod
    def numeric(

        dataframe,

        columns,

    ):

        for column in columns:

            if not np.issubdtype(

                dataframe[column].dtype,

                np.number

            ):

                raise TypeError(

                    f"{column} must be numeric."

                )

    @staticmethod
    def categorical(

        dataframe,

        columns,

    ):

        for column in columns:

            if dataframe[column].dtype != object:

                raise TypeError(

                    f"{column} must be categorical."

                )

    @staticmethod
    def no_missing(

        dataframe,

    ):

        if dataframe.isna().sum().sum() > 0:

            raise ValueError(

                "Dataset contains missing values."

            )

    @staticmethod
    def minimum_rows(

        dataframe,

        rows,

    ):

        if len(dataframe) < rows:

            raise ValueError(

                f"Dataset must contain at least {rows} rows."

            )

    @staticmethod
    def minimum_columns(

        dataframe,

        columns,

    ):

        if dataframe.shape[1] < columns:

            raise ValueError(

                f"Dataset must contain at least {columns} columns."

            )
        
    # ==========================================================
# SERVICE
# ==========================================================

class Validation:

    """
    API principale.
    """

    @staticmethod
    def inspect(

        dataframe,

    ):

        return DatasetValidator.validate(

            dataframe

        )

    @staticmethod
    def check(

        dataframe,

        rules=None,

    ):

        result = DatasetValidator.validate(

            dataframe

        )

        if rules:

            for rule in rules:

                rule(dataframe)

        return result