from pathlib import Path

from emidaf_core.managers.logger_manager import LoggerManager


def main():

    logger = LoggerManager()

    logger.info("Framework EMIDAF démarré.")

    logger.project.info("Projet créé.")

    logger.importer.info("Import CSV.")

    logger.inspection.info("Inspection terminée.")

    logger.error.error("Erreur simulée.")

    print()

    print("=" * 60)
    print("TEST LOGGER MANAGER")
    print("=" * 60)

    print()

    print("Loggers enregistrés")

    print("-------------------")

    for name in logger.list():

        print(name)

    print()

    print("Fichiers")

    print("---------")

    for file in [

        "application.log",

        "project.log",

        "import.log",

        "inspection.log",

        "error.log"

    ]:

        path = Path("logs") / file

        print(

            f"{file:<20} : {'OK' if path.exists() else 'ERREUR'}"

        )

    print()

    print("LoggerManager OK")


if __name__ == "__main__":

    main()