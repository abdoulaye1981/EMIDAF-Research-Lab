"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Assignment Service
=========================================================

Affectation reproductible des cas d'une étude HITL
aux enseignants évaluateurs.

Principe :
- tous les cas communs sont évalués par tous les enseignants ;
- chaque cas complémentaire est évalué par un seul enseignant ;
- les cas complémentaires sont équilibrés par strate ;
- aucune affectation n'est recréée si l'étude en possède déjà.
=========================================================
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Iterable

from database.models.teacher_validation_assignment_model import (
    TeacherValidationAssignmentModel,
)

from emidaf_core.repositories.teacher_validation_study_repository import (
    TeacherValidationStudyRepository,
)


PROBABILITY_BANDS = (
    "very_low",
    "low",
    "boundary_low",
    "boundary_high",
    "high",
    "very_high",
)


class TeacherValidationAssignmentService:

    def __init__(
        self,
        repository: TeacherValidationStudyRepository,
    ) -> None:

        self._repository = repository

    # =====================================================
    # CREATION DES AFFECTATIONS
    # =====================================================

    def create_assignments(
        self,
        *,
        study_id: int,
        teacher_user_ids: Iterable[int],
    ) -> dict:

        study_id = int(study_id)

        teacher_ids = [
            int(value)
            for value in teacher_user_ids
        ]

        # -------------------------------------------------
        # 1. Validation des enseignants
        # -------------------------------------------------

        if not teacher_ids:
            raise ValueError(
                "Aucun enseignant n'a été fourni."
            )

        if len(set(teacher_ids)) != len(teacher_ids):
            raise ValueError(
                "Les identifiants enseignants "
                "doivent être distincts."
            )

        study = self._repository.get_study(
            study_id
        )

        if study is None:
            raise ValueError(
                f"Etude HITL introuvable : {study_id}"
            )

        expected_teachers = int(
            study.teachers_required
        )

        if len(teacher_ids) != expected_teachers:
            raise ValueError(
                f"L'étude nécessite "
                f"{expected_teachers} enseignants ; "
                f"{len(teacher_ids)} fournis."
            )

        # -------------------------------------------------
        # 2. Protection anti-doublon
        # -------------------------------------------------

        existing = (
            self._repository
            .get_assignments(
                study_id
            )
        )

        if existing:
            raise RuntimeError(
                f"L'étude {study_id} possède déjà "
                f"{len(existing)} affectations. "
                "Aucune nouvelle affectation créée."
            )

        # -------------------------------------------------
        # 3. Chargement et contrôle des cas
        # -------------------------------------------------

        cases = self._repository.get_cases(
            study_id
        )

        if not cases:
            raise RuntimeError(
                "L'étude ne contient aucun cas."
            )

        expected_cases = int(
            study.requested_sample_size
        )

        if len(cases) != expected_cases:
            raise RuntimeError(
                f"{expected_cases} cas attendus, "
                f"{len(cases)} trouvés."
            )

        common_cases = [
            case
            for case in cases
            if bool(case.is_common)
        ]

        complementary_cases = [
            case
            for case in cases
            if not bool(case.is_common)
        ]

        expected_common = int(
            study.common_cases
        )

        if len(common_cases) != expected_common:
            raise RuntimeError(
                f"{expected_common} cas communs "
                f"attendus, {len(common_cases)} trouvés."
            )

        # -------------------------------------------------
        # 4. Affectation des cas communs
        #    Chaque cas -> tous les enseignants
        # -------------------------------------------------

        assignments = []

        for case in sorted(
            common_cases,
            key=self._case_sort_key,
        ):

            for teacher_id in teacher_ids:

                assignments.append(
                    TeacherValidationAssignmentModel(
                        study_id=study_id,
                        case_id=int(case.id),
                        teacher_user_id=teacher_id,
                        status="pending",
                    )
                )

        # -------------------------------------------------
        # 5. Cas complémentaires groupés par strate
        # -------------------------------------------------

        grouped = defaultdict(list)

        for case in complementary_cases:
            grouped[
                str(case.probability_band)
            ].append(case)

        for band in grouped:
            grouped[band].sort(
                key=self._case_sort_key
            )

        # Nombre de cas complémentaires déjà confiés
        # à chaque enseignant.
        extra_counts = {
            teacher_id: 0
            for teacher_id in teacher_ids
        }

        extra_band_counts = {
            teacher_id: Counter()
            for teacher_id in teacher_ids
        }

        # -------------------------------------------------
        # 6. Répartition équilibrée par strate
        # -------------------------------------------------

        for band_index, band in enumerate(
            PROBABILITY_BANDS
        ):

            band_cases = grouped.get(
                band,
                [],
            )

            if not band_cases:
                continue

            # Rotation du départ selon la strate.
            rotated_teachers = (
                teacher_ids[band_index % len(teacher_ids):]
                + teacher_ids[:band_index % len(teacher_ids)]
            )

            priority = {
                teacher_id: position
                for position, teacher_id
                in enumerate(rotated_teachers)
            }

            for case in band_cases:

                teacher_id = min(
                    teacher_ids,
                    key=lambda value: (
                        extra_counts[value],
                        extra_band_counts[value][band],
                        priority[value],
                    ),
                )

                assignments.append(
                    TeacherValidationAssignmentModel(
                        study_id=study_id,
                        case_id=int(case.id),
                        teacher_user_id=teacher_id,
                        status="pending",
                    )
                )

                extra_counts[teacher_id] += 1

                extra_band_counts[
                    teacher_id
                ][band] += 1

        # -------------------------------------------------
        # 7. Contrôles mathématiques avant INSERT
        # -------------------------------------------------

        expected_total = (
            len(common_cases)
            * len(teacher_ids)
            + len(complementary_cases)
        )

        if len(assignments) != expected_total:
            raise RuntimeError(
                "Nombre d'affectations incohérent : "
                f"{len(assignments)} produit, "
                f"{expected_total} attendu."
            )

        expected_pairs = {
            (
                assignment.case_id,
                assignment.teacher_user_id,
            )
            for assignment in assignments
        }

        if len(expected_pairs) != len(assignments):
            raise RuntimeError(
                "Une affectation dupliquée "
                "a été générée."
            )

        # -------------------------------------------------
        # 8. Persistance
        # -------------------------------------------------

        persisted = (
            self._repository
            .add_assignments(
                assignments
            )
        )

        # -------------------------------------------------
        # 9. Mise à jour du statut de l'étude
        # -------------------------------------------------

        study.status = "assigned"

        self._repository.update_study(
            study
        )

        # -------------------------------------------------
        # 10. Résumé
        # -------------------------------------------------

        total_by_teacher = {
            teacher_id: 0
            for teacher_id in teacher_ids
        }

        for assignment in persisted:
            total_by_teacher[
                int(
                    assignment.teacher_user_id
                )
            ] += 1

        return {
            "study_id": study_id,
            "status": "assigned",

            "teachers": teacher_ids,

            "common_cases":
                len(common_cases),

            "complementary_cases":
                len(complementary_cases),

            "total_assignments":
                len(persisted),

            "total_by_teacher":
                total_by_teacher,

            "complementary_by_teacher":
                dict(extra_counts),

            "complementary_by_band": {
                teacher_id:
                    dict(
                        extra_band_counts[
                            teacher_id
                        ]
                    )
                for teacher_id
                in teacher_ids
            },
        }

    # =====================================================
    # READ
    # =====================================================

    def get_assignments(
        self,
        study_id: int,
    ):
        return (
            self._repository
            .get_assignments(
                int(study_id)
            )
        )

    def get_assignments_for_teacher(
        self,
        *,
        study_id: int,
        teacher_user_id: int,
    ):
        return (
            self._repository
            .get_assignments_for_teacher(
                int(study_id),
                int(teacher_user_id),
            )
        )


    # =====================================================
    # WORKFLOW H7
    # =====================================================

    def get_assignment(
        self,
        assignment_id: int,
    ):
        return (
            self._repository
            .get_assignment(
                int(assignment_id)
            )
        )


    def get_assignment_for_teacher(
        self,
        *,
        assignment_id: int,
        teacher_user_id: int,
    ):
        return (
            self._repository
            .get_assignment_for_teacher(
                int(assignment_id),
                int(teacher_user_id),
            )
        )


    def get_case(
        self,
        case_id: int,
    ):
        return (
            self._repository
            .get_case(
                int(case_id)
            )
        )


    def start_assignment(
        self,
        *,
        assignment_id: int,
        teacher_user_id: int,
    ):
        """
        Marque une affectation comme démarrée.

        Transition normale :
        pending -> started

        L'opération est idempotente pour une affectation
        déjà démarrée ou plus avancée.
        """

        assignment = self._require_teacher_assignment(
            assignment_id=assignment_id,
            teacher_user_id=teacher_user_id,
        )

        status = str(
            assignment.status or "pending"
        )

        if status == "pending":

            assignment.status = "started"

            if assignment.started_at is None:
                assignment.started_at = datetime.utcnow()

            assignment = (
                self._repository
                .update_assignment(
                    assignment
                )
            )

        elif status not in {
            "started",
            "locked",
            "model_revealed",
            "completed",
        }:

            raise RuntimeError(
                "Statut d'affectation inconnu : "
                f"{status}"
            )

        return assignment


    def lock_assignment(
        self,
        *,
        assignment_id: int,
        teacher_user_id: int,
        validation_id: int,
    ):
        """
        Lie le jugement humain verrouillé à l'affectation.

        Transition :
        pending/started -> locked
        """

        assignment = self._require_teacher_assignment(
            assignment_id=assignment_id,
            teacher_user_id=teacher_user_id,
        )

        validation_id = int(
            validation_id
        )

        if validation_id <= 0:
            raise ValueError(
                "validation_id invalide."
            )

        status = str(
            assignment.status or "pending"
        )

        if status == "locked":

            if (
                assignment.validation_id is not None
                and int(assignment.validation_id)
                != validation_id
            ):
                raise RuntimeError(
                    "Cette affectation est déjà liée "
                    "à une autre validation."
                )

            if assignment.validation_id is None:
                assignment.validation_id = validation_id
                assignment = (
                    self._repository
                    .update_assignment(
                        assignment
                    )
                )

            return assignment

        if status not in {
            "pending",
            "started",
        }:
            raise RuntimeError(
                "Transition vers locked interdite "
                f"depuis le statut '{status}'."
            )

        if (
            assignment.validation_id is not None
            and int(assignment.validation_id)
            != validation_id
        ):
            raise RuntimeError(
                "Cette affectation possède déjà "
                "une autre validation."
            )

        if assignment.started_at is None:
            assignment.started_at = datetime.utcnow()

        assignment.validation_id = validation_id
        assignment.status = "locked"

        return (
            self._repository
            .update_assignment(
                assignment
            )
        )


    def reveal_assignment(
        self,
        *,
        assignment_id: int,
        teacher_user_id: int,
        validation_id: int | None = None,
    ):
        """
        Marque la révélation du résultat algorithmique.

        Transition :
        locked -> model_revealed
        """

        assignment = self._require_teacher_assignment(
            assignment_id=assignment_id,
            teacher_user_id=teacher_user_id,
        )

        status = str(
            assignment.status or "pending"
        )

        if validation_id is not None:

            validation_id = int(
                validation_id
            )

            if (
                assignment.validation_id is not None
                and int(assignment.validation_id)
                != validation_id
            ):
                raise RuntimeError(
                    "La validation fournie ne correspond "
                    "pas à l'affectation."
                )

        if status == "model_revealed":
            return assignment

        if status != "locked":
            raise RuntimeError(
                "Transition vers model_revealed "
                "interdite depuis le statut "
                f"'{status}'."
            )

        if assignment.validation_id is None:
            raise RuntimeError(
                "Impossible de révéler le modèle : "
                "aucune validation n'est liée "
                "à cette affectation."
            )

        assignment.status = "model_revealed"

        return (
            self._repository
            .update_assignment(
                assignment
            )
        )


    def complete_assignment(
        self,
        *,
        assignment_id: int,
        teacher_user_id: int,
        validation_id: int | None = None,
    ):
        """
        Marque une affectation comme terminée.

        Transition :
        model_revealed -> completed
        """

        assignment = self._require_teacher_assignment(
            assignment_id=assignment_id,
            teacher_user_id=teacher_user_id,
        )

        status = str(
            assignment.status or "pending"
        )

        if validation_id is not None:

            validation_id = int(
                validation_id
            )

            if (
                assignment.validation_id is not None
                and int(assignment.validation_id)
                != validation_id
            ):
                raise RuntimeError(
                    "La validation fournie ne correspond "
                    "pas à l'affectation."
                )

        if status == "completed":
            return assignment

        if status != "model_revealed":
            raise RuntimeError(
                "Transition vers completed interdite "
                f"depuis le statut '{status}'."
            )

        if assignment.validation_id is None:
            raise RuntimeError(
                "Impossible de terminer l'affectation : "
                "aucune validation n'est liée."
            )

        assignment.status = "completed"

        if assignment.completed_at is None:
            assignment.completed_at = datetime.utcnow()

        return (
            self._repository
            .update_assignment(
                assignment
            )
        )


    def _require_teacher_assignment(
        self,
        *,
        assignment_id: int,
        teacher_user_id: int,
    ):
        """
        Vérifie qu'une affectation existe et appartient
        bien à l'enseignant connecté.
        """

        assignment = (
            self._repository
            .get_assignment_for_teacher(
                int(assignment_id),
                int(teacher_user_id),
            )
        )

        if assignment is None:
            raise PermissionError(
                "Affectation introuvable ou non "
                "attribuée à cet enseignant."
            )

        return assignment


    # =====================================================
    # INTERNAL
    # =====================================================

    @staticmethod
    def _case_sort_key(case):
        rank = (
            case.sampling_rank
            if case.sampling_rank is not None
            else 10**12
        )

        return (
            int(rank),
            int(case.id),
        )
