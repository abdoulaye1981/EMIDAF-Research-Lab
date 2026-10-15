from sqlalchemy import inspect, text

from emidaf_core.bootstrap.bootstrap import Bootstrap


bootstrap = Bootstrap()
bootstrap.initialize()

with bootstrap.database_manager.session_scope() as session:

    connection = session.connection()

    inspector = inspect(
        connection
    )

    columns = {
        column["name"]
        for column in inspector.get_columns(
            "teacher_validations"
        )
    }

    if "teacher_detected_class" in columns:

        print(
            "Colonne teacher_detected_class "
            "déjà présente."
        )

    else:

        connection.execute(
            text(
                """
                ALTER TABLE teacher_validations
                ADD COLUMN teacher_detected_class
                VARCHAR(50)
                """
            )
        )

        print(
            "Colonne teacher_detected_class "
            "ajoutée avec succès."
        )
