"""
=========================================================
EMIDAF Framework
Base Builder
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .base_object import BaseObject


class BaseBuilder(BaseObject, ABC):
    """
    Classe mère de tous les builders EMIDAF.
    """

    def __init__(self) -> None:

        super().__init__()

        self.reset()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self) -> None:
        """
        Réinitialise le builder.
        """
        self._result = None

    # =====================================================
    # BUILD
    # =====================================================

    @abstractmethod
    def build(
        self,
        *args,
        **kwargs,
    ):
        """
        Construit le résultat final.
        """
        raise NotImplementedError

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(self) -> None:
        """
        Validation du résultat construit.
        """
        if self._result is None:

            raise RuntimeError(

                "No result has been built."

            )

    # =====================================================
    # FINALIZE
    # =====================================================

    def finalize(self):

        self.validate()

        return self._result