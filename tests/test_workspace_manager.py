from emidaf_core.managers.workspace_manager import WorkspaceManager


def main():

    manager = WorkspaceManager()

    print()
    print("=" * 60)
    print("TEST WORKSPACE MANAGER")
    print("=" * 60)

    # =====================================================
    # INITIALISATION
    # =====================================================

    print("\n[INITIALISATION]")

    print("Workspace :", manager.get_workspace())
    print("Projects  :", manager.get_projects())
    print("Templates :", manager.get_templates())
    print("Archives  :", manager.get_archives())
    print("Trash     :", manager.get_trash())

    print("\nNombre de projets :", manager.count_projects())
    print("Liste des projets :", manager.list_projects())

    # =====================================================
    # CREATION
    # =====================================================

    print("\n" + "=" * 60)
    print("TEST CREATE PROJECT")
    print("=" * 60)

    result = manager.create_project("Projet_Test")

    print("Création :", result)
    print("Liste :", manager.list_projects())

    # =====================================================
    # RENOMMAGE
    # =====================================================

    print("\n" + "=" * 60)
    print("TEST RENAME PROJECT")
    print("=" * 60)

    result = manager.rename_project(
        "Projet_Test",
        "Projet_Test_2"
    )

    print("Renommage :", result)
    print("Liste :", manager.list_projects())

    # =====================================================
    # DUPLICATION
    # =====================================================

    print("\n" + "=" * 60)
    print("TEST DUPLICATE PROJECT")
    print("=" * 60)

    result = manager.duplicate_project(
        "Projet_Test_2",
        "Projet_Test_Copie"
    )

    print("Duplication :", result)
    print("Liste :", manager.list_projects())

    # =====================================================
    # ARCHIVAGE
    # =====================================================

    print("\n" + "=" * 60)
    print("TEST ARCHIVE PROJECT")
    print("=" * 60)

    result = manager.archive_project(
        "Projet_Test_Copie"
    )

    print("Archivage :", result)
    print("Liste :", manager.list_projects())

    # =====================================================
    # RESTAURATION
    # =====================================================

    print("\n" + "=" * 60)
    print("TEST RESTORE PROJECT")
    print("=" * 60)

    result = manager.restore_project(
        "Projet_Test_Copie"
    )

    print("Restauration :", result)
    print("Liste :", manager.list_projects())

    # =====================================================
    # SUPPRESSION
    # =====================================================

    print("\n" + "=" * 60)
    print("TEST DELETE PROJECT")
    print("=" * 60)

    result = manager.delete_project(
        "Projet_Test_Copie"
    )

    print("Suppression :", result)
    print("Liste :", manager.list_projects())

    # =====================================================
    # FIN
    # =====================================================

    print()
    print("=" * 60)
    print("TOUS LES TESTS DU WORKSPACE MANAGER SONT TERMINÉS")
    print("=" * 60)


if __name__ == "__main__":
    main()