from __future__ import annotations

from typing import Any
import math


class ContextBuilder:

    EXCLUDED_KEYS = {
        # Objets scientifiques / modèles
        "estimator",
        "pipeline",
        "model",
        "X_train",
        "X_test",
        "y_train",
        "y_test",

        # Données tabulaires brutes
        "dataframe",
        "dataset",
        "raw_data",
        "train_data",
        "test_data",
        "records",
        "rows",
        "documents",
        "texts",

        # Sorties individuelles
        "labels",
        "prediction",
        "predictions",
        "probability",
        "probabilities",
        "observation_ids",
        "student_ids",
        "train_observation_ids",
        "test_observation_ids",
        "train_student_ids",
        "test_student_ids",

        # Contenus qualitatifs potentiellement identifiants
        "quotations",
        "verbatims",
    }

    MAX_SEQUENCE_ITEMS = 100
    MAX_STRING_LENGTH = 4000

    @classmethod
    def build(
        cls,
        analyses: dict[str, Any],
    ) -> dict[str, Any]:

        if not isinstance(analyses, dict):
            raise TypeError(
                "analyses doit être un dictionnaire."
            )

        return cls._sanitize(analyses)

    @classmethod
    def _sanitize(
        cls,
        value: Any,
    ) -> Any:

        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            return value[:cls.MAX_STRING_LENGTH]

        if isinstance(value, float):
            if not math.isfinite(value):
                return None
            return value

        if isinstance(value, dict):
            result = {}

            for key, item in value.items():
                key_str = str(key)

                if key_str in cls.EXCLUDED_KEYS:
                    continue

                sanitized = cls._sanitize(item)

                if sanitized is not None:
                    result[key_str] = sanitized

            return result

        if isinstance(value, (list, tuple, set)):
            return [
                cls._sanitize(item)
                for item in list(value)[
                    :cls.MAX_SEQUENCE_ITEMS
                ]
            ]

        if hasattr(value, "item"):
            try:
                return cls._sanitize(
                    value.item()
                )
            except Exception:
                pass

        module_name = value.__class__.__module__

        if (
            module_name.startswith("pandas")
            or module_name.startswith("sklearn")
            or module_name.startswith("xgboost")
        ):
            return None

        return str(value)[:cls.MAX_STRING_LENGTH]
