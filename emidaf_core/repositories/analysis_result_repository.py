"""
=========================================================
EMIDAF Framework
Analysis Result Repository
=========================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from database.database_manager import DatabaseManager
from database.models.analysis_result_model import (
    AnalysisResultModel,
)


class AnalysisResultRepository:

    def __init__(
        self,
        database_manager: DatabaseManager,
    ) -> None:

        self._database = database_manager

    def upsert(
        self,
        project_id: int,
        dataset_id: int,
        stage: str,
        payload: Any,
    ) -> AnalysisResultModel:
        """
        Effectue un véritable UPSERT SQLite atomique.

        La contrainte unique porte sur :
        (project_id, dataset_id, stage).

        Cela évite les collisions lorsque plusieurs
        callbacks Dash écrivent simultanément le même
        résultat analytique.
        """

        project_id = int(project_id)
        dataset_id = int(dataset_id)
        stage = str(stage)

        with self._database.session_scope() as session:

            statement = (
                sqlite_insert(
                    AnalysisResultModel
                )
                .values(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    stage=stage,
                    payload=payload,
                )
                .on_conflict_do_update(
                    index_elements=[
                        AnalysisResultModel.project_id,
                        AnalysisResultModel.dataset_id,
                        AnalysisResultModel.stage,
                    ],
                    set_={
                        "payload": payload,
                        "updated_at": (
                            func.current_timestamp()
                        ),
                    },
                )
            )

            session.execute(statement)
            session.flush()

            result = session.scalar(
                select(
                    AnalysisResultModel
                ).where(
                    AnalysisResultModel.project_id
                    == project_id,
                    AnalysisResultModel.dataset_id
                    == dataset_id,
                    AnalysisResultModel.stage
                    == stage,
                )
            )

            return result

    def get(
        self,
        project_id: int,
        dataset_id: int,
        stage: str,
    ):

        with self._database.session_scope() as session:

            statement = select(
                AnalysisResultModel
            ).where(
                AnalysisResultModel.project_id
                == int(project_id),
                AnalysisResultModel.dataset_id
                == int(dataset_id),
                AnalysisResultModel.stage
                == str(stage),
            )

            result = session.scalar(statement)

            if result is None:
                return None

            return result.payload

    def exists(
        self,
        project_id: int,
        dataset_id: int,
        stage: str,
    ) -> bool:

        with self._database.session_scope() as session:

            statement = select(
                AnalysisResultModel.id
            ).where(
                AnalysisResultModel.project_id
                == int(project_id),
                AnalysisResultModel.dataset_id
                == int(dataset_id),
                AnalysisResultModel.stage
                == str(stage),
            )

            return (
                session.scalar(statement)
                is not None
            )

    def get_all(
        self,
        project_id: int,
        dataset_id: int,
    ) -> dict[str, Any]:

        with self._database.session_scope() as session:

            statement = select(
                AnalysisResultModel
            ).where(
                AnalysisResultModel.project_id
                == int(project_id),
                AnalysisResultModel.dataset_id
                == int(dataset_id),
            )

            results = session.scalars(
                statement
            ).all()

            return {
                result.stage: result.payload
                for result in results
            }

    def delete(
        self,
        project_id: int,
        dataset_id: int,
        stage: str,
    ) -> None:

        with self._database.session_scope() as session:

            statement = delete(
                AnalysisResultModel
            ).where(
                AnalysisResultModel.project_id
                == int(project_id),
                AnalysisResultModel.dataset_id
                == int(dataset_id),
                AnalysisResultModel.stage
                == str(stage),
            )

            session.execute(statement)

    def delete_dataset(
        self,
        project_id: int,
        dataset_id: int,
    ) -> None:

        with self._database.session_scope() as session:

            statement = delete(
                AnalysisResultModel
            ).where(
                AnalysisResultModel.project_id
                == int(project_id),
                AnalysisResultModel.dataset_id
                == int(dataset_id),
            )

            session.execute(statement)

    def delete_all(self) -> None:

        with self._database.session_scope() as session:
            session.execute(
                delete(AnalysisResultModel)
            )
