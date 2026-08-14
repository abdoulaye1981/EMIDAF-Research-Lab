"""
=========================================================
EMIDAF Framework
Base Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe mère de tous les résultats produits
par EMIDAF.

Tous les objets retournés par le framework
héritent de cette classe.

Exemples
---------
DescriptiveResult
CorrelationResult
HypothesisResult
OutlierResult
CleaningResult
VisualizationResult
ModelResult
=========================================================
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from datetime import datetime

import json

import pandas as pd


@dataclass(slots=True)
class BaseResult:
    """
    Classe mère de tous les résultats EMIDAF.
    """

    # =====================================================
    # Metadata
    # =====================================================

    name: str = ""

    category: str = ""

    description: str = ""

    success: bool = True

    execution_time: float = 0.0

    timestamp: str = field(

        default_factory=lambda:

        datetime.now().isoformat()

    )

    metadata: dict = field(

        default_factory=dict

    )

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:
        """
        Conversion en dictionnaire.
        """

        return asdict(self)

    # =====================================================

    def to_json(
        self,
        indent: int = 4,
    ) -> str:
        """
        Conversion JSON.
        """

        return json.dumps(

            self.to_dict(),

            indent=indent,

            default=str,

            ensure_ascii=False

        )

    # =====================================================

    def to_dataframe(self) -> pd.DataFrame:
        """
        Conversion DataFrame.
        """

        return pd.DataFrame(

            [self.to_dict()]

        )

    # =====================================================

    def to_series(self) -> pd.Series:
        """
        Conversion Series.
        """

        return pd.Series(

            self.to_dict()

        )

    # =====================================================

    def keys(self):

        return self.to_dict().keys()

    # =====================================================

    def values(self):

        return self.to_dict().values()

    # =====================================================

    def items(self):

        return self.to_dict().items()

    # =====================================================

    def update(
        self,
        **kwargs,
    ):
        """
        Mise à jour dynamique.
        """

        for key, value in kwargs.items():

            setattr(

                self,

                key,

                value

            )

    # =====================================================

    def get(
        self,
        key,
        default=None,
    ):

        return getattr(

            self,

            key,

            default

        )

    # =====================================================

    def copy(self):
        """
        Copie profonde.
        """

        return self.__class__(

            **self.to_dict()

        )

    # =====================================================

    def clear_metadata(self):

        self.metadata.clear()

    # =====================================================

    def add_metadata(
        self,
        key,
        value,
    ):

        self.metadata[key] = value

    # =====================================================

    def has_metadata(
        self,
        key,
    ):

        return key in self.metadata

    # =====================================================

    def merge_metadata(
        self,
        other: dict,
    ):

        self.metadata.update(other)

    # =====================================================
    # Display
    # =====================================================

    def summary(self):

        return {

            "name": self.name,

            "category": self.category,

            "success": self.success,

            "execution_time": self.execution_time

        }

    # =====================================================

    def __getitem__(self, key):

        return getattr(self, key)

    # =====================================================

    def __contains__(self, key):

        return hasattr(self, key)

    # =====================================================

    def __len__(self):

        return len(

            self.to_dict()

        )

    # =====================================================

    def __iter__(self):

        return iter(

            self.to_dict().items()

        )

    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(category='{self.category}', "

            f"success={self.success})"

        )

    # =====================================================

    def __str__(self):

        return self.to_json(indent=2)