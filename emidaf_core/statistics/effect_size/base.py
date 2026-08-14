"""
=========================================================
EMIDAF Framework
Effect Size Base Classes
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass
from dataclasses import field

@dataclass(slots=True)

class EffectSizeResult:

    ###################################################

    name:str=""

    ###################################################

    statistic:float|None=None

    ###################################################

    interpretation:str=""

    ###################################################

    magnitude:str=""

    ###################################################

    confidence_interval:tuple|None=None

    ###################################################

    metadata:dict=field(

        default_factory=dict

    )

class BaseEffectSize(

    ABC

):

    name="Effect Size"

    @abstractmethod

    def compute(

        self,

        *args,

        **kwargs,

    ):

        ...

class EffectSize:

    pass