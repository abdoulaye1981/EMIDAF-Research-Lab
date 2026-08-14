"""
=========================================================
EMIDAF Framework
Base Analyzer
=========================================================

Classe de base de tous les analyzers EMIDAF.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from time import perf_counter

from .analyzer_result import AnalyzerResult
from .base_context import BaseContext


class BaseAnalyzer(ABC):
    """
    Classe mère de tous les analyzers.

    Chaque analyzer suit exactement le même cycle de vie :

        validate()
              ↓
        analyze()
              ↓
        finalize()

    Cette classe s'occupe automatiquement :

    - validation
    - mesure du temps d'exécution
    - capture des erreurs
    - création du AnalyzerResult
    """

    # =====================================================
    # CONFIGURATION
    # =====================================================

    name: str = "BaseAnalyzer"

    version: str = "1.0.0"

    enabled: bool = True

    # =====================================================
    # PUBLIC
    # =====================================================

    def execute(
        self,
        context: BaseContext,
    ) -> AnalyzerResult:
        """
        Lance complètement l'analyse.
        """

        if context is None:

            raise ValueError(

                "context cannot be None."

            )

        result = AnalyzerResult(

            name=self.name,

            analyzer=self.name,

            version=self.version,

        )

        start = perf_counter()

        try:

            self.validate(context)

            result.result = self.analyze(

                context

            )

        except Exception as e:

            result.add_error(

                str(e)

            )

        finally:

            result.execution_time = round(

                perf_counter() - start,

                4

            )

            result.success = (

                result.error_count == 0

            )

            self.finalize(

                context,

                result

            )

        return result

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        context: BaseContext,
    ) -> None:
        """
        Validation.

        Peut être redéfinie.
        """

        return None

    # =====================================================
    # ANALYSIS
    # =====================================================

    @abstractmethod
    def analyze(
        self,
        context: BaseContext,
    ):
        """
        Analyse le contexte.

        Retourne le résultat de l'analyse.
        """
        raise NotImplementedError

    # =====================================================
    # FINALIZATION
    # =====================================================

    def finalize(
        self,
        context: BaseContext,
        result: AnalyzerResult,
    ) -> None:
        """
        Finalisation.

        Peut être redéfinie.
        """

        return None

    # =====================================================
    # UTILITIES
    # =====================================================

    def warning(
        self,
        result: AnalyzerResult,
        message: str,
    ) -> None:

        result.add_warning(message)

    def error(
        self,
        result: AnalyzerResult,
        message: str,
    ) -> None:

        result.add_error(message)

    def recommendation(
        self,
        result: AnalyzerResult,
        message: str,
    ) -> None:

        result.add_recommendation(message)

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def is_enabled(self) -> bool:

        return self.enabled

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __str__(self) -> str:

        return self.name

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"version='{self.version}')"

        )