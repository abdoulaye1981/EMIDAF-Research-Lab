"""
=========================================================
EMIDAF Framework v1.0
Profile Context
---------------------------------------------------------
Contexte d'exécution partagé par tous les analyzers.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(slots=True)
class ProfileContext:
    """
    Contexte partagé par le moteur de profilage.

    Cette classe centralise toutes les informations
    nécessaires à l'exécution des analyzers.

    Chaque analyzer reçoit un ProfileContext au lieu
    d'un simple DataFrame.
    """

    # =====================================================
    # DATASET
    # =====================================================

    dataframe: pd.DataFrame

    dataset_name: str = ""

    dataset_path: Path | None = None

    dataset_format: str = ""

    dataset_size: int = 0

    dataset_encoding: str = "utf-8"

    # =====================================================
    # PROJET
    # =====================================================

    project_name: str = ""

    project_path: Path | None = None

    workspace: Path | None = None

    # =====================================================
    # PROFILER
    # =====================================================

    profile_name: str = ""

    profile_version: str = "1.0.0"

    framework_version: str = "1.0.0"

    # =====================================================
    # EXECUTION
    # =====================================================

    random_state: int = 42

    sample_size: int | None = None

    use_sampling: bool = False

    parallel: bool = False

    max_workers: int = 1

    # =====================================================
    # OPTIONS
    # =====================================================

    options: dict[str, Any] = field(
        default_factory=dict
    )

    configuration: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # CACHE
    # =====================================================

    cache: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # LOGGER
    # =====================================================

    logger: Any = None

    # =====================================================
    # METADATA
    # =====================================================

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # SHARED OBJECTS
    # =====================================================

    shared: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # RESULTS
    # =====================================================

    results: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # DATAFRAME
    # =====================================================

    @property
    def rows(self) -> int:

        return self.dataframe.shape[0]

    @property
    def columns(self) -> int:

        return self.dataframe.shape[1]

    @property
    def shape(self) -> tuple[int, int]:

        return self.dataframe.shape

    @property
    def memory_usage(self) -> int:

        return int(

            self.dataframe.memory_usage(

                deep=True

            ).sum()

        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def set_option(
        self,
        key: str,
        value: Any
    ) -> None:

        self.options[key] = value

    def get_option(
        self,
        key: str,
        default: Any = None
    ) -> Any:

        return self.options.get(

            key,

            default

        )

    # =====================================================
    # CACHE
    # =====================================================

    def put_cache(
        self,
        key: str,
        value: Any
    ) -> None:

        self.cache[key] = value

    def get_cache(
        self,
        key: str,
        default: Any = None
    ) -> Any:

        return self.cache.get(

            key,

            default

        )

    def clear_cache(self) -> None:

        self.cache.clear()

    # =====================================================
    # RESULTS
    # =====================================================

    def add_result(
        self,
        analyzer: str,
        result: Any
    ) -> None:

        self.results[analyzer] = result

    def get_result(
        self,
        analyzer: str
    ) -> Any:

        return self.results.get(analyzer)

    # =====================================================
    # SHARED
    # =====================================================

    def share(
        self,
        name: str,
        value: Any
    ) -> None:

        self.shared[name] = value

    def shared_value(
        self,
        name: str,
        default: Any = None
    ) -> Any:

        return self.shared.get(

            name,

            default

        )

    # =====================================================
    # METADATA
    # =====================================================

    def add_metadata(
        self,
        key: str,
        value: Any
    ) -> None:

        self.metadata[key] = value

    # =====================================================
    # LOGGER
    # =====================================================

    def log(
        self,
        message: str
    ) -> None:

        if self.logger is not None:

            self.logger.info(message)

    # =====================================================
    # SAMPLING
    # =====================================================

    def working_dataframe(
        self
    ) -> pd.DataFrame:
        """
        Retourne le DataFrame utilisé
        par les analyzers.
        """

        if (

            not self.use_sampling

            or

            self.sample_size is None

            or

            self.sample_size >= len(self.dataframe)

        ):

            return self.dataframe

        return self.dataframe.sample(

            n=self.sample_size,

            random_state=self.random_state

        )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self):

        return (

            "ProfileContext("

            f"rows={self.rows}, "

            f"columns={self.columns}, "

            f"sampling={self.use_sampling})"

        )