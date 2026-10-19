from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATHS = [
    Path("database/emidaf.db"),
    Path("database/test_emidaf.db"),
    Path("database/test_emidaf_controller.db"),
]


COLUMNS = {
    "teacher_confidence": "INTEGER",
    "teacher_initial_comment": "TEXT",
    "teacher_post_model_comment": "TEXT",
    "disagreement_reasons": "JSON",
    "validation_status": "VARCHAR(50) DEFAULT 'completed'",
    "judgment_locked_at": "DATETIME",
    "model_revealed_at": "DATETIME",
    "completed_at": "DATETIME",
}


def migrate(path: Path) -> None:

    if not path.exists():

        print(
            f"[SKIP] {path} absent"
        )

        return

    connection = sqlite3.connect(
        path
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            "PRAGMA table_info(teacher_validations)"
        )

        rows = cursor.fetchall()

        if not rows:

            print(
                f"[SKIP] {path} : "
                "table teacher_validations absente"
            )

            return

        existing = {
            row[1]
            for row in rows
        }

        for (
            column,
            sql_type,
        ) in COLUMNS.items():

            if column in existing:

                print(
                    f"[OK] {path} : "
                    f"{column}"
                )

                continue

            print(
                f"[ADD] {path} : "
                f"{column}"
            )

            cursor.execute(
                "ALTER TABLE teacher_validations "
                f"ADD COLUMN {column} {sql_type}"
            )

        # Les anciennes validations déjà présentes
        # sont considérées comme finalisées.
        cursor.execute(
            """
            UPDATE teacher_validations
            SET validation_status = 'completed'
            WHERE validation_status IS NULL
               OR TRIM(validation_status) = ''
            """
        )

        connection.commit()

        print(
            f"[DONE] {path}"
        )

    finally:

        connection.close()


if __name__ == "__main__":

    for db_path in DB_PATHS:

        migrate(
            db_path
        )

    print(
        "\nMigration HITL terminée."
    )
