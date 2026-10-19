"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Service
=========================================================

Logique métier de validation humaine des résultats
EMIDAF.

Cette couche maintient une séparation stricte entre :
- résultat algorithmique ;
- validation humaine ;
- éventuelle consolidation ultérieure.
=========================================================
"""

from __future__ import annotations

from database.models.teacher_validation_model import (
    TeacherValidationModel,
)
from emidaf_core.repositories.teacher_validation_repository import (
    TeacherValidationRepository,
)


VALID_VALIDATION_STATUSES = {
    "confirmed",
    "partially_confirmed",
    "not_confirmed",
    "not_evaluable",
}

VALID_DIFFICULTY_LEVELS = {
    "none",
    "mild",
    "moderate",
    "severe",
}


VALID_TEACHER_DETECTED_CLASSES = {
    "difficulty",
    "no_difficulty",
    "not_evaluable",
}


class TeacherValidationService:
    """
    Service métier des validations humaines EMIDAF.
    """

    def __init__(
        self,
        repository: TeacherValidationRepository,
    ) -> None:

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        *,
        project_id: int,
        dataset_id: int,
        observation_id: str,
        model_name: str,
        task: str,
        detection_validation: str,
        diagnosis_validation: str,
        student_id: str | None = None,
        validator_user_id: int | None = None,
        educational_teacher_id: str | None = None,
        target: str | None = None,
        threshold: float | None = None,
        predicted_class: str | int | None = None,
        predicted_probability: float | None = None,
        teacher_detected_class: str | None = None,
        difficulty_level: str | None = None,
        teacher_factors: list | None = None,
        teacher_comment: str | None = None,
        algorithmic_diagnosis: dict | None = None,
    ) -> TeacherValidationModel:

        project_id = int(project_id)
        dataset_id = int(dataset_id)

        observation_id = str(
            observation_id
        ).strip()

        model_name = str(
            model_name
        ).strip()

        task = str(
            task
        ).strip()

        detection_validation = str(
            detection_validation
        ).strip()

        diagnosis_validation = str(
            diagnosis_validation
        ).strip()

        if not observation_id:
            raise ValueError(
                "L'identifiant de l'observation "
                "est obligatoire."
            )

        if not model_name:
            raise ValueError(
                "Le nom du modèle est obligatoire."
            )

        if task not in {
            "classification",
            "regression",
        }:
            raise ValueError(
                "La tâche doit être "
                "'classification' ou 'regression'."
            )

        self._validate_status(
            detection_validation,
            "validation de la détection",
        )

        self._validate_status(
            diagnosis_validation,
            "validation du diagnostic",
        )

        if difficulty_level is not None:

            difficulty_level = str(
                difficulty_level
            ).strip()

            if (
                difficulty_level
                not in VALID_DIFFICULTY_LEVELS
            ):
                raise ValueError(
                    "Niveau de difficulté invalide : "
                    f"{difficulty_level}"
                )

        if predicted_probability is not None:

            predicted_probability = float(
                predicted_probability
            )

            if task == "classification":

                if not (
                    0.0
                    <= predicted_probability
                    <= 1.0
                ):
                    raise ValueError(
                        "La probabilité prédite doit "
                        "être comprise entre 0 et 1."
                    )

        if threshold is not None:
            threshold = float(threshold)

        if teacher_detected_class is not None:

            teacher_detected_class = str(
                teacher_detected_class
            ).strip()

            if (
                teacher_detected_class
                not in VALID_TEACHER_DETECTED_CLASSES
            ):
                raise ValueError(
                    "Classe détectée par l'enseignant "
                    "invalide : "
                    f"{teacher_detected_class}"
                )

        if student_id is not None:
            student_id = str(
                student_id
            ).strip() or None

        if educational_teacher_id is not None:
            educational_teacher_id = str(
                educational_teacher_id
            ).strip() or None

        if target is not None:
            target = str(
                target
            ).strip() or None

        if predicted_class is not None:
            predicted_class = str(
                predicted_class
            )

        if teacher_comment is not None:
            teacher_comment = str(
                teacher_comment
            ).strip() or None

        clean_factors = None

        if teacher_factors is not None:

            clean_factors = [
                str(value).strip()
                for value in teacher_factors
                if str(value).strip()
            ]

        validation = TeacherValidationModel(
            project_id=project_id,
            dataset_id=dataset_id,
            observation_id=observation_id,
            student_id=student_id,
            validator_user_id=(
                int(validator_user_id)
                if validator_user_id is not None
                else None
            ),
            educational_teacher_id=(
                educational_teacher_id
            ),
            model_name=model_name,
            task=task,
            target=target,
            threshold=threshold,
            predicted_class=predicted_class,
            predicted_probability=(
                predicted_probability
            ),
            teacher_detected_class=(
                teacher_detected_class
            ),
            detection_validation=(
                detection_validation
            ),
            diagnosis_validation=(
                diagnosis_validation
            ),
            difficulty_level=(
                difficulty_level
            ),
            teacher_factors=(
                clean_factors
            ),
            teacher_comment=(
                teacher_comment
            ),
            algorithmic_diagnosis=(
                algorithmic_diagnosis
            ),
        )

        return self._repository.add(
            validation
        )

    # =====================================================
    # READ
    # =====================================================

    def get(
        self,
        validation_id: int,
    ) -> TeacherValidationModel | None:

        return self._repository.get_by_id(
            validation_id
        )

    def get_for_observation(
        self,
        project_id: int,
        dataset_id: int,
        observation_id: str,
    ) -> list[TeacherValidationModel]:

        return (
            self._repository
            .get_by_observation(
                project_id,
                dataset_id,
                observation_id,
            )
        )

    def get_latest_for_observation(
        self,
        project_id: int,
        dataset_id: int,
        observation_id: str,
    ) -> TeacherValidationModel | None:

        return (
            self._repository
            .get_latest_by_observation(
                project_id,
                dataset_id,
                observation_id,
            )
        )

    def get_for_student(
        self,
        project_id: int,
        dataset_id: int,
        student_id: str,
    ) -> list[TeacherValidationModel]:

        return (
            self._repository
            .get_by_student(
                project_id,
                dataset_id,
                student_id,
            )
        )

    def get_for_dataset(
        self,
        project_id: int,
        dataset_id: int,
    ) -> list[TeacherValidationModel]:

        return (
            self._repository
            .get_by_dataset(
                project_id,
                dataset_id,
            )
        )

    def get_for_project(
        self,
        project_id: int,
    ) -> list[TeacherValidationModel]:

        return (
            self._repository
            .get_by_project(
                project_id
            )
        )

    def get_for_validator(
        self,
        validator_user_id: int,
    ) -> list[TeacherValidationModel]:

        return (
            self._repository
            .get_by_validator(
                validator_user_id
            )
        )

    def count(
        self,
        project_id: int,
        dataset_id: int,
    ) -> int:

        return self._repository.count(
            project_id,
            dataset_id,
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        validation: TeacherValidationModel,
    ) -> TeacherValidationModel:

        self._validate_status(
            validation.detection_validation,
            "validation de la détection",
        )

        self._validate_status(
            validation.diagnosis_validation,
            "validation du diagnostic",
        )

        if (
            validation.teacher_detected_class
            is not None
            and validation.teacher_detected_class
            not in VALID_TEACHER_DETECTED_CLASSES
        ):
            raise ValueError(
                "Classe détectée par l'enseignant "
                "invalide : "
                f"{validation.teacher_detected_class}"
            )

        if (
            validation.difficulty_level
            is not None
            and validation.difficulty_level
            not in VALID_DIFFICULTY_LEVELS
        ):
            raise ValueError(
                "Niveau de difficulté invalide : "
                f"{validation.difficulty_level}"
            )

        return self._repository.update(
            validation
        )

    # =====================================================
    # HUMAN-IN-THE-LOOP
    # =====================================================

    def create_locked_judgment(
        self,
        *,
        project_id: int,
        dataset_id: int,
        observation_id: str,
        model_name: str,
        task: str,
        validator_user_id: int,
        teacher_detected_class: str,
        teacher_confidence: int,
        student_id: str | None = None,
        educational_teacher_id: str | None = None,
        target: str | None = None,
        threshold: float | None = None,
        predicted_class: str | int | None = None,
        predicted_probability: float | None = None,
        difficulty_level: str | None = None,
        teacher_factors: list | None = None,
        teacher_initial_comment: str | None = None,
        algorithmic_diagnosis: dict | None = None,
    ) -> TeacherValidationModel:
        """
        Enregistre et verrouille le jugement indépendant.

        La prédiction peut être persistée côté serveur,
        mais elle ne doit pas être révélée dans l'interface
        avant le verrouillage.

        Les valeurs temporaires 'not_evaluable' de
        detection_validation et diagnosis_validation
        servent uniquement à respecter le schéma historique
        nullable=False. Elles ne doivent pas être analysées
        tant que validation_status != 'completed'.
        """

        from datetime import datetime

        teacher_detected_class = str(
            teacher_detected_class
        ).strip()

        if (
            teacher_detected_class
            not in VALID_TEACHER_DETECTED_CLASSES
        ):

            raise ValueError(
                "Classe détectée par l'enseignant "
                "invalide : "
                f"{teacher_detected_class}"
            )

        teacher_confidence = int(
            teacher_confidence
        )

        if teacher_confidence not in {
            1,
            2,
            3,
            4,
            5,
        }:

            raise ValueError(
                "Le niveau de confiance doit être "
                "compris entre 1 et 5."
            )

        # Cohérence niveau de difficulté / jugement.
        if (
            teacher_detected_class
            == "difficulty"
        ):

            if difficulty_level in {
                None,
                "",
                "none",
            }:

                raise ValueError(
                    "Le niveau de difficulté est "
                    "obligatoire lorsqu'une difficulté "
                    "est déclarée."
                )

        elif (
            teacher_detected_class
            == "no_difficulty"
        ):

            difficulty_level = "none"

        elif (
            teacher_detected_class
            == "not_evaluable"
        ):

            difficulty_level = None

        initial_comment = (
            str(
                teacher_initial_comment
            ).strip()
            if teacher_initial_comment
            else None
        )

        validation = self.create(
            project_id=project_id,
            dataset_id=dataset_id,
            observation_id=observation_id,
            model_name=model_name,
            task=task,

            # Valeurs techniques temporaires.
            detection_validation="not_evaluable",
            diagnosis_validation="not_evaluable",

            student_id=student_id,
            validator_user_id=validator_user_id,
            educational_teacher_id=(
                educational_teacher_id
            ),
            target=target,
            threshold=threshold,
            predicted_class=predicted_class,
            predicted_probability=(
                predicted_probability
            ),
            teacher_detected_class=(
                teacher_detected_class
            ),
            difficulty_level=(
                difficulty_level
            ),
            teacher_factors=(
                teacher_factors or []
            ),

            # Compatibilité avec les anciennes
            # vues utilisant teacher_comment.
            teacher_comment=(
                initial_comment
            ),

            algorithmic_diagnosis=(
                algorithmic_diagnosis
            ),
        )

        validation.teacher_confidence = (
            teacher_confidence
        )

        validation.teacher_initial_comment = (
            initial_comment
        )

        validation.teacher_post_model_comment = None

        validation.disagreement_reasons = None

        validation.validation_status = (
            "locked"
        )

        validation.judgment_locked_at = (
            datetime.utcnow()
        )

        validation.model_revealed_at = None

        validation.completed_at = None

        return self._repository.update(
            validation
        )

    def reveal_model(
        self,
        validation_id: int,
    ) -> TeacherValidationModel:
        """
        Passe de locked à model_revealed.

        Le jugement initial ne peut pas être modifié ici.
        """

        from datetime import datetime

        validation = self.get(
            validation_id
        )

        if validation is None:

            raise ValueError(
                "Validation introuvable."
            )

        if (
            validation.judgment_locked_at
            is None
        ):

            raise ValueError(
                "Le jugement indépendant doit "
                "être verrouillé avant de révéler "
                "le modèle."
            )

        if (
            validation.validation_status
            == "completed"
        ):

            return validation

        if (
            validation.model_revealed_at
            is None
        ):

            validation.model_revealed_at = (
                datetime.utcnow()
            )

        validation.validation_status = (
            "model_revealed"
        )

        return self._repository.update(
            validation
        )

    def complete_validation(
        self,
        validation_id: int,
        *,
        detection_validation: str,
        diagnosis_validation: str,
        post_model_comment: str | None = None,
        disagreement_reasons: list | None = None,
    ) -> TeacherValidationModel:
        """
        Finalise la validation après révélation du modèle.

        Cette méthode ne modifie jamais :
        - teacher_detected_class ;
        - teacher_confidence ;
        - difficulty_level ;
        - teacher_factors ;
        - teacher_initial_comment.
        """

        from datetime import datetime

        validation = self.get(
            validation_id
        )

        if validation is None:

            raise ValueError(
                "Validation introuvable."
            )

        if (
            validation.judgment_locked_at
            is None
        ):

            raise ValueError(
                "Le jugement indépendant doit "
                "être verrouillé avant la finalisation."
            )

        self._validate_status(
            detection_validation,
            "validation de la détection",
        )

        self._validate_status(
            diagnosis_validation,
            "validation du diagnostic",
        )

        if (
            validation.model_revealed_at
            is None
        ):

            validation.model_revealed_at = (
                datetime.utcnow()
            )

        validation.detection_validation = (
            detection_validation
        )

        validation.diagnosis_validation = (
            diagnosis_validation
        )

        validation.teacher_post_model_comment = (
            str(
                post_model_comment
            ).strip()
            if post_model_comment
            else None
        )

        validation.disagreement_reasons = [
            str(
                value
            ).strip()
            for value
            in (
                disagreement_reasons
                or []
            )
            if str(
                value
            ).strip()
        ] or None

        validation.validation_status = (
            "completed"
        )

        validation.completed_at = (
            datetime.utcnow()
        )

        return self._repository.update(
            validation
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        validation_id: int,
    ) -> None:

        self._repository.delete(
            validation_id
        )

    # =====================================================
    # INTERNAL VALIDATION
    # =====================================================

    @staticmethod
    def _validate_status(
        value: str,
        label: str,
    ) -> None:

        if value not in VALID_VALIDATION_STATUSES:
            raise ValueError(
                f"{label} invalide : {value}. "
                "Valeurs autorisées : "
                + ", ".join(
                    sorted(
                        VALID_VALIDATION_STATUSES
                    )
                )
            )
