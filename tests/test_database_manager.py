from database.database_manager import DatabaseManager


def main():

    manager = DatabaseManager()

    manager.initialize()

    print()

    print("=" * 60)

    print("TEST DATABASE MANAGER")

    print("=" * 60)

    print()

    print("Base existante :", manager.exists())

    print()

    print("Chemin :")

    print(manager.database_path())

    session = manager.get_session()

    print()

    print("Session SQLAlchemy : OK")

    session.close()

    print()

    print("DatabaseManager OK")


if __name__ == "__main__":

    main()