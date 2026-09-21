"""
EMIDAF Framework
EAIE - Classification Models
"""

from __future__ import annotations

from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class ClassificationModels:

    @staticmethod
    def registry(
        random_state: int = 42,
    ):

        return {
            "logistic_regression": (
                LogisticRegression(
                    max_iter=2000,
                    random_state=random_state,
                )
            ),
            "decision_tree": (
                DecisionTreeClassifier(
                    random_state=random_state,
                )
            ),
            "random_forest": (
                RandomForestClassifier(
                    n_estimators=100,
                    random_state=random_state,
                    n_jobs=1,
                )
            ),
            "knn": (
                KNeighborsClassifier()
            ),
            "svm": (
                SVC(
                    probability=True,
                    random_state=random_state,
                )
            ),
            "gradient_boosting": (
                GradientBoostingClassifier(
                    random_state=random_state,
                )
            ),
        }
