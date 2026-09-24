"""
EMIDAF Framework
EAIE - Regression Models
"""

from __future__ import annotations

from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


class RegressionModels:

    @staticmethod
    def registry(
        random_state: int = 42,
    ):

        registry = {
            "linear_regression": (
                LinearRegression()
            ),
            "ridge": (
                Ridge()
            ),
            "decision_tree": (
                DecisionTreeRegressor(
                    random_state=random_state,
                )
            ),
            "random_forest": (
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=random_state,
                    n_jobs=1,
                )
            ),
            "knn": (
                KNeighborsRegressor()
            ),
            "svr": (
                SVR()
            ),
            "gradient_boosting": (
                GradientBoostingRegressor(
                    random_state=random_state,
                )
            ),
        }

        # Dépendance optionnelle.
        # XGBoost n'est chargé que lorsque EAIE
        # construit réellement son registre.
        try:
            from xgboost import XGBRegressor

            registry["xgboost"] = (
                XGBRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    subsample=1.0,
                    colsample_bytree=1.0,
                    random_state=random_state,
                    n_jobs=1,
                    objective="reg:squarederror",
                )
            )

        except ImportError:
            pass

        return registry
