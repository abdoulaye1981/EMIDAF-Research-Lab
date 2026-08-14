"""
=========================================================
EMIDAF Framework v1.0
Profile Utils
---------------------------------------------------------
Fonctions utilitaires utilisées par le moteur
de profilage.
=========================================================
"""

from __future__ import annotations

import hashlib
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


# ==========================================================
# TEMPS
# ==========================================================

def execution_time(start: float) -> float:
    """
    Retourne le temps écoulé en secondes.
    """
    return round(time.perf_counter() - start, 4)


# ==========================================================
# POURCENTAGES
# ==========================================================

def percentage(
    value: float,
    total: float,
    decimals: int = 2
) -> float:
    """
    Calcule un pourcentage.
    """

    if total == 0:
        return 0.0

    return round((value / total) * 100, decimals)


def safe_division(
    numerator: float,
    denominator: float,
    default: float = 0.0
) -> float:
    """
    Division sécurisée.
    """

    if denominator == 0:
        return default

    return numerator / denominator


# ==========================================================
# MEMOIRE
# ==========================================================

def bytes_to_kb(size: int) -> float:
    return round(size / 1024, 2)


def bytes_to_mb(size: int) -> float:
    return round(size / (1024 ** 2), 2)


def bytes_to_gb(size: int) -> float:
    return round(size / (1024 ** 3), 2)


def format_bytes(size: int) -> str:
    """
    Formate une taille mémoire.
    """

    if size < 1024:
        return f"{size} B"

    elif size < 1024 ** 2:
        return f"{bytes_to_kb(size)} KB"

    elif size < 1024 ** 3:
        return f"{bytes_to_mb(size)} MB"

    else:
        return f"{bytes_to_gb(size)} GB"


def dataframe_memory(df: pd.DataFrame) -> int:
    """
    Taille mémoire réelle.
    """

    return int(
        df.memory_usage(
            deep=True
        ).sum()
    )


# ==========================================================
# HASH
# ==========================================================

def sha256(file: Path) -> str:
    """
    SHA256 d'un fichier.
    """

    digest = hashlib.sha256()

    with open(file, "rb") as f:

        while True:

            block = f.read(8192)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


# ==========================================================
# DATAFRAME
# ==========================================================

def dataframe_shape(
    df: pd.DataFrame
) -> tuple[int, int]:

    return df.shape


def row_count(df: pd.DataFrame) -> int:

    return int(df.shape[0])


def column_count(df: pd.DataFrame) -> int:

    return int(df.shape[1])


def empty(df: pd.DataFrame) -> bool:

    return df.empty


# ==========================================================
# COLONNES
# ==========================================================

def numeric_columns(
    df: pd.DataFrame
) -> list[str]:

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def categorical_columns(
    df: pd.DataFrame
) -> list[str]:

    return df.select_dtypes(
        include=["category"]
    ).columns.tolist()


def boolean_columns(
    df: pd.DataFrame
) -> list[str]:

    return df.select_dtypes(
        include=["bool"]
    ).columns.tolist()


def datetime_columns(
    df: pd.DataFrame
) -> list[str]:

    return df.select_dtypes(
        include=["datetime"]
    ).columns.tolist()


def object_columns(
    df: pd.DataFrame
) -> list[str]:

    return df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()


# ==========================================================
# QUALITE
# ==========================================================

def missing_values(df: pd.DataFrame) -> int:

    return int(
        df.isna().sum().sum()
    )


def duplicate_rows(df: pd.DataFrame) -> int:

    return int(
        df.duplicated().sum()
    )


def duplicate_ratio(df: pd.DataFrame) -> float:

    return percentage(
        duplicate_rows(df),
        len(df)
    )


def missing_ratio(df: pd.DataFrame) -> float:

    return percentage(
        missing_values(df),
        df.shape[0] * df.shape[1]
    )


# ==========================================================
# CARDINALITE
# ==========================================================

def unique_values(
    df: pd.DataFrame
) -> dict[str, int]:

    return {

        column: int(df[column].nunique(dropna=True))

        for column in df.columns

    }


def constant_columns(
    df: pd.DataFrame
) -> list[str]:

    return [

        column

        for column in df.columns

        if df[column].nunique(dropna=False) == 1

    ]


def empty_columns(
    df: pd.DataFrame
) -> list[str]:

    return [

        column

        for column in df.columns

        if df[column].isna().all()

    ]


# ==========================================================
# STATISTIQUES
# ==========================================================

def entropy(values: pd.Series) -> float:
    """
    Entropie de Shannon.
    """

    probabilities = (
        values.value_counts(normalize=True)
    )

    if probabilities.empty:
        return 0.0

    return float(

        -np.sum(

            probabilities *

            np.log2(probabilities)

        )

    )


def coefficient_variation(
    values: pd.Series
) -> float:

    mean = values.mean()

    if mean == 0:

        return 0.0

    return float(

        values.std() / mean

    )


# ==========================================================
# NORMALISATION
# ==========================================================

def normalize(
    value: float,
    minimum: float,
    maximum: float
) -> float:

    if maximum == minimum:
        return 0.0

    return (

        value - minimum

    ) / (

        maximum - minimum

    )


# ==========================================================
# SCORE
# ==========================================================

def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0
) -> float:

    return max(

        minimum,

        min(

            maximum,

            value

        )

    )


# ==========================================================
# TEXTE
# ==========================================================

def truncate(
    text: Any,
    length: int = 120
) -> str:

    text = str(text)

    if len(text) <= length:
        return text

    return text[:length] + "..."


# ==========================================================
# PATH
# ==========================================================

def ensure_directory(
    directory: Path
) -> None:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )