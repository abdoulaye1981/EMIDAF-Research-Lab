from emidaf_core.bootstrap import Bootstrap


def main():

    print("=" * 60)
    print("TEST BOOTSTRAP")
    print("=" * 60)

    bootstrap = Bootstrap()

    registry = bootstrap.initialize()

    composants = registry.list()

    print()

    print("Nombre de composants :", registry.count())

    print()

    for composant in composants:
        print("✔", composant)

    assert registry.has("configuration_manager")
    assert registry.has("logger_manager")
    assert registry.has("database_manager")
    assert registry.has("workspace_manager")
    assert registry.has("event_manager")
    assert registry.has("app_context")
    assert registry.has("project_repository")
    assert registry.has("project_builder")
    assert registry.has("project_service")
    assert registry.has("project_controller")

    print()
    print("Bootstrap OK")


if __name__ == "__main__":
    main()