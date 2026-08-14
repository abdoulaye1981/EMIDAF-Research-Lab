"""
=========================================================
EMIDAF Framework v1.0
Profile Validator
---------------------------------------------------------
Validation des DataFrames, des résultats de profilage
et des objets métier.
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from .profile_result import ProfileResult
from .profile_summary import ProfileSummary
from .profile_metadata import ProfileMetadata
from .profile_exceptions import (
    EmptyDatasetError,
    InvalidDataFrameError,
    InvalidDatasetError,
    InvalidProfileError,
)


class ProfileValidator:
    """
    Validation des objets manipulés par le Profiler.

    Cette classe ne réalise aucun calcul statistique.

    Elle vérifie uniquement la cohérence des données.
    """

    # =====================================================
    # DATAFRAME
    # =====================================================

    def validate_dataframe(
        self,
        dataframe: Any
    ) -> None:
        """
        Vérifie que l'objet est un DataFrame valide.
        """

        if dataframe is None:
            raise InvalidDataFrameError()

        if not isinstance(dataframe, pd.DataFrame):
            raise InvalidDataFrameError()

        if dataframe.empty:
            raise EmptyDatasetError()

    # =====================================================
    # STRUCTURE
    # =====================================================

    def validate_columns(
        self,
        dataframe: pd.DataFrame
    ) -> None:
        """
        Vérifie que le DataFrame possède au moins
        une colonne.
        """

        if dataframe.shape[1] == 0:
            raise InvalidDatasetError(
                "The dataset contains no columns."
            )

    def validate_rows(
        self,
        dataframe: pd.DataFrame
    ) -> None:
        """
        Vérifie que le DataFrame possède
        au moins une ligne.
        """

        if dataframe.shape[0] == 0:
            raise EmptyDatasetError()

    def validate_duplicate_columns(
        self,
        dataframe: pd.DataFrame
    ) -> None:
        """
        Vérifie les noms de colonnes.
        """

        duplicated = dataframe.columns.duplicated()

        if duplicated.any():

            columns = dataframe.columns[duplicated]

            raise InvalidDatasetError(

                "Duplicated column names detected : "

                + ", ".join(columns)

            )

    # =====================================================
    # TYPES
    # =====================================================

    def validate_dtypes(
        self,
        dataframe: pd.DataFrame
    ) -> None:
        """
        Vérifie les types des colonnes.
        """

        for column in dataframe.columns:

            dtype = dataframe[column].dtype

            if dtype is None:

                raise InvalidDatasetError(

                    f"Invalid dtype for '{column}'."

                )

    # =====================================================
    # MEMOIRE
    # =====================================================

    def validate_memory(
        self,
        dataframe: pd.DataFrame,
        max_memory: int | None = None
    ) -> None:
        """
        Vérifie la consommation mémoire.

        max_memory exprimée en octets.
        """

        if max_memory is None:
            return

        memory = int(

            dataframe.memory_usage(

                deep=True

            ).sum()

        )

        if memory > max_memory:

            raise InvalidDatasetError(

                "Dataset exceeds the authorized memory."

            )

    # =====================================================
    # PROFIL
    # =====================================================

    def validate_profile(
        self,
        profile: ProfileResult
    ) -> None:
        """
        Vérifie un ProfileResult.
        """

        if profile is None:

            raise InvalidProfileError()

        if not isinstance(

            profile,

            ProfileResult

        ):

            raise InvalidProfileError()

        self.validate_metadata(

            profile.metadata

        )

        self.validate_summary(

            profile.summary

        )

    # =====================================================
    # METADATA
    # =====================================================

    def validate_metadata(
        self,
        metadata: ProfileMetadata
    ) -> None:
        """
        Vérifie les métadonnées.
        """

        if metadata is None:

            raise InvalidProfileError()

        if not isinstance(

            metadata,

            ProfileMetadata

        ):

            raise InvalidProfileError()

    # =====================================================
    # SUMMARY
    # =====================================================

    def validate_summary(
        self,
        summary: ProfileSummary
    ) -> None:
        """
        Vérifie le résumé.
        """

        if summary is None:

            raise InvalidProfileError()

        if not isinstance(

            summary,

            ProfileSummary

        ):

            raise InvalidProfileError()

    # =====================================================
    # ANALYZERS
    # =====================================================

    def validate_analyzer_result(
        self,
        result: dict
    ) -> None:
        """
        Vérifie le résultat retourné
        par un Analyzer.
        """

        if not isinstance(

            result,

            dict

        ):

            raise InvalidProfileError(

                "Analyzer must return a dictionary."

            )

    # =====================================================
    # GLOBAL
    # =====================================================

    def validate(
        self,
        dataframe: pd.DataFrame
    ) -> None:
        """
        Validation complète du DataFrame.
        """

        self.validate_dataframe(dataframe)

        self.validate_rows(dataframe)

        self.validate_columns(dataframe)

        self.validate_duplicate_columns(dataframe)

        self.validate_dtypes(dataframe)

    # =====================================================
    # SCORES
    # =====================================================

    def validate_score(
        self,
        value: float
    ) -> float:
        """
        Vérifie qu'un score est compris
        entre 0 et 100.
        """

        if value < 0:
            return 0.0

        if value > 100:
            return 100.0

        return float(value)

    # =====================================================
    # UTILITAIRE
    # =====================================================

    def is_valid_dataframe(
        self,
        dataframe: Any
    ) -> bool:
        """
        Validation booléenne.
        """

        try:

            self.validate(dataframe)

            return True

        except Exception:

            return False

    def is_valid_profile(
        self,
        profile: Any
    ) -> bool:
        """
        Validation booléenne.
        """

        try:

            self.validate_profile(profile)

            return True

        except Exception:

            return False