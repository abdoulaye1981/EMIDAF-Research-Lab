"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Study Service
=========================================================

Gestion métier d'une étude quantitative Human-in-the-Loop :

- création de l'étude ;
- échantillonnage stratifié reproductible ;
- sélection équilibrée des cas communs ;
- persistance des cas ;
- passage draft -> sampled.
=========================================================
"""

from __future__ import annotations

from datetime import datetime
import random

from database.models.teacher_validation_study_model import (
    TeacherValidationStudyModel,
)
from database.models.teacher_validation_case_model import (
    TeacherValidationCaseModel,
)

from emidaf_core.repositories.teacher_validation_study_repository import (
    TeacherValidationStudyRepository,
)
from emidaf_core.services.teacher_validation_sampling_service import (
    TeacherValidationSamplingService,
)


VALID_STUDY_STATUSES = {
    "draft",
    "sampled",
    "assigned",
    "active",
    "closed",
}


class TeacherValidationStudyService:

    def __init__(
        self,
        repository: TeacherValidationStudyRepository,
        sampling_service: TeacherValidationSamplingService | None = None,
    ) -> None:

        self._repository = repository

        self._sampling = (
            sampling_service
            or TeacherValidationSamplingService()
        )

    # =====================================================
    # CREATION COMPLETE : ETUDE + ECHANTILLON
    # =====================================================

    def create_sampled_study(
        self,
        *,
        project_id: int,
        dataset_id: int,
        name: str,
        model_name: str,
        target: str,
        predictions: list[dict],
        threshold: float = 0.5,
        requested_sample_size: int = 180,
        teachers_required: int = 3,
        common_cases: int = 100,
        random_state: int = 42,
        created_by: int | None = None,
        provenance: dict | None = None,
        description: str | None = None,
    ) -> TeacherValidationStudyModel:

        project_id = int(project_id)
        dataset_id = int(dataset_id)

        name = str(name).strip()
        model_name = str(model_name).strip()
        target = str(target).strip()

        threshold = float(threshold)
        requested_sample_size = int(
            requested_sample_size
        )
        teachers_required = int(
            teachers_required
        )
        common_cases = int(
            common_cases
        )
        random_state = int(
            random_state
        )

        if not name:
            raise ValueError(
                "Le nom de l'étude est obligatoire."
            )

        if not model_name:
            raise ValueError(
                "Le nom du modèle est obligatoire."
            )

        if not target:
            raise ValueError(
                "La cible est obligatoire."
            )

        if not 0.0 < threshold < 1.0:
            raise ValueError(
                "Le seuil doit être compris "
                "strictement entre 0 et 1."
            )

        if requested_sample_size <= 0:
            raise ValueError(
                "La taille de l'échantillon "
                "doit être positive."
            )

        if teachers_required <= 0:
            raise ValueError(
                "Le nombre d'enseignants "
                "doit être positif."
            )

        if common_cases < 0:
            raise ValueError(
                "Le nombre de cas communs "
                "ne peut pas être négatif."
            )

        if common_cases > requested_sample_size:
            raise ValueError(
                "Le nombre de cas communs ne peut pas "
                "dépasser la taille de l'échantillon."
            )

        # ---------------------------------------------
        # 1. Echantillonnage stratifié reproductible
        # ---------------------------------------------

        sample_result = (
            self._sampling
            .build_stratified_sample(
                predictions,
                requested_sample_size=
                    requested_sample_size,
                threshold=threshold,
                random_state=random_state,
            )
        )

        sampled_rows = sample_result["cases"]
        sampling_summary = sample_result["summary"]

        # ---------------------------------------------
        # 2. Sélection stratifiée des cas communs
        # ---------------------------------------------

        common_ids = (
            self._select_common_observation_ids(
                sampled_rows,
                common_cases=common_cases,
                random_state=random_state,
            )
        )

        # ---------------------------------------------
        # 3. Création de l'étude en draft
        # ---------------------------------------------

        sampling_config = {
            "strategy":
                "stratified_probability",
            "bands":
                list(
                    self._sampling.BAND_NAMES
                ),
            "requested_sample_size":
                requested_sample_size,
            "realized_sample_size":
                len(sampled_rows),
            "teachers_required":
                teachers_required,
            "common_cases":
                common_cases,
            "random_state":
                random_state,
            "available_counts":
                sampling_summary.get(
                    "available_counts",
                    {},
                ),
            "selected_counts":
                sampling_summary.get(
                    "realized_counts",
                    {},
                ),
            "targets":
                sampling_summary.get(
                    "targets",
                    {},
                ),
        }

        if provenance:
            sampling_config["provenance"] = dict(
                provenance
            )

        study = TeacherValidationStudyModel(
            project_id=project_id,
            dataset_id=dataset_id,
            name=name,
            description=description,
            model_name=model_name,
            target=target,
            threshold=threshold,
            sampling_method=
                "stratified_probability",
            requested_sample_size=
                requested_sample_size,
            teachers_required=
                teachers_required,
            common_cases=
                common_cases,
            random_state=
                random_state,
            sampling_config=
                sampling_config,
            status="draft",
            created_by=created_by,
        )

        study = self._repository.add_study(
            study
        )

        # ---------------------------------------------
        # 4. Transformation en objets persistants
        # ---------------------------------------------

        cases = []

        for row in sampled_rows:

            observation_id = str(
                row["observation_id"]
            )

            probability = float(
                row["predicted_probability"]
            )

            predicted_class = row.get(
                "predicted_class"
            )

            if predicted_class is not None:
                predicted_class = str(
                    predicted_class
                )

            student_id = row.get(
                "student_id"
            )

            if student_id is not None:
                student_id = str(
                    student_id
                )

            snapshot = {
                "observation_id":
                    observation_id,
                "predicted_probability":
                    probability,
                "predicted_class":
                    predicted_class,
                "threshold":
                    threshold,
                "probability_band":
                    row[
                        "probability_band"
                    ],
                "distance_to_threshold":
                    float(
                        row[
                            "distance_to_threshold"
                        ]
                    ),
            }

            case = TeacherValidationCaseModel(
                study_id=study.id,
                observation_id=
                    observation_id,
                student_id=
                    student_id,
                predicted_class=
                    predicted_class,
                predicted_probability=
                    probability,
                threshold=
                    threshold,
                probability_band=
                    row[
                        "probability_band"
                    ],
                distance_to_threshold=
                    float(
                        row[
                            "distance_to_threshold"
                        ]
                    ),
                sampling_rank=
                    int(
                        row[
                            "sampling_rank"
                        ]
                    ),
                is_common=(
                    observation_id
                    in common_ids
                ),
                prediction_snapshot=
                    snapshot,
            )

            cases.append(case)

        self._repository.add_cases(
            cases
        )

        # ---------------------------------------------
        # 5. L'étude devient sampled
        # ---------------------------------------------

        study.status = "sampled"

        study = (
            self._repository
            .update_study(
                study
            )
        )

        return study

    # =====================================================
    # READ
    # =====================================================

    def get(
        self,
        study_id: int,
    ) -> TeacherValidationStudyModel | None:

        return self._repository.get_study(
            study_id
        )

    def get_cases(
        self,
        study_id: int,
    ) -> list[TeacherValidationCaseModel]:

        return self._repository.get_cases(
            study_id
        )

    # =====================================================
    # SELECTION DES CAS COMMUNS
    # =====================================================

    def _select_common_observation_ids(
        self,
        sampled_rows: list[dict],
        *,
        common_cases: int,
        random_state: int,
    ) -> set[str]:

        if common_cases == 0:
            return set()

        grouped = {
            band: []
            for band in self._sampling.BAND_NAMES
        }

        for row in sampled_rows:

            grouped[
                row["probability_band"]
            ].append(row)

        rng = random.Random(
            int(random_state) + 1000
        )

        n_bands = len(
            self._sampling.BAND_NAMES
        )

        base = common_cases // n_bands
        remainder = common_cases % n_bands

        targets = {}

        for index, band in enumerate(
            self._sampling.BAND_NAMES
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

        for band in self._sampling.BAND_NAMES:

            population = list(
                grouped[band]
            )

            population.sort(
                key=lambda row:
                    int(
                        row[
                            "sampling_rank"
                        ]
                    )
            )

            n_select = min(
                targets[band],
                len(population),
            )

            chosen = (
                rng.sample(
                    population,
                    n_select,
                )
                if n_select > 0
                else []
            )

            selected.extend(chosen)

            for row in chosen:
                selected_ids.add(
                    str(
                        row[
                            "observation_id"
                        ]
                    )
                )

        deficit = (
            common_cases
            - len(selected_ids)
        )

        if deficit > 0:

            remaining = [
                row
                for row in sampled_rows
                if str(
                    row["observation_id"]
                )
                not in selected_ids
            ]

            remaining.sort(
                key=lambda row:
                    int(
                        row[
                            "sampling_rank"
                        ]
                    )
            )

            extras = rng.sample(
                remaining,
                deficit,
            )

            for row in extras:
                selected_ids.add(
                    str(
                        row[
                            "observation_id"
                        ]
                    )
                )

        return selected_ids
