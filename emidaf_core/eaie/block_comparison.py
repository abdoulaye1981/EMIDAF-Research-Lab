"""
=========================================================
EMIDAF Framework
EAIE - Scientific Block Comparison
=========================================================

Comparaison prédictive cumulative de blocs de variables
avec :

- un split train/test commun ;
- des folds CV strictement identiques ;
- les mêmes modèles candidats ;
- sélection bloc + modèle uniquement par CV ;
- utilisation unique du jeu de test final.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

import pandas as pd

from sklearn.base import clone
from sklearn.model_selection import (
    KFold,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline

from emidaf_core.common.results import (
    ModelResult,
)

from .blocks import FeatureBlockResult
from .classification import (
    ClassificationModels,
)
from .comparison import ModelComparison
from .evaluation import ModelEvaluator
from .preparation import DataPreparation
from .problem import ProblemDetector
from .regression import RegressionModels


@dataclass(slots=True)
class BlockPerformance:
    """
    Performance CV du meilleur modèle d'un bloc cumulatif.
    """

    block: str
    features: list[str]
    n_features: int
    best_model: str
    cv_metric: str
    cv_mean: float
    cv_std: float
    delta_cv: float | None = None

    def to_dict(self) -> dict:
        return {
            "block": self.block,
            "features": list(
                self.features
            ),
            "n_features": self.n_features,
            "best_model": self.best_model,
            "cv_metric": self.cv_metric,
            "cv_mean": self.cv_mean,
            "cv_std": self.cv_std,
            "delta_cv": self.delta_cv,
        }


@dataclass(slots=True)
class BlockComparisonResult:
    """
    Résultat complet de la comparaison des blocs.
    """

    task: str
    target: str

    performances: list[
        BlockPerformance
    ] = field(default_factory=list)

    selected_block: str | None = None
    selected_model: str | None = None

    final_result: ModelResult | None = None

    train_indices: list = field(
        default_factory=list
    )

    test_indices: list = field(
        default_factory=list
    )

    cv_splits: list = field(
        default_factory=list
    )

    def table(self) -> pd.DataFrame:

        return pd.DataFrame(
            [
                performance.to_dict()
                for performance
                in self.performances
            ]
        )


class BlockComparisonEngine:
    """
    Comparaison scientifique cumulative de blocs EAIE.

    Le jeu de test n'est jamais utilisé pour comparer
    les blocs ou choisir les modèles.
    """

    def __init__(
        self,
        *,
        test_size: float = 0.20,
        random_state: int = 42,
        cv: int = 5,
    ):

        self.test_size = test_size
        self.random_state = random_state
        self.cv = cv

        self.result_: (
            BlockComparisonResult | None
        ) = None

    def _registry(
        self,
        task: str,
        models: list[str] | None,
    ):

        if task == "classification":

            registry = (
                ClassificationModels.registry(
                    random_state=self.random_state
                )
            )

        else:

            registry = (
                RegressionModels.registry(
                    random_state=self.random_state
                )
            )

        if models is None:
            return registry

        unknown = [
            name
            for name in models
            if name not in registry
        ]

        if unknown:
            raise ValueError(
                "Modèles inconnus : "
                + ", ".join(
                    unknown
                )
            )

        return {
            name: registry[name]
            for name in models
        }

    def _make_cv_splits(
        self,
        y_train,
        task: str,
    ) -> list[
        tuple[list[int], list[int]]
    ]:

        if task == "classification":

            splitter = StratifiedKFold(
                n_splits=self.cv,
                shuffle=True,
                random_state=self.random_state,
            )

            iterator = splitter.split(
                range(
                    len(y_train)
                ),
                y_train,
            )

        else:

            splitter = KFold(
                n_splits=self.cv,
                shuffle=True,
                random_state=self.random_state,
            )

            iterator = splitter.split(
                range(
                    len(y_train)
                )
            )

        return [
            (
                train_idx.tolist(),
                valid_idx.tolist(),
            )
            for train_idx, valid_idx
            in iterator
        ]

    def run(
        self,
        dataframe: pd.DataFrame,
        target: str,
        *,
        blocks: FeatureBlockResult,
        task: str | None = None,
        models: list[str] | None = None,
    ) -> BlockComparisonResult:

        if not blocks.valid:
            raise ValueError(
                "La configuration des blocs "
                "scientifiques est invalide."
            )

        if not blocks.cumulative:
            raise ValueError(
                "Aucun bloc cumulatif disponible."
            )

        all_features = list(
            blocks.predictors
        )

        prepared_all = (
            DataPreparation.prepare(
                dataframe,
                target,
                features=all_features,
            )
        )

        detected_task = (
            ProblemDetector.detect(
                prepared_all.y,
                task=task,
            )
        )

        positions = list(
            range(
                len(dataframe)
            )
        )

        stratify = None

        if detected_task == "classification":

            counts = (
                prepared_all.y
                .value_counts()
            )

            if (
                len(counts) > 1
                and counts.min() >= 2
            ):
                stratify = prepared_all.y

        (
            train_positions,
            test_positions,
        ) = train_test_split(
            positions,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=stratify,
        )

        y_train_common = (
            prepared_all.y.iloc[
                train_positions
            ]
            .reset_index(
                drop=True
            )
        )

        cv_splits = (
            self._make_cv_splits(
                y_train_common,
                detected_task,
            )
        )

        registry = self._registry(
            detected_task,
            models,
        )

        performances: list[
            BlockPerformance
        ] = []

        selected_pipeline = None
        selected_block = None
        selected_model = None
        selected_features = None
        selected_cv = None

        previous_cv = None

        for (
            block_name,
            block_features,
        ) in blocks.cumulative.items():

            prepared = (
                DataPreparation.prepare(
                    dataframe,
                    target,
                    features=block_features,
                )
            )

            X_train = (
                prepared.X.iloc[
                    train_positions
                ]
                .reset_index(
                    drop=True
                )
            )

            y_train = (
                prepared.y.iloc[
                    train_positions
                ]
                .reset_index(
                    drop=True
                )
            )

            preprocessor = (
                DataPreparation
                .build_preprocessor(
                    prepared.numeric_features,
                    prepared.categorical_features,
                    scale_numeric=True,
                )
            )

            block_candidates = []

            for name, estimator in (
                registry.items()
            ):

                pipeline = Pipeline(
                    [
                        (
                            "preprocessor",
                            clone(
                                preprocessor
                            ),
                        ),
                        (
                            "model",
                            clone(
                                estimator
                            ),
                        ),
                    ]
                )

                validation = (
                    ModelComparison
                    .cross_validate(
                        pipeline,
                        X_train,
                        y_train,
                        task=detected_task,
                        cv=cv_splits,
                    )
                )

                block_candidates.append(
                    (
                        validation[
                            "cv_mean"
                        ],
                        name,
                        pipeline,
                        validation,
                    )
                )

            if not block_candidates:
                raise RuntimeError(
                    f"Aucun modèle évalué pour "
                    f"le bloc '{block_name}'."
                )

            (
                best_cv,
                best_name,
                best_pipeline,
                best_validation,
            ) = max(
                block_candidates,
                key=lambda item: item[0],
            )

            delta_cv = (
                None
                if previous_cv is None
                else best_cv
                - previous_cv
            )

            performances.append(
                BlockPerformance(
                    block=block_name,
                    features=list(
                        block_features
                    ),
                    n_features=len(
                        block_features
                    ),
                    best_model=best_name,
                    cv_metric=(
                        best_validation[
                            "cv_metric"
                        ]
                    ),
                    cv_mean=best_cv,
                    cv_std=(
                        best_validation[
                            "cv_std"
                        ]
                    ),
                    delta_cv=delta_cv,
                )
            )

            previous_cv = best_cv

            if (
                selected_cv is None
                or best_cv > selected_cv
            ):
                selected_cv = best_cv
                selected_block = block_name
                selected_model = best_name
                selected_pipeline = (
                    best_pipeline
                )
                selected_features = list(
                    block_features
                )

        if (
            selected_pipeline is None
            or selected_features is None
        ):
            raise RuntimeError(
                "Aucun bloc scientifique "
                "n'a pu être sélectionné."
            )

        prepared_final = (
            DataPreparation.prepare(
                dataframe,
                target,
                features=selected_features,
            )
        )

        X_train_final = (
            prepared_final.X.iloc[
                train_positions
            ]
            .reset_index(
                drop=True
            )
        )

        X_test_final = (
            prepared_final.X.iloc[
                test_positions
            ]
            .reset_index(
                drop=True
            )
        )

        y_train_final = (
            prepared_final.y.iloc[
                train_positions
            ]
            .reset_index(
                drop=True
            )
        )

        y_test_final = (
            prepared_final.y.iloc[
                test_positions
            ]
            .reset_index(
                drop=True
            )
        )

        final_pipeline = clone(
            selected_pipeline
        )

        final_pipeline.fit(
            X_train_final,
            y_train_final,
        )

        if detected_task == "classification":

            final_result = (
                ModelEvaluator.classification(
                    estimator=final_pipeline,
                    X_test=X_test_final,
                    y_test=y_test_final,
                    model_name=selected_model,
                    features=selected_features,
                    target=target,
                    train_size=len(
                        X_train_final
                    ),
                )
            )

        else:

            final_result = (
                ModelEvaluator.regression(
                    estimator=final_pipeline,
                    X_test=X_test_final,
                    y_test=y_test_final,
                    model_name=selected_model,
                    features=selected_features,
                    target=target,
                    train_size=len(
                        X_train_final
                    ),
                )
            )

        final_result.metadata.update(
            {
                "selected_block":
                    selected_block,
                "cv_mean":
                    selected_cv,
                "block_comparison":
                    True,
            }
        )

        result = BlockComparisonResult(
            task=detected_task,
            target=target,
            performances=performances,
            selected_block=selected_block,
            selected_model=selected_model,
            final_result=final_result,
            train_indices=list(
                train_positions
            ),
            test_indices=list(
                test_positions
            ),
            cv_splits=cv_splits,
        )

        self.result_ = result

        return result
