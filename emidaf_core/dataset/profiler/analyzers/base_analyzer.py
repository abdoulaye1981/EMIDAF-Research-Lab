"""
=========================================================
EMIDAF Framework v1.0
Base Analyzer
---------------------------------------------------------
Classe abstraite de tous les analyzers.
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from time import perf_counter
from typing import Any

import numpy as np
import pandas as pd

from .analyzer_result import AnalyzerResult


class BaseAnalyzer(ABC):
    """
    Classe mère de tous les analyzers.
    """

    VERSION = "1.0.0"

    def __init__(self):

        self._name = self.__class__.__name__

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def name(self) -> str:

        return self._name

    @property
    def version(self) -> str:

        return self.VERSION

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        dataframe: pd.DataFrame
    ) -> None:

        if dataframe is None:

            raise ValueError(
                "DataFrame cannot be None."
            )

        if not isinstance(
            dataframe,
            pd.DataFrame
        ):

            raise TypeError(
                "Expected pandas.DataFrame."
            )

        if dataframe.empty:

            raise ValueError(
                "Empty DataFrame."
            )

    # =====================================================
    # DATAFRAME
    # =====================================================

    def shape(
        self,
        dataframe: pd.DataFrame
    ) -> tuple[int, int]:

        return dataframe.shape

    def rows(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return dataframe.shape[0]

    def columns(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return dataframe.shape[1]

    def memory_usage(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return int(

            dataframe.memory_usage(

                deep=True

            ).sum()

        )

    # =====================================================
    # TYPES
    # =====================================================

    def numeric_columns(
        self,
        dataframe: pd.DataFrame
    ) -> list[str]:

        return dataframe.select_dtypes(

            include=np.number

        ).columns.tolist()

    def categorical_columns(
        self,
        dataframe: pd.DataFrame
    ) -> list[str]:

        return dataframe.select_dtypes(

            include=["category"]

        ).columns.tolist()

    def boolean_columns(
        self,
        dataframe: pd.DataFrame
    ) -> list[str]:

        return dataframe.select_dtypes(

            include=["bool"]

        ).columns.tolist()

    def datetime_columns(
        self,
        dataframe: pd.DataFrame
    ) -> list[str]:

        return dataframe.select_dtypes(

            include=["datetime"]

        ).columns.tolist()

    def text_columns(
        self,
        dataframe: pd.DataFrame
    ) -> list[str]:

        return dataframe.select_dtypes(

            include=["object", "string"]

        ).columns.tolist()

    # =====================================================
    # QUALITE
    # =====================================================

    def missing_values(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return int(

            dataframe.isna().sum().sum()

        )

    def duplicate_rows(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return int(

            dataframe.duplicated().sum()

        )

    def unique_values(
        self,
        dataframe: pd.DataFrame,
        column: str
    ) -> int:

        return int(

            dataframe[column].nunique()

        )

    # =====================================================
    # UTILITAIRES
    # =====================================================

    def percentage(
        self,
        value: float,
        total: float
    ) -> float:

        if total == 0:

            return 0.0

        return round(

            value / total * 100,

            2

        )

    def safe_division(
        self,
        numerator: float,
        denominator: float
    ) -> float:

        if denominator == 0:

            return 0.0

        return numerator / denominator

    # =====================================================
    # ABSTRACT
    # =====================================================

    @abstractmethod
    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Chaque analyzer retourne uniquement
        un dictionnaire.
        """

        ...

    # =====================================================
    # EXECUTION
    # =====================================================

    def execute(
        self,
        context: ProfileContext
    ) -> AnalyzerResult:
        """
        Exécute l'analyse et retourne un AnalyzerResult.
        """

        self.validate(context)

        result = AnalyzerResult(
            name=self.name,
            analyzer=self.__class__.__name__,
            version=self.version
        )

        start = perf_counter()

        try:
            analysis = self.analyze(context)

            result.set_result(analysis)

            result.status = "SUCCESS"
            result.success = True

        except Exception as exception:
            result.add_error(str(exception))

        finally:
            result.execution_time = round(
                perf_counter() - start,
                4
            )

            result.finish()

        return result
    # =====================================================
    # CALLABLE
    # =====================================================

    def __call__(
        self,
        dataframe: pd.DataFrame
    ) -> AnalyzerResult:

        return self.execute(
            dataframe
        )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __str__(self):

        return self.name

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(version='{self.version}')"

        )
