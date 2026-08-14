"""
=========================================================
EMIDAF Framework
Frequency Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Statistiques de fréquence.

Contient :

- Count
- MissingCount
- MissingPercentage
- UniqueCount
- DistinctCount
- DuplicateCount
- DuplicatePercentage
- FrequencyTable
- RelativeFrequency
=========================================================
"""

from __future__ import annotations

from abc import ABC

import pandas as pd

from ..base.descriptive_statistic import DescriptiveStatistic
from .validator import StatisticsValidator


class FrequencyStatistic(DescriptiveStatistic, ABC):
    """
    Classe mère des statistiques de fréquence.
    """

    category = "Frequency"


# =====================================================
# COUNT
# =====================================================

class Count(FrequencyStatistic):

    name = "Count"

    description = "Number of observations"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        return int(len(values))


# =====================================================
# MISSING COUNT
# =====================================================

class MissingCount(FrequencyStatistic):

    name = "Missing Count"

    description = "Missing values"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        return int(values.isna().sum())


# =====================================================
# MISSING PERCENTAGE
# =====================================================

class MissingPercentage(FrequencyStatistic):

    name = "Missing Percentage"

    description = "Percentage of missing values"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        total = len(values)

        if total == 0:

            return 0.0

        return float(

            values.isna().sum()

            / total

            * 100

        )


# =====================================================
# UNIQUE COUNT
# =====================================================

class UniqueCount(FrequencyStatistic):

    name = "Unique Count"

    description = "Number of unique values"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        return int(

            values.nunique()

        )


# =====================================================
# DISTINCT COUNT
# =====================================================

class DistinctCount(FrequencyStatistic):

    name = "Distinct Count"

    description = "Distinct values"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        return int(

            values.drop_duplicates().shape[0]

        )


# =====================================================
# DUPLICATE COUNT
# =====================================================

class DuplicateCount(FrequencyStatistic):

    name = "Duplicate Count"

    description = "Duplicated observations"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        return int(

            values.duplicated().sum()

        )


# =====================================================
# DUPLICATE PERCENTAGE
# =====================================================

class DuplicatePercentage(FrequencyStatistic):

    name = "Duplicate Percentage"

    description = "Percentage of duplicated values"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        total = len(values)

        if total == 0:

            return 0.0

        return float(

            values.duplicated().sum()

            / total

            * 100

        )


# =====================================================
# FREQUENCY TABLE
# =====================================================

class FrequencyTable(FrequencyStatistic):

    name = "Frequency Table"

    description = "Absolute frequencies"

    @classmethod
    def compute(
        cls,
        values,
        normalize: bool = False,
        dropna: bool = False,
    ):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        table = values.value_counts(

            normalize=normalize,

            dropna=dropna

        )

        return table.to_dict()


# =====================================================
# RELATIVE FREQUENCY
# =====================================================

class RelativeFrequency(FrequencyStatistic):

    name = "Relative Frequency"

    description = "Relative frequencies"

    @classmethod
    def compute(
        cls,
        values,
    ):

        return FrequencyTable.compute(

            values,

            normalize=True

        )


# =====================================================
# SERVICE
# =====================================================

class FrequencyStatistics:
    """
    Calcul de toutes les statistiques de fréquence.
    """

    @staticmethod
    def compute(values):

        values = StatisticsValidator.series(
            values,
            drop_na=False
        )

        return {

            "count":

                Count.compute(values),

            "missing_count":

                MissingCount.compute(values),

            "missing_percentage":

                MissingPercentage.compute(values),

            "unique_count":

                UniqueCount.compute(values),

            "distinct_count":

                DistinctCount.compute(values),

            "duplicate_count":

                DuplicateCount.compute(values),

            "duplicate_percentage":

                DuplicatePercentage.compute(values),

            "frequency_table":

                FrequencyTable.compute(values),

            "relative_frequency":

                RelativeFrequency.compute(values)

        }