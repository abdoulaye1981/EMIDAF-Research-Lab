"""
=========================================================
EMIDAF Framework
Preprocessing - Interpretation
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def interpret_missing_percentage(
    percentage
):

    if percentage == 0:

        return "Aucune valeur manquante."

    if percentage < 5:

        return "Taux de valeurs manquantes faible."

    if percentage < 20:

        return "Taux de valeurs manquantes modéré."

    if percentage < 50:

        return "Taux de valeurs manquantes élevé."

    return "Taux de valeurs manquantes très élevé."


def interpret_skewness(
    value
):

    if pd.isna(value):

        return "Non interprétable."

    value = abs(value)

    if value < 0.5:

        return "Distribution approximativement symétrique."

    if value < 1:

        return "Asymétrie modérée."

    return "Asymétrie forte."


def interpret_kurtosis(
    value
):

    if pd.isna(value):

        return "Non interprétable."

    if abs(value) < 0.5:

        return "Kurtosis proche de celle d'une distribution normale."

    if value > 0:

        return "Distribution plus pointue que la normale."

    return "Distribution plus aplatie que la normale."


def interpret_coefficient_variation(
    value
):

    if pd.isna(value):

        return "Non interprétable."

    value = abs(value)

    if value < 10:

        return "Faible dispersion."

    if value < 20:

        return "Dispersion modérée."

    return "Dispersion élevée."


def interpret_vif(
    value
):

    if pd.isna(value):

        return "Non interprétable."

    if np.isinf(value):

        return "Multicolinéarité extrêmement élevée."

    if value < 5:

        return "Pas de problème majeur de multicolinéarité."

    if value < 10:

        return "Multicolinéarité potentiellement importante."

    return "Multicolinéarité élevée."


def interpret_correlation(
    value
):

    if pd.isna(value):

        return "Corrélation non disponible."

    value = abs(value)

    if value < 0.2:

        return "Corrélation très faible."

    if value < 0.4:

        return "Corrélation faible."

    if value < 0.7:

        return "Corrélation modérée."

    if value < 0.9:

        return "Corrélation forte."

    return "Corrélation très forte."


def interpret_imbalance_ratio(
    value
):

    if pd.isna(value):

        return "Non interprétable."

    if value < 1.5:

        return "Classes relativement équilibrées."

    if value < 3:

        return "Déséquilibre modéré."

    if value < 5:

        return "Déséquilibre important."

    return "Déséquilibre très important."


def interpret_numeric_variable(
    series
):

    result = {}

    result["missing_percentage"] = (
        series.isna().mean() * 100
    )

    result["missing_interpretation"] = (
        interpret_missing_percentage(
            result["missing_percentage"]
        )
    )

    result["skewness"] = series.skew()

    result["skewness_interpretation"] = (
        interpret_skewness(
            result["skewness"]
        )
    )

    result["kurtosis"] = series.kurtosis()

    result["kurtosis_interpretation"] = (
        interpret_kurtosis(
            result["kurtosis"]
        )
    )

    mean = series.mean()

    if mean != 0:

        cv = (
            series.std()
            / mean
            * 100
        )

    else:

        cv = np.nan

    result["coefficient_variation"] = cv

    result["cv_interpretation"] = (
        interpret_coefficient_variation(
            cv
        )
    )

    return result


def interpret_vif_table(
    vif_table
):

    result = vif_table.copy()

    result["interpretation"] = (
        result["VIF"]
        .apply(
            interpret_vif
        )
    )

    return result


def interpret_missing_table(
    missing_table
):

    result = missing_table.copy()

    result["interpretation"] = (
        result["missing_percentage"]
        .apply(
            interpret_missing_percentage
        )
    )

    return result
