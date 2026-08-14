"""
=========================================================
EMIDAF Framework
Base Engine
=========================================================

Classe de base de tous les moteurs EMIDAF.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from time import perf_counter
from typing import Any

from .base_context import BaseContext


class BaseEngine(ABC):
    """
    Classe mère de tous les moteurs EMIDAF.

    Cette classe implémente le cycle de vie standard :

        initialize()
            ↓
        validate()
            ↓
        create_context()
            ↓
        run()
            ↓
        finalize()
    """

    # =====================================================
    # PUBLIC
    # =====================================================

    def execute(
        self,
        *args,
        **kwargs,
    ) -> Any:
        """
        Lance complètement le moteur.
        """

        start = perf_counter()

        self.initialize()

        self.validate(*args, **kwargs)

        context = self.create_context(
            *args,
            **kwargs
        )

        result = self.run(context)

        execution_time = round(
            perf_counter() - start,
            4
        )

        self._store_execution_time(
            result,
            execution_time
        )

        self.finalize(
            context,
            result
        )

        return result

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self) -> None:
        """
        Initialisation du moteur.
        """

        return None

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Validation des paramètres.
        """

        return None

    # =====================================================
    # CONTEXT
    # =====================================================

    @abstractmethod
    def create_context(
        self,
        *args,
        **kwargs,
    ) -> BaseContext:
        """
        Crée le contexte d'exécution.
        """
        raise NotImplementedError

    # =====================================================
    # EXECUTION
    # =====================================================

    @abstractmethod
    def run(
        self,
        context: BaseContext,
    ) -> Any:
        """
        Exécute le moteur.
        """
        raise NotImplementedError

    # =====================================================
    # FINALIZATION
    # =====================================================

    def finalize(
        self,
        context: BaseContext,
        result: Any,
    ) -> None:
        """
        Finalisation du moteur.
        """

        return None

    # =====================================================
    # INTERNAL
    # =====================================================

    @staticmethod
    def _store_execution_time(
        result: Any,
        execution_time: float,
    ) -> None:
        """
        Enregistre le temps d'exécution dans le résultat.

        Compatible avec :
        - BaseResult
        - ProfileResult
        - tout autre objet résultat
        """

        if result is None:
            return

        # Cas 1 : BaseResult
        if hasattr(result, "execution_time"):

            result.execution_time = execution_time

            return

        # Cas 2 : ProfileResult
        if (

            hasattr(result, "metadata")

            and

            hasattr(result.metadata, "execution_time")

        ):

            result.metadata.execution_time = execution_time

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return self.__class__.__name__