"""
=========================================================
EMIDAF Framework
Power Analysis Base Classes
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

class PowerResult:

    ###################################################

    test:str=""

    ###################################################

    effect_size:float|None=None

    ###################################################

    alpha:float|None=None

    ###################################################

    power:float|None=None

    ###################################################

    sample_size:float|None=None

    ###################################################

    alternative:str="two-sided"

    ###################################################

    metadata:dict=field(

        default_factory=dict

    )
class BasePowerAnalysis(

    ABC

):

    name="Power Analysis"

    @abstractmethod

    def solve(

        self,

        *args,

        **kwargs,

    ):

        ...

class PowerAnalysis:

    pass