"""
=========================================================
EMIDAF Framework
Inferential Statistics Base Classes
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

class InferentialResult:

    ####################################################

    test:str=""

    statistic:float|None=None

    p_value:float|None=None

    alpha:float=0.05

    ####################################################

    reject_null:bool=False

    ####################################################

    confidence_interval:tuple|None=None

    ####################################################

    effect_size:float|None=None

    power:float|None=None

    ####################################################

    interpretation:str=""

    recommendation:str=""

    ####################################################

    metadata:dict=field(

        default_factory=dict

    )

class BaseInferentialTest(

    ABC

):

    name="Inferential Test"

    @abstractmethod

    def compute(

        self,

        *args,

        **kwargs,

    ):

        ...