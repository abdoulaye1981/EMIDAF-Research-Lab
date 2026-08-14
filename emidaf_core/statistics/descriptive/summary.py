"""
=========================================================
EMIDAF Framework
Descriptive Statistics Summary
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from .central_tendency import CentralTendency
from .dispersion import Dispersion
from .position import Position
from .shape import Shape
from .robust import Robust

# ==========================================================
# SUMMARY
# ==========================================================

class DescriptiveSummary:

    """
    Résumé statistique complet
    d'une variable numérique.
    """

    def __init__(

        self,

        x,

        name=None,

    ):

        self.x=np.asarray(x)

        self.name=name

    # ==========================================================
# CENTRAL
# ==========================================================

    def central(

        self,

    ):

        return CentralTendency.all(

            self.x

        )
    
    # ==========================================================
# DISPERSION
# ==========================================================

    def dispersion(

        self,

    ):

        return Dispersion.all(

            self.x

        )
    
    # ==========================================================
# POSITION
# ==========================================================

    def position(

        self,

    ):

        return Position.all(

            self.x

        )
    
    # ==========================================================
# SHAPE
# ==========================================================

    def shape(

        self,

    ):

        return Shape.all(

            self.x

        )
    
    # ==========================================================
# ROBUST
# ==========================================================

    def robust(

        self,

    ):

        return Robust.all(

            self.x

        )
    
    # ==========================================================
# COMPLETE SUMMARY
# ==========================================================

    def compute(

        self,

    ):

        return {

            "central":

                self.central(),

            "dispersion":

                self.dispersion(),

            "position":

                self.position(),

            "shape":

                self.shape(),

            "robust":

                self.robust()

        }
    
    # ==========================================================
# DATAFRAME
# ==========================================================

    def to_dataframe(

        self,

    ):

        summary=self.compute()

        rows=[]

        for section,values in summary.items():

            if isinstance(

                values,

                dict

            ):

                for key,value in values.items():

                    rows.append({

                        "Category":

                            section,

                        "Statistic":

                            key,

                        "Value":

                            value

                    })

        return pd.DataFrame(

            rows

        )

    # ==========================================================
# TEXT
# ==========================================================

    def to_text(

        self,

    ):

        df=self.to_dataframe()

        lines=[]

        if self.name:

            lines.append(

                f"Variable : {self.name}"

            )

            lines.append("")

        for _,row in df.iterrows():

            lines.append(

                f"{row['Category']} | "

                f"{row['Statistic']} : "

                f"{row['Value']}"

            )

        return "\n".join(

            lines

        )

    # ==========================================================
# JSON
# ==========================================================

    def to_json(

        self,

    ):

        import json

        return json.dumps(

            self.compute(),

            indent=4,

            default=str

        )
    
    # ==========================================================
# SERVICE
# ==========================================================

class Summary:

    @staticmethod

    def describe(

        x,

        name=None,

    ):

        return DescriptiveSummary(

            x,

            name

        )