"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Sampling Service
=========================================================

Construction reproductible d'un échantillon expert
stratifié selon la probabilité produite par le modèle.
=========================================================
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Iterable


class TeacherValidationSamplingService:

    BAND_NAMES = (
        "very_low",
        "low",
        "boundary_low",
        "boundary_high",
        "high",
        "very_high",
    )

    @staticmethod
    def build_band_limits(
        threshold: float = 0.5,
    ) -> list[tuple[str, float, float, bool]]:

        threshold = float(threshold)

        if not 0.30 <= threshold <= 0.70:
            raise ValueError(
                "Le plan de stratification standard EMIDAF "
                "est prévu pour un seuil compris entre "
                "0.30 et 0.70."
            )

        lower_far = max(
            0.0,
            threshold - 0.30,
        )

        lower_near = max(
            0.0,
            threshold - 0.10,
        )

        upper_near = min(
            1.0,
            threshold + 0.10,
        )

        upper_far = min(
            1.0,
            threshold + 0.30,
        )

        return [
            ("very_low", 0.0, lower_far, False),
            ("low", lower_far, lower_near, False),
            (
                "boundary_low",
                lower_near,
                threshold,
                False,
            ),
            (
                "boundary_high",
                threshold,
                upper_near,
                False,
            ),
            ("high", upper_near, upper_far, False),
            ("very_high", upper_far, 1.0, True),
        ]

    @classmethod
    def probability_band(
        cls,
        probability: float,
        threshold: float = 0.5,
    ) -> str:

        probability = float(probability)

        if not 0.0 <= probability <= 1.0:
            raise ValueError(
                "La probabilité doit être comprise "
                "entre 0 et 1."
            )

        for (
            name,
            lower,
            upper,
            include_upper,
        ) in cls.build_band_limits(threshold):

            if include_upper:
                inside = (
                    lower
                    <= probability
                    <= upper
                )
            else:
                inside = (
                    lower
                    <= probability
                    < upper
                )

            if inside:
                return name

        raise ValueError(
            f"Probabilité non classable : {probability}"
        )

    @classmethod
    def prepare_predictions(
        cls,
        predictions: Iterable[dict],
        *,
        threshold: float = 0.5,
    ) -> list[dict]:

        prepared = []
        seen = set()

        for raw in predictions:

            observation_id = str(
                raw["observation_id"]
            ).strip()

            if not observation_id:
                continue

            if observation_id in seen:
                continue

            probability = float(
                raw["predicted_probability"]
            )

            if not 0.0 <= probability <= 1.0:
                continue

            seen.add(observation_id)

            row = dict(raw)

            row["observation_id"] = observation_id
            row["predicted_probability"] = probability
            row["threshold"] = float(threshold)

            row["probability_band"] = (
                cls.probability_band(
                    probability,
                    threshold,
                )
            )

            row["distance_to_threshold"] = abs(
                probability
                - float(threshold)
            )

            prepared.append(row)

        return prepared

    @classmethod
    def build_stratified_sample(
        cls,
        predictions: Iterable[dict],
        *,
        requested_sample_size: int,
        threshold: float = 0.5,
        random_state: int = 42,
    ) -> dict:

        requested_sample_size = int(
            requested_sample_size
        )

        if requested_sample_size <= 0:
            raise ValueError(
                "La taille de l'échantillon "
                "doit être positive."
            )

        records = cls.prepare_predictions(
            predictions,
            threshold=threshold,
        )

        if len(records) < requested_sample_size:

            raise ValueError(
                "Nombre insuffisant de prédictions : "
                f"{len(records)} disponibles pour "
                f"{requested_sample_size} demandées."
            )

        grouped = defaultdict(list)

        for row in records:
            grouped[
                row["probability_band"]
            ].append(row)

        rng = random.Random(
            int(random_state)
        )

        n_bands = len(
            cls.BAND_NAMES
        )

        base = (
            requested_sample_size // n_bands
        )

        remainder = (
            requested_sample_size % n_bands
        )

        targets = {}

        for index, band in enumerate(
            cls.BAND_NAMES
        ):

            targets[band] = (
                base
                + (
                    1
                    if index < remainder
                    else 0
                )
            )

        selected = []
        selected_ids = set()
        realized_counts = {}

        for band in cls.BAND_NAMES:

            population = list(
                grouped.get(
                    band,
                    [],
                )
            )

            population.sort(
                key=lambda row:
                    row["observation_id"]
            )

            target = min(
                targets[band],
                len(population),
            )

            chosen = (
                rng.sample(
                    population,
                    target,
                )
                if target > 0
                else []
            )

            selected.extend(chosen)

            for row in chosen:
                selected_ids.add(
                    row["observation_id"]
                )

            realized_counts[band] = len(
                chosen
            )

        # Redistribue le déficit éventuel
        # lorsque certaines strates sont trop petites.
        deficit = (
            requested_sample_size
            - len(selected)
        )

        if deficit > 0:

            remaining = [
                row
                for row in records
                if row["observation_id"]
                not in selected_ids
            ]

            if len(remaining) < deficit:
                raise ValueError(
                    "Impossible de compléter "
                    "l'échantillon demandé."
                )

            remaining.sort(
                key=lambda row: (
                    row["probability_band"],
                    row["observation_id"],
                )
            )

            extras = rng.sample(
                remaining,
                deficit,
            )

            for row in extras:

                selected.append(row)

                band = row[
                    "probability_band"
                ]

                realized_counts[band] = (
                    realized_counts.get(
                        band,
                        0,
                    )
                    + 1
                )

        rng.shuffle(selected)

        for rank, row in enumerate(
            selected,
            start=1,
        ):
            row["sampling_rank"] = rank

        return {
            "cases": selected,
            "summary": {
                "requested_sample_size":
                    requested_sample_size,
                "realized_sample_size":
                    len(selected),
                "threshold":
                    float(threshold),
                "random_state":
                    int(random_state),
                "targets":
                    targets,
                "realized_counts":
                    realized_counts,
                "available_counts": {
                    band: len(
                        grouped.get(
                            band,
                            [],
                        )
                    )
                    for band in cls.BAND_NAMES
                },
            },
        }
