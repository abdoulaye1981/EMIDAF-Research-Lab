"""
=========================================================
EMIDAF Framework
Outlier Treatment
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Traitement des valeurs aberrantes.

Contient

- Remove Outliers
- Winsorization
- Capping
- Flooring
- Mean Replacement
- Median Replacement
- Quantile Capping
- Adaptive Treatment

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ...common.results import CleaningResult


def _validate_bounds(
    lower,
    upper,
):
    """
    Vérifie la cohérence des bornes.
    """

    if lower > upper:
        raise ValueError(
            "lower must be less than or equal to upper."
        )


def _validate_mask(
    dataframe,
    mask,
):
    """
    Valide et aligne un masque d'observations.

    Un masque pandas doit avoir exactement le même index
    que le DataFrame. Les autres objets array-like sont
    acceptés s'ils ont exactement la bonne longueur.
    """

    if isinstance(
        mask,
        pd.Series,
    ):

        if len(mask) != len(dataframe):
            raise ValueError(
                "mask must have the same length "
                "as the dataframe."
            )

        if not mask.index.equals(
            dataframe.index
        ):
            raise ValueError(
                "mask index must match "
                "the dataframe index."
            )

        if mask.isna().any():
            raise ValueError(
                "mask cannot contain missing values."
            )

        return mask.astype(bool)

    values = np.asarray(mask)

    if (
        values.ndim != 1
        or len(values) != len(dataframe)
    ):
        raise ValueError(
            "mask must have the same length "
            "as the dataframe."
        )

    return pd.Series(
        values.astype(bool),
        index=dataframe.index,
    )



# ==========================================================
# BASE
# ==========================================================

class BaseTreatment:
    """
    Classe mère des traitements.
    """

    name = ""

    @classmethod
    def build_result(

        cls,

        before,

        after,

        column,

        strategy,

    ):

        return CleaningResult(

            operation="Outlier Treatment",

            strategy=strategy,

            initial_rows=len(before),

            final_rows=len(after),

            removed_rows=len(before)-len(after),

            initial_columns=before.shape[1],

            final_columns=after.shape[1],

            removed_columns=0,

            affected_columns=[column]

        )


# ==========================================================
# REMOVE
# ==========================================================

class RemoveOutliers(BaseTreatment):

    name = "Remove"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        lower,
        upper,
    ):

        _validate_bounds(
            lower,
            upper,
        )

        before = dataframe.copy()

        after = dataframe.loc[
            (dataframe[column] >= lower)
            &
            (dataframe[column] <= upper)
        ]

        result = cls.build_result(
            before,
            after,
            column,
            "Remove"
        )

        return after, result


# ==========================================================
# WINSORIZATION
# ==========================================================

class Winsorization(BaseTreatment):

    name = "Winsorization"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        lower,
        upper,
    ):

        _validate_bounds(
            lower,
            upper,
        )

        before = dataframe.copy()
        after = dataframe.copy()

        after[column] = after[column].clip(
            lower,
            upper
        )

        result = cls.build_result(
            before,
            after,
            column,
            "Winsorization"
        )

        return after, result


# ==========================================================
# CAPPING
# ==========================================================

class Capping(BaseTreatment):

    name = "Capping"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        lower,
        upper,
    ):

        _validate_bounds(
            lower,
            upper,
        )

        before = dataframe.copy()
        after = dataframe.copy()

        after[column] = after[column].clip(
            lower,
            upper
        )

        result = cls.build_result(
            before,
            after,
            column,
            "Capping"
        )

        return after, result


# ==========================================================
# FLOORING
# ==========================================================

class Flooring(BaseTreatment):

    name = "Flooring"

    @classmethod
    def apply(

        cls,

        dataframe,

        column,

        lower,

    ):

        before = dataframe.copy()

        after = dataframe.copy()

        after[column] = np.maximum(

            after[column],

            lower

        )

        result = cls.build_result(

            before,

            after,

            column,

            "Flooring"

        )

        return after, result


# ==========================================================
# MEAN REPLACEMENT
# ==========================================================

class MeanReplacement(BaseTreatment):

    name = "Mean"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        mask,
    ):

        mask = _validate_mask(
            dataframe,
            mask,
        )

        if mask.all():
            raise ValueError(
                "Mean replacement requires "
                "at least one non-outlier observation."
            )

        before = dataframe.copy()
        after = dataframe.copy()

        mean = after.loc[
            ~mask,
            column
        ].mean()

        after.loc[
            mask,
            column
        ] = mean

        result = cls.build_result(
            before,
            after,
            column,
            "Mean Replacement"
        )

        return after, result


# ==========================================================
# MEDIAN REPLACEMENT
# ==========================================================

class MedianReplacement(BaseTreatment):

    name = "Median"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        mask,
    ):

        mask = _validate_mask(
            dataframe,
            mask,
        )

        if mask.all():
            raise ValueError(
                "Median replacement requires "
                "at least one non-outlier observation."
            )

        before = dataframe.copy()
        after = dataframe.copy()

        median = after.loc[
            ~mask,
            column
        ].median()

        after.loc[
            mask,
            column
        ] = median

        result = cls.build_result(
            before,
            after,
            column,
            "Median Replacement"
        )

        return after, result


# ==========================================================
# QUANTILE CAPPING
# ==========================================================

class QuantileCapping(BaseTreatment):

    name = "Quantile"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        q_low=.01,
        q_high=.99,
    ):

        if not (
            0 <= q_low < q_high <= 1
        ):
            raise ValueError(
                "Quantiles must satisfy "
                "0 <= q_low < q_high <= 1."
            )

        lower = dataframe[column].quantile(
            q_low
        )

        upper = dataframe[column].quantile(
            q_high
        )

        return Winsorization.apply(
            dataframe,
            column,
            lower,
            upper
        )


# ==========================================================
# ADAPTIVE TREATMENT
# ==========================================================

class AdaptiveTreatment(BaseTreatment):

    """
    Choix automatique.

    <1%

        Remove

    1-5%

        Winsorization

    >5%

        Median
    """

    name = "Adaptive"

    @classmethod
    def apply(
        cls,
        dataframe,
        column,
        mask,
    ):

        mask = _validate_mask(
            dataframe,
            mask,
        )

        ratio = mask.mean()

        if ratio < 0.01:

            before = dataframe.copy()

            after = dataframe.loc[
                ~mask
            ].copy()

            result = cls.build_result(
                before,
                after,
                column,
                "Remove"
            )

            return after, result

        if ratio < 0.05:

            return Winsorization.apply(
                dataframe,
                column,
                dataframe[column].quantile(.01),
                dataframe[column].quantile(.99)
            )

        return MedianReplacement.apply(
            dataframe,
            column,
            mask
        )


# ==========================================================
# SERVICE
# ==========================================================

class OutlierTreatment:

    """
    Service principal.

    Toutes les méthodes de traitement.
    """

    @staticmethod
    def remove(

        dataframe,

        column,

        lower,

        upper,

    ):

        return RemoveOutliers.apply(

            dataframe,

            column,

            lower,

            upper

        )

    @staticmethod
    def winsorize(

        dataframe,

        column,

        lower,

        upper,

    ):

        return Winsorization.apply(

            dataframe,

            column,

            lower,

            upper

        )

    @staticmethod
    def cap(

        dataframe,

        column,

        lower,

        upper,

    ):

        return Capping.apply(

            dataframe,

            column,

            lower,

            upper

        )

    @staticmethod
    def floor(

        dataframe,

        column,

        lower,

    ):

        return Flooring.apply(

            dataframe,

            column,

            lower

        )

    @staticmethod
    def mean(

        dataframe,

        column,

        mask,

    ):

        return MeanReplacement.apply(

            dataframe,

            column,

            mask

        )

    @staticmethod
    def median(

        dataframe,

        column,

        mask,

    ):

        return MedianReplacement.apply(

            dataframe,

            column,

            mask

        )

    @staticmethod
    def quantile(

        dataframe,

        column,

        q_low=.01,

        q_high=.99,

    ):

        return QuantileCapping.apply(

            dataframe,

            column,

            q_low,

            q_high

        )

    @staticmethod
    def adaptive(

        dataframe,

        column,

        mask,

    ):

        return AdaptiveTreatment.apply(

            dataframe,

            column,

            mask

        )
