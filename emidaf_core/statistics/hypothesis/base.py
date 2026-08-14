"""
=========================================================
EMIDAF Framework
Hypothesis Testing - Base
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .result import HypothesisResult


class BaseHypothesisTest(ABC):

    name = "Base Hypothesis Test"

    def __init__(
        self,
        alpha=0.05
    ):

        if not 0 < alpha < 1:

            raise ValueError(
                "alpha doit être compris entre 0 et 1."
            )

        self.alpha = alpha
        self.result = None

    @abstractmethod
    def test(
        self,
        *args,
        **kwargs
    ) -> HypothesisResult:

        pass

    def _create_result(
        self,
        statistic=None,
        p_value=None,
        null_hypothesis="",
        alternative_hypothesis="",
        details=None
    ):

        result = HypothesisResult(
            test_name=self.name,
            statistic=statistic,
            p_value=p_value,
            alpha=self.alpha,
            null_hypothesis=null_hypothesis,
            alternative_hypothesis=
                alternative_hypothesis,
            details=details or {}
        )

        self.result = result

        return result

    @property
    def significant(self):

        if self.result is None:

            return None

        return self.result.significant

    @property
    def p_value(self):

        if self.result is None:

            return None

        return self.result.p_value

    @property
    def statistic(self):

        if self.result is None:

            return None

        return self.result.statistic

    def summary(self):

        if self.result is None:

            return None

        return self.result.summary()

    def to_dict(self):

        if self.result is None:

            return None

        return self.result.to_dict()
