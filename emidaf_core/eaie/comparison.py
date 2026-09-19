"""
EMIDAF Framework
EAIE - Model Comparison
"""

from __future__ import annotations

import pandas as pd

from sklearn.model_selection import cross_val_score


class ModelComparison:

    @staticmethod
    def cross_validate(
        estimator,
        X,
        y,
        task: str,
        cv: int = 5,
    ) -> dict:

        scoring = (
            "f1_weighted"
            if task == "classification"
            else "r2"
        )

        scores = cross_val_score(
            estimator,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=None,
        )

        return {
            "cv_metric": scoring,
            "cv_mean": float(
                scores.mean()
            ),
            "cv_std": float(
                scores.std()
            ),
            "cv_scores": (
                scores.tolist()
            ),
        }

    @staticmethod
    def table(
        results: list,
    ) -> pd.DataFrame:

        rows = []

        for result in results:

            row = {
                "model": result.model_name,
                "task": result.task,
                "score": result.score,
            }

            if result.task == "classification":

                row.update(
                    {
                        "accuracy": result.accuracy,
                        "precision": result.precision,
                        "recall": result.recall,
                        "f1": result.f1_score,
                        "roc_auc": result.roc_auc,
                    }
                )

            else:

                row.update(
                    {
                        "mae": result.mae,
                        "mse": result.mse,
                        "rmse": result.rmse,
                        "r2": result.r2,
                    }
                )

            row["cv_mean"] = (
                result.metadata.get(
                    "cv_mean"
                )
            )

            row["cv_std"] = (
                result.metadata.get(
                    "cv_std"
                )
            )

            rows.append(row)

        table = pd.DataFrame(rows)

        if not table.empty:

            table = table.sort_values(
                by="score",
                ascending=False,
                na_position="last",
            ).reset_index(drop=True)

        return table
