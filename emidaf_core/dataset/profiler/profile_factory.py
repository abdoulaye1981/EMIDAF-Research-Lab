"""
=========================================================
EMIDAF Framework v1.0
Profile Factory
---------------------------------------------------------
Fabrique des objets du moteur de profilage.
=========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .profile_context import ProfileContext
from .profile_metadata import ProfileMetadata
from .profile_result import ProfileResult
from .profile_summary import ProfileSummary


class ProfileFactory:
    """
    Fabrique des objets du Profiler.

    Toutes les créations passent
    par cette classe.
    """

    # =====================================================
    # CONTEXT
    # =====================================================

    def create_context(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str = "",
        dataset_path: str | None = None,
        project_name: str = ""
    ) -> ProfileContext:
        """
        Construit un ProfileContext.
        """

        context = ProfileContext(

            dataframe=dataframe,

            dataset_name=dataset_name,

            project_name=project_name

        )

        if dataset_path:

            context.dataset_path = Path(
                dataset_path
            )

        context.dataset_size = int(

            dataframe.memory_usage(

                deep=True

            ).sum()

        )

        return context

    # =====================================================
    # METADATA
    # =====================================================

    def create_metadata(
        self,
        context: ProfileContext
    ) -> ProfileMetadata:
        """
        Construit les métadonnées.
        """

        metadata = ProfileMetadata()

        metadata.dataset_name = (
            context.dataset_name
        )

        metadata.profile_name = (
            context.profile_name
        )

        metadata.memory_usage = (
            context.memory_usage
        )

        metadata.analyzed_rows = (
            context.rows
        )

        metadata.analyzed_columns = (
            context.columns
        )

        metadata.analyzed_cells = (

            context.rows

            *

            context.columns

        )

        return metadata

    # =====================================================
    # SUMMARY
    # =====================================================

    def create_summary(
        self,
        context: ProfileContext
    ) -> ProfileSummary:
        """
        Construit le résumé.
        """

        summary = ProfileSummary()

        summary.rows = context.rows

        summary.columns = context.columns

        summary.cells = (

            context.rows

            *

            context.columns

        )

        summary.memory_usage = (

            context.memory_usage

        )

        return summary

    # =====================================================
    # PROFILE
    # =====================================================

    def create_profile(
        self,
        context: ProfileContext
    ) -> ProfileResult:
        """
        Construit un ProfileResult vide.
        """

        profile = ProfileResult()

        profile.metadata = self.create_metadata(
            context
        )

        profile.summary = self.create_summary(
            context
        )

        return profile