"""
=========================================================
EMIDAF Framework
Normalization Module
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Méthodes de normalisation.

Contient

- MinMax
- MaxAbs
- Unit Norm
- Decimal Scaling
- Robust Scaling
- Quantile Normalization
- Power Normalization

=========================================================
"""

from __future__ import annotations

import pandas as pd

from sklearn.preprocessing import (
    MinMaxScaler,
    MaxAbsScaler,
    Normalizer,
    RobustScaler,
    QuantileTransformer,
    PowerTransformer,
)

from ..common.results import CleaningResult


# ==========================================================
# BASE
# ==========================================================

class BaseNormalizer:

    """
    Classe mère.
    """

    name = ""

    scaler = None

    @classmethod
    def fit(cls, dataframe):

        cls.scaler.fit(dataframe)

        return cls

    @classmethod
    def transform(cls, dataframe):

        values = cls.scaler.transform(dataframe)

        return pd.DataFrame(

            values,

            columns=dataframe.columns,

            index=dataframe.index

        )

    @classmethod
    def fit_transform(cls, dataframe):

        values = cls.scaler.fit_transform(dataframe)

        return pd.DataFrame(

            values,

            columns=dataframe.columns,

            index=dataframe.index

        )

    @classmethod
    def report(cls, before, after):

        return CleaningResult(

            operation="Normalization",

            strategy=cls.name,

            initial_rows=len(before),

            final_rows=len(after),

            initial_columns=before.shape[1],

            final_columns=after.shape[1],

            affected_columns=list(before.columns)

        )


# ==========================================================
# MIN MAX
# ==========================================================

class MinMaxNormalization(BaseNormalizer):

    name = "Min-Max"

    scaler = MinMaxScaler()


# ==========================================================
# MAX ABS
# ==========================================================

class MaxAbsNormalization(BaseNormalizer):

    name = "MaxAbs"

    scaler = MaxAbsScaler()


# ==========================================================
# UNIT NORM
# ==========================================================

class UnitNormNormalization(BaseNormalizer):

    name = "Unit Norm"

    scaler = Normalizer(norm="l2")


# ==========================================================
# ROBUST
# ==========================================================

class RobustNormalization(BaseNormalizer):

    name = "Robust"

    scaler = RobustScaler()


# ==========================================================
# QUANTILE
# ==========================================================

class QuantileNormalization(BaseNormalizer):

    name = "Quantile"

    scaler = QuantileTransformer(

        output_distribution="normal",

        random_state=42

    )


# ==========================================================
# POWER
# ==========================================================

class PowerNormalization(BaseNormalizer):

    name = "Power"

    scaler = PowerTransformer()


# ==========================================================
# DECIMAL SCALING
# ==========================================================

class DecimalScaling(BaseNormalizer):

    """
    Normalisation décimale.

    x' = x / 10^j
    """

    name = "Decimal Scaling"

    @classmethod
    def fit(cls, dataframe):

        cls.factor = 10 ** (

            dataframe.abs()

            .max()

            .astype(str)

            .str.split(".")

            .str[0]

            .str.len()

            .max()

        )

        return cls

    @classmethod
    def transform(cls, dataframe):

        return dataframe / cls.factor

    @classmethod
    def fit_transform(cls, dataframe):

        cls.fit(dataframe)

        return cls.transform(dataframe)


# ==========================================================
# SERVICE
# ==========================================================

class Normalization:

    """
    Interface principale.
    """

    @staticmethod
    def minmax(dataframe):

        return MinMaxNormalization.fit_transform(

            dataframe

        )

    @staticmethod
    def maxabs(dataframe):

        return MaxAbsNormalization.fit_transform(

            dataframe

        )

    @staticmethod
    def unitnorm(dataframe):

        return UnitNormNormalization.fit_transform(

            dataframe

        )

    @staticmethod
    def robust(dataframe):

        return RobustNormalization.fit_transform(

            dataframe

        )

    @staticmethod
    def quantile(dataframe):

        return QuantileNormalization.fit_transform(

            dataframe

        )

    @staticmethod
    def power(dataframe):

        return PowerNormalization.fit_transform(

            dataframe

        )

    @staticmethod
    def decimal(dataframe):

        return DecimalScaling.fit_transform(

            dataframe

        )