from emidaf_core.bootstrap import Bootstrap


def main():

    bootstrap = Bootstrap()

    registry = bootstrap.initialize()

    print()
    print("=" * 60)
    print("DEPENDENCY INJECTION")
    print("=" * 60)
    print()

    composants = [
        "configuration_manager",
        "logger_manager",
        "database_manager",
        "workspace_manager",
        "event_manager",
        "app_context",
        "project_repository",
        "project_builder",
        "project_service",
        "project_controller"
    ]

    for composant in composants:

        print(
            f"{composant:<25} :",
            "OK" if registry.exists(composant) else "ERREUR"
        )

    print()
    print("Injection de dépendances validée.")


if __name__ == "__main__":
    main()