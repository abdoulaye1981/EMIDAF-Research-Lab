"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Study Repository
=========================================================

Persistance des études quantitatives Human-in-the-Loop,
des cas sélectionnés et des affectations aux enseignants.
=========================================================
"""

from __future__ import annotations

from sqlalchemy import func, select

from database.database_manager import DatabaseManager
from database.models.teacher_validation_study_model import (
    TeacherValidationStudyModel,
)
from database.models.teacher_validation_case_model import (
    TeacherValidationCaseModel,
)
from database.models.teacher_validation_assignment_model import (
    TeacherValidationAssignmentModel,
)


class TeacherValidationStudyRepository:

    def __init__(
        self,
        database_manager: DatabaseManager,
    ) -> None:

        self._database = database_manager

    def add_study(
        self,
        study: TeacherValidationStudyModel,
    ) -> TeacherValidationStudyModel:

        with self._database.session_scope() as session:

            session.add(study)
            session.flush()
            session.refresh(study)
            session.expunge(study)

            return study

    def get_study(
        self,
        study_id: int,
    ) -> TeacherValidationStudyModel | None:

        with self._database.session_scope() as session:

            study = session.get(
                TeacherValidationStudyModel,
                int(study_id),
            )

            if study is not None:
                session.expunge(study)

            return study

    def get_studies_for_dataset(
        self,
        project_id: int,
        dataset_id: int,
    ) -> list[TeacherValidationStudyModel]:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationStudyModel)
                .where(
                    TeacherValidationStudyModel.project_id
                    == int(project_id),
                    TeacherValidationStudyModel.dataset_id
                    == int(dataset_id),
                )
                .order_by(
                    TeacherValidationStudyModel.created_at.desc()
                )
            )

            studies = list(
                session.scalars(statement).all()
            )

            for study in studies:
                session.expunge(study)

            return studies

    def update_study(
        self,
        study: TeacherValidationStudyModel,
    ) -> TeacherValidationStudyModel:

        with self._database.session_scope() as session:

            merged = session.merge(study)
            session.flush()
            session.refresh(merged)
            session.expunge(merged)

            return merged

    def add_cases(
        self,
        cases: list[TeacherValidationCaseModel],
    ) -> list[TeacherValidationCaseModel]:

        if not cases:
            return []

        with self._database.session_scope() as session:

            session.add_all(cases)
            session.flush()

            result = []

            for case in cases:
                session.refresh(case)
                session.expunge(case)
                result.append(case)

            return result

    def get_case(
        self,
        case_id: int,
    ) -> TeacherValidationCaseModel | None:

        with self._database.session_scope() as session:

            case = session.get(
                TeacherValidationCaseModel,
                int(case_id),
            )

            if case is not None:
                session.expunge(case)

            return case

    def get_cases(
        self,
        study_id: int,
    ) -> list[TeacherValidationCaseModel]:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationCaseModel)
                .where(
                    TeacherValidationCaseModel.study_id
                    == int(study_id)
                )
                .order_by(
                    TeacherValidationCaseModel.sampling_rank.asc()
                )
            )

            cases = list(
                session.scalars(statement).all()
            )

            for case in cases:
                session.expunge(case)

            return cases

    def count_cases(
        self,
        study_id: int,
    ) -> int:

        with self._database.session_scope() as session:

            statement = (
                select(
                    func.count(
                        TeacherValidationCaseModel.id
                    )
                )
                .where(
                    TeacherValidationCaseModel.study_id
                    == int(study_id)
                )
            )

            return int(
                session.scalar(statement) or 0
            )

    def add_assignments(
        self,
        assignments: list[
            TeacherValidationAssignmentModel
        ],
    ) -> list[TeacherValidationAssignmentModel]:

        if not assignments:
            return []

        with self._database.session_scope() as session:

            session.add_all(assignments)
            session.flush()

            result = []

            for assignment in assignments:
                session.refresh(assignment)
                session.expunge(assignment)
                result.append(assignment)

            return result

    def get_assignment(
        self,
        assignment_id: int,
    ) -> TeacherValidationAssignmentModel | None:

        with self._database.session_scope() as session:

            assignment = session.get(
                TeacherValidationAssignmentModel,
                int(assignment_id),
            )

            if assignment is not None:
                session.expunge(assignment)

            return assignment

    def get_assignment_for_teacher(
        self,
        assignment_id: int,
        teacher_user_id: int,
    ) -> TeacherValidationAssignmentModel | None:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationAssignmentModel)
                .where(
                    TeacherValidationAssignmentModel.id
                    == int(assignment_id),
                    TeacherValidationAssignmentModel.teacher_user_id
                    == int(teacher_user_id),
                )
                .limit(1)
            )

            assignment = session.scalar(
                statement
            )

            if assignment is not None:
                session.expunge(assignment)

            return assignment

    def get_assignments(
        self,
        study_id: int,
    ) -> list[TeacherValidationAssignmentModel]:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationAssignmentModel)
                .where(
                    TeacherValidationAssignmentModel.study_id
                    == int(study_id)
                )
                .order_by(
                    TeacherValidationAssignmentModel.id.asc()
                )
            )

            assignments = list(
                session.scalars(statement).all()
            )

            for assignment in assignments:
                session.expunge(assignment)

            return assignments

    def get_assignments_for_teacher(
        self,
        study_id: int,
        teacher_user_id: int,
    ) -> list[TeacherValidationAssignmentModel]:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationAssignmentModel)
                .where(
                    TeacherValidationAssignmentModel.study_id
                    == int(study_id),
                    TeacherValidationAssignmentModel.teacher_user_id
                    == int(teacher_user_id),
                )
                .order_by(
                    TeacherValidationAssignmentModel.id.asc()
                )
            )

            assignments = list(
                session.scalars(statement).all()
            )

            for assignment in assignments:
                session.expunge(assignment)

            return assignments

    def update_assignment(
        self,
        assignment: TeacherValidationAssignmentModel,
    ) -> TeacherValidationAssignmentModel:

        if assignment is None:
            raise ValueError(
                "L'affectation est obligatoire."
            )

        if assignment.id is None:
            raise ValueError(
                "L'affectation doit déjà exister en base."
            )

        with self._database.session_scope() as session:

            merged = session.merge(
                assignment
            )

            session.flush()
            session.refresh(merged)
            session.expunge(merged)

            return merged
