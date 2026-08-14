"""
=========================================================
EMIDAF Framework
Probability Distribution Base Classes
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

class DistributionResult:

    ###################################################

    distribution:str=""

    ###################################################

    parameters:tuple=()

    ###################################################

    log_likelihood:float|None=None

    aic:float|None=None

    bic:float|None=None

    ###################################################

    statistic:float|None=None

    p_value:float|None=None

    ###################################################

    sample=None

    ###################################################

    metadata:dict=field(

        default_factory=dict

    )

class BaseDistribution(

    ABC

):

    name="Distribution"

    @abstractmethod

    def fit(

        self,

        data,

    ):

        ...

    @abstractmethod

    def pdf(

        self,

        x,

    ):

        ...

    @abstractmethod

    def cdf(

        self,

        x,

    ):

        ...

    @abstractmethod

    def ppf(

        self,

        q,

    ):

        ...

    @abstractmethod

    def rvs(

        self,

        size,

    ):

        ...