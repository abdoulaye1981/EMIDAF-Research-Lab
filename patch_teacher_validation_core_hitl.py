from __future__ import annotations

from datetime import datetime
from pathlib import Path
import py_compile
import shutil


ROOT = Path.cwd()

MODEL = ROOT / "database/models/teacher_validation_model.py"
SERVICE = ROOT / "emidaf_core/services/teacher_validation_service.py"
CONTROLLER = ROOT / "emidaf_core/controllers/teacher_validation_controller.py"

FILES = [
    MODEL,
    SERVICE,
    CONTROLLER,
]


def backup(path: Path) -> None:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    destination = path.with_name(
        path.name + f".bak_hitl_{stamp}"
    )

    shutil.copy2(
        path,
        destination,
    )

    print(
        f"[BACKUP] {destination}"
    )


def read(path: Path) -> str:

    if not path.exists():

        raise FileNotFoundError(
            f"Fichier introuvable : {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


def write(
    path: Path,
    content: str,
) -> None:

    path.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"[WRITE] {path}"
    )


def replace_once(
    text: str,
    old: str,
    new: str,
    label: str,
) -> str:

    count = text.count(
        old
    )

    if count != 1:

        raise RuntimeError(
            f"{label} : "
            f"ancre attendue 1 fois, "
            f"trouvée {count} fois."
        )

    return text.replace(
        old,
        new,
        1,
    )


# =========================================================
# MODEL
# =========================================================

def patch_model() -> None:

    text = read(
        MODEL
    )

    if (
        "teacher_confidence: Mapped[int | None]"
        in text
    ):

        print(
            "[SKIP] Modèle déjà patché."
        )

        return

    anchor = '''    teacher_detected_class: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
'''

    replacement = anchor + '''

    # =====================================================
    # HUMAN-IN-THE-LOOP
    # =====================================================

    # Degré de confiance du jugement indépendant :
    # 1 = très faible ; 5 = très élevé.
    teacher_confidence: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Commentaire produit AVANT révélation du modèle.
    teacher_initial_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Commentaire produit APRÈS révélation du modèle.
    teacher_post_model_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Raisons structurées d'un désaccord ou d'une réserve.
    disagreement_reasons: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # Etats possibles :
    # locked
    # model_revealed
    # completed
    validation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="completed",
    )

    # Instant où le jugement humain devient immuable.
    judgment_locked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Instant de première révélation du résultat algorithmique.
    model_revealed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Fin de la procédure de validation.
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
'''

    text = replace_once(
        text,
        anchor,
        replacement,
        "TeacherValidationModel",
    )

    write(
        MODEL,
        text,
    )


# =========================================================
# SERVICE
# =========================================================

def patch_service() -> None:

    text = read(
        SERVICE
    )

    if (
        "def create_locked_judgment("
        in text
    ):

        print(
            "[SKIP] Service déjà patché."
        )

        return

    marker = '''    # =====================================================
    # DELETE
    # =====================================================
'''

    methods = r'''    # =====================================================
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

'''

    text = replace_once(
        text,
        marker,
        methods + marker,
        "TeacherValidationService",
    )

    write(
        SERVICE,
        text,
    )


# =========================================================
# CONTROLLER
# =========================================================

def patch_controller() -> None:

    text = read(
        CONTROLLER
    )

    if (
        "def create_locked_judgment("
        in text
    ):

        print(
            "[SKIP] Contrôleur déjà patché."
        )

        return

    marker = '''    # =====================================================
    # UPDATE
    # =====================================================
'''

    methods = r'''    # =====================================================
    # HUMAN-IN-THE-LOOP
    # =====================================================

    def create_locked_judgment(
        self,
        **kwargs,
    ) -> TeacherValidationModel:

        return (
            self._service
            .create_locked_judgment(
                **kwargs
            )
        )

    def reveal_model(
        self,
        validation_id: int,
    ) -> TeacherValidationModel:

        return (
            self._service
            .reveal_model(
                validation_id
            )
        )

    def complete_validation(
        self,
        validation_id: int,
        **kwargs,
    ) -> TeacherValidationModel:

        return (
            self._service
            .complete_validation(
                validation_id,
                **kwargs,
            )
        )

'''

    text = replace_once(
        text,
        marker,
        methods + marker,
        "TeacherValidationController",
    )

    write(
        CONTROLLER,
        text,
    )


# =========================================================
# VERIFICATION
# =========================================================

def compile_files() -> None:

    for path in FILES:

        py_compile.compile(
            str(path),
            doraise=True,
        )

        print(
            f"[COMPILE OK] {path}"
        )


def main() -> None:

    print(
        "=============================================="
    )

    print(
        "EMIDAF — PATCH VALIDATION ENSEIGNANT HITL"
    )

    print(
        "=============================================="
    )

    for path in FILES:

        if not path.exists():

            raise FileNotFoundError(
                f"Fichier requis absent : {path}"
            )

    print(
        "\n[1/5] Sauvegardes"
    )

    for path in FILES:
        backup(
            path
        )

    print(
        "\n[2/5] Modèle"
    )

    patch_model()

    print(
        "\n[3/5] Service"
    )

    patch_service()

    print(
        "\n[4/5] Contrôleur"
    )

    patch_controller()

    print(
        "\n[5/5] Vérification syntaxique"
    )

    compile_files()

    print(
        "\n=============================================="
    )

    print(
        "PATCH DU COEUR HITL TERMINE AVEC SUCCES"
    )

    print(
        "=============================================="
    )

    print(
        "\nNe relancez pas encore EMIDAF."
    )

    print(
        "La prochaine étape sera la migration SQLite."
    )


if __name__ == "__main__":
    main()
