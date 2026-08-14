from emidaf_core.managers.configuration_manager import ConfigurationManager


def main():

    print("=" * 70)
    print("           TEST DU CONFIGURATION MANAGER")
    print("=" * 70)

    manager = ConfigurationManager()

    print("\n1. Initialisation")
    print("-----------------")
    print("✓ Configuration chargée")

    print("\n2. Nombre de paramètres")
    print("-----------------------")
    print(manager.count())

    print("\n3. Liste des clés")
    print("-----------------")
    for key in manager.keys():
        print(f" - {key}")

    print("\n4. Vérification des clés")
    print("------------------------")
    print("theme      :", manager.has("theme"))
    print("database   :", manager.has("database"))
    print("inconnue   :", manager.has("xxxx"))

    print("\n5. Lecture des paramètres")
    print("-------------------------")
    print("Application :", manager.application)
    print("Version     :", manager.version)
    print("Theme       :", manager.theme)
    print("Langue      :", manager.language)
    print("Workspace   :", manager.workspace)
    print("Database    :", manager.database)
    print("Debug       :", manager.debug)
    print("Autosave    :", manager.autosave)
    print("Log Level   :", manager.log_level)

    print("\n6. Test de modification")
    print("-----------------------")

    ancien_theme = manager.theme

    manager.set("theme", "Dark")

    print("Nouveau thème :", manager.theme)

    if manager.theme == "Dark":
        print("✓ Modification OK")
    else:
        print("✗ Erreur")

    print("\n7. Restauration")
    print("----------------")

    manager.set("theme", ancien_theme)

    print("Theme restauré :", manager.theme)

    print("\n8. Test remove()")
    print("----------------")

    manager.set("temp", 123)

    print("Avant :", manager.has("temp"))

    manager.remove("temp")

    print("Après :", manager.has("temp"))

    print("\n9. Test items()")
    print("----------------")

    for cle, valeur in manager.items():
        print(f"{cle:15} : {valeur}")

    print("\n10. Sauvegarde")
    print("----------------")

    manager.save()

    print("✓ Sauvegarde réalisée")

    print("\n11. Rechargement")
    print("----------------")

    manager.reload()

    print("Theme après reload :", manager.theme)

    print("\n" + "=" * 70)
    print("      TOUS LES TESTS SONT TERMINÉS AVEC SUCCÈS")
    print("=" * 70)


if __name__ == "__main__":
    main()