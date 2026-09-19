"""
=========================================================
EMIDAF Framework
Model Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat standard des modèles de Machine Learning.

Utilisé par

- Linear Regression
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- CatBoost
- SVM
- KNN
- Naive Bayes
- PCA
- KMeans
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .base_result import BaseResult


@dataclass(slots=True)
class ModelResult(BaseResult):
    """
    Résultat standard d'un modèle.
    """

    category: str = "Machine Learning"

    # =====================================================
    # Général
    # =====================================================

    model_name: str = ""

    algorithm: str = ""

    model_type: str = ""

    task: str = ""

    library: str = ""

    fitted: bool = False

    # =====================================================
    # Données
    # =====================================================

    train_size: int = 0

    test_size: int = 0

    features: list[str] = field(default_factory=list)

    target: str = ""

    # =====================================================
    # Modèle
    # =====================================================

    estimator: object | None = field(
        default=None,
        repr=False,
    )

    parameters: dict = field(default_factory=dict)

    best_parameters: dict = field(default_factory=dict)

    # =====================================================
    # Métriques
    # =====================================================

    score: float | None = None

    accuracy: float | None = None

    precision: float | None = None

    recall: float | None = None

    f1_score: float | None = None

    roc_auc: float | None = None

    mae: float | None = None

    mse: float | None = None

    rmse: float | None = None

    r2: float | None = None

    log_loss: float | None = None

    silhouette_score: float | None = None

    davies_bouldin_score: float | None = None

    calinski_harabasz_score: float | None = None

    # =====================================================
    # Importance
    # =====================================================

    feature_importance: dict = field(
        default_factory=dict
    )

    coefficients: dict = field(
        default_factory=dict
    )

    intercept: float | None = None

    # =====================================================
    # Résultats
    # =====================================================

    predictions: list = field(
        default_factory=list
    )

    probabilities: list = field(
        default_factory=list
    )

    residuals: list = field(
        default_factory=list
    )

    confusion_matrix: list = field(
        default_factory=list
    )

    classification_report: dict = field(
        default_factory=dict
    )

    # =====================================================
    # Validation
    # =====================================================

    def is_fitted(self):

        return self.fitted

    def is_classifier(self):

        return self.task.lower() == "classification"

    def is_regressor(self):

        return self.task.lower() == "regression"

    def is_clusterer(self):

        return self.task.lower() == "clustering"

    # =====================================================
    # Utilitaires
    # =====================================================

    def add_feature(self, feature: str):

        self.features.append(feature)

    def add_parameter(self, key, value):

        self.parameters[key] = value

    def add_importance(self, feature, value):

        self.feature_importance[feature] = value

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Model": self.model_name,

            "Task": self.task,

            "Score": self.score,

            "Accuracy": self.accuracy,

            "R²": self.r2,

            "RMSE": self.rmse,

            "MAE": self.mae,

            "Features": len(self.features)

        }

    # =====================================================
    # Compact
    # =====================================================

    def compact(self):

        return {

            "model": self.model_name,

            "task": self.task,

            "score": self.score

        }

    # =====================================================
    # Display
    # =====================================================

    def __repr__(self):

        return (

            f"ModelResult("

            f"model='{self.model_name}', "

            f"task='{self.task}', "

            f"score={self.score}"

            f")"

        )