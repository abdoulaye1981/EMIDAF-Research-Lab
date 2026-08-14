"""
=========================================================
EMIDAF Framework
Base Context
=========================================================

Classe de base de tous les Context du framework.

Tous les modules héritent de cette classe :

- ProfileContext
- MissingContext
- OutlierContext
- CorrelationContext
- NormalityContext
- CleaningContext
- MLContext

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from .base_object import BaseObject
from .cache import Cache
from .configuration import Configuration
from .logger import Logger


class BaseContext(BaseObject):
    """
    Contexte partagé pendant l'exécution d'un moteur.

    Cette classe ne réalise aucun calcul.
    Elle stocke uniquement l'état partagé entre les analyzers.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        super().__init__()

        if dataframe is None:
            raise ValueError("dataframe cannot be None.")

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas.DataFrame.")

        # =====================================================
        # DATAFRAME
        # =====================================================

        self._original_dataframe = dataframe.copy(deep=True)

        self._dataframe = dataframe.copy(deep=True)

        # =====================================================
        # FRAMEWORK COMPONENTS
        # =====================================================

        self._configuration = Configuration()

        self._logger = Logger()

        self._cache = Cache()

        # =====================================================
        # SHARED EXECUTION STATE
        # =====================================================

        self._results: dict[str, Any] = {}

        self._shared: dict[str, Any] = {}

        self._statistics: dict[str, Any] = {}

    # =====================================================
    # DATAFRAME
    # =====================================================

    @property
    def dataframe(self) -> pd.DataFrame:
        """
        DataFrame courant.
        """
        return self._dataframe

    @dataframe.setter
    def dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas.DataFrame.")

        self._dataframe = dataframe

    @property
    def original_dataframe(self) -> pd.DataFrame:
        """
        DataFrame original.
        """
        return self._original_dataframe

    @property
    def shape(self) -> tuple[int, int]:
        return self._dataframe.shape

    @property
    def rows(self) -> int:
        return self.shape[0]

    @property
    def columns(self) -> int:
        return self.shape[1]

    @property
    def column_names(self) -> list[str]:
        return self._dataframe.columns.tolist()

    # =====================================================
    # CONFIGURATION
    # =====================================================

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    # =====================================================
    # LOGGER
    # =====================================================

    @property
    def logger(self) -> Logger:
        return self._logger

    # =====================================================
    # CACHE
    # =====================================================

    @property
    def cache(self) -> Cache:
        return self._cache

    def put_cache(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._cache.put(key, value)

    def get_cache(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._cache.get(key, default)

    def has_cache(
        self,
        key: str,
    ) -> bool:

        return self._cache.exists(key)

    def clear_cache(self) -> None:

        self._cache.clear()

    # =====================================================
    # RESULTS
    # =====================================================

    @property
    def results(self) -> dict[str, Any]:
        return self._results

    def add_result(
        self,
        name: str,
        result: Any,
    ) -> None:

        self._results[name] = result

    def get_result(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self._results.get(name, default)

    def clear_results(self) -> None:

        self._results.clear()

    # =====================================================
    # SHARED DATA
    # =====================================================

    @property
    def shared(self) -> dict[str, Any]:
        return self._shared

    def put(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._shared[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._shared.get(key, default)

    def clear_shared(self) -> None:

        self._shared.clear()

    # =====================================================
    # STATISTICS
    # =====================================================

    @property
    def statistics(self) -> dict[str, Any]:
        return self._statistics

    def set_statistic(
        self,
        name: str,
        value: Any,
    ) -> None:

        self._statistics[name] = value

    def get_statistic(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self._statistics.get(name, default)

    def clear_statistics(self) -> None:

        self._statistics.clear()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self) -> None:
        """
        Réinitialise uniquement l'état d'exécution.
        Le DataFrame est conservé.
        """

        self.clear_cache()

        self.clear_results()

        self.clear_shared()

        self.clear_statistics()

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(self) -> dict[str, Any]:

        data = super().to_dict()

        data.update({

            "rows": self.rows,

            "columns": self.columns,

            "shape": self.shape,

            "column_names": self.column_names,

            "cache_size": self.cache.size,

            "results": list(self.results.keys()),

            "statistics": list(self.statistics.keys()),

        })

        return data

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(rows={self.rows}, "

            f"columns={self.columns})"

        )